import socket

class Cliente():
    """
    Classe Cliente - API Socket
    """
    def __init__(self, server_ip, port):
        """
        Construtor da classe Cliente
        """
        self.__server_ip = server_ip
        self.__port = port
    
    def start(self):
        """
        Método que inicializa a execução do Cliente
        """
        self.__tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        endpoint = (self.__server_ip,self.__port)
        try:
            self.__tcp.connect(endpoint)
            print("Conexão realizada com sucesso!")
            self.__method()
        except:
            print("Servidor não disponível")

    
    def __method(self):
        """
        Método que implementa as requisições do cliente
        """
        try:
            msg = ''
            while msg != '\x18':
                msg = input("Digite o simbolo da empresa (x para sair): ")
                op = input(
                    "\nOperacoes:\n\n E - para endereço da Empresa\n T - Telefone da Empresa\n S - Site\n D - Taxa de Dividendo\n\nDigite a operacao desejada: "
                )
                
                msg = str(op.upper() + ' ' + msg.upper())
                #print("\n"+ msg + "\n")
                if msg == '':
                    continue
                elif msg == 'x':
                    break

                self.__tcp.send(bytes(msg, 'ascii'))
                resp = self.__tcp.recv(1024)
                print('\n' + resp.decode('ascii'))
            self.__tcp.close()
        except Exception as e:
            print("Erro ao realizar comunicação com o servidor", e.args)
