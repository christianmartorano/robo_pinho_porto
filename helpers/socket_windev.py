import socket

def client_socket(mensagem):
    HOST = '127.0.0.1'
    PORT = 8000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.send(b'%b\r\n' % mensagem.encode('utf-8'))
        print("Mensagem enviada => {}".format(mensagem))
        msg = s.recv(1024)
        print("Mensagem recebida => {}".format(msg.decode('utf-8')))
