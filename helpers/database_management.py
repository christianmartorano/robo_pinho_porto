import pypyodbc

CONN = ""

def conecta_banco():
    conn = pypyodbc.connect('DSN=hfsql')
    return conn

def fecha_conexao():
    global CONN
    CONN.close()

def usuario_senha():
    global CONN
    cursor = CONN.cursor()

    query = '''
        SELECT
            parametros.parametrosUsuario AS qUSUARIO,
            parametros.parametrosSenha   AS qSENHA,
            parametros.parametrosURL     AS qURL
        FROM
            parametros'''
    res = cursor.execute(query)
    row = res.fetchone()
    return row

def select_cliente():
    global CONN
    cursor = CONN.cursor()

    query = '''
        SELECT
            cliente.clienteSinistro     AS qSINISTRO,
            cliente.clienteAnoSinistro  AS qANO
        FROM
            cliente
        WHERE
            cliente.clienteExportado = 0 '''
    res = cursor.execute(query)
    return res

def count_cliente():
    global CONN
    cursor = CONN.cursor()

    query = '''
        SELECT
            COUNT(*)
        FROM
            cliente
        WHERE
            cliente.clienteExportado = 0 '''

    res = cursor.execute(query)

    qtd = res.fetchone()[0]

    return qtd

def update_cliente_exportado(sinistro, anoSinistro):
    global CONN
    cursor = CONN.cursor()

    query = '''
        UPDATE
            cliente
        SET
            clienteExportado = 1
        WHERE
            clienteSinistro     = '{}' AND
            clienteAnoSinistro  = '{}' '''

    cursor.execute(query.format(sinistro, anoSinistro))

    print("Update => {}".format(query.format(sinistro, anoSinistro)))

def update(cliente_dados, sinistro, anoSinistro):
    global CONN

    cursor = CONN.cursor()
    query = '''
        UPDATE cliente
            SET clienteEndereco                     = '{}',
                clienteDataImportacao               = SYSDATE,
                clientePagamentosIndenizacao        = {},
                clientePagamentosTotalRecuperado    = {},
                clientePagamentosDespesas           = {},
                clientePagamentosSaldoRessarcir     = {},
                clientePagamentosTotalPago          = {},
                clienteImportado                    = 1
            WHERE
                clienteSinistro     = '{}' AND
                clienteAnoSinistro  = '{}'
    '''
    cursor.execute(query.format(cliente_dados['endereco'].replace("'", ""), cliente_dados['indenizacao'].replace(".", "").replace(",","."),
            cliente_dados['total_recuperado'].replace(".", "").replace(",","."),
            cliente_dados['despesas'].replace(".", "").replace(",","."), cliente_dados['saldo_a_ressarcir'].replace(".", "").replace(",","."),
            cliente_dados['total_pago'].replace(".", "").replace(",","."), sinistro, anoSinistro))

    cursor.commit()

    print("UPDATE => {}".format(query.format(cliente_dados['endereco'], cliente_dados['indenizacao'], cliente_dados['total_recuperado'],
        cliente_dados['despesas'], cliente_dados['saldo_a_ressarcir'], cliente_dados['total_pago'], sinistro, anoSinistro)))

def checa_se_ja_existe(sinistro, anoSinistro, cliente_dados):
    global CONN

    cursor = CONN.cursor()

    query = '''
    SELECT TOP 1
        *
    FROM
        clienteGarantidos
    WHERE
        clienteGarantidoSinistro    = '{}' AND
        clienteGarantidoAnoSinistro = '{}' AND
        clienteGarantidoCPF         = '{}' '''

    cursor.execute(query.format(sinistro, anoSinistro, cliente_dados))

    result=cursor.fetchone()

    if result == None:
        return False
    else:
        return True


def insert_dados(cliente_dados, sinistro, anoSinistro):
    global CONN

    update(cliente_dados, sinistro, anoSinistro)

    res = checa_se_ja_existe(sinistro, anoSinistro, cliente_dados['cpf_garantidos'])

    query = ""

    if res == False:
        cursor = CONN.cursor()
        query = '''
            INSERT INTO clienteGarantidos (clienteGarantidoCPF, clienteGarantidoNome, clienteGarantidoSinistro, clienteGarantidoAnoSinistro)
            VALUES ('{}', '{}', '{}', '{}')'''
        cursor.execute(query.format(cliente_dados['cpf_garantidos'].replace("'", ""), cliente_dados['nome_garantidos'].replace("'", ""), sinistro, anoSinistro))
        cursor.commit()
        print("INSERT => {}".format(query.format(cliente_dados['cpf_garantidos'], cliente_dados['nome_garantidos'], sinistro, anoSinistro)))
    else:
        print("CLIENTE {} - {} JÁ EXISTE NO DATABASE!".format(cliente_dados['nome_garantidos'], cliente_dados['cpf_garantidos']))

def main():
    global CONN
    CONN = conecta_banco()
