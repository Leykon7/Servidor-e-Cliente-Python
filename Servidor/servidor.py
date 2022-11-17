import socket
import threading
import yahooquery as yq

class Servidor():
    """
    Classe Servidor - API Socket
    """
    def __init__(self, host, port):
        """
        Construtor da classe servidor
        """
        self._host = host
        self._port = port
    
    def start(self):
        """
        Método que inicializa a execução do servidor
        """
        self.__tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        endpoint = (self._host,self._port)
        try:
            self.__tcp.bind(endpoint)
            self.__tcp.listen(1)
            print("Servidor iniciado em ",self._host,": ", self._port)
            while True:
                con, client = self.__tcp.accept()
                self._service(con,client)
        except Exception as e:
            print("Erro ao inicializar o servidor",e.args)
    
    def _service(self, con, client):
        """
        Método que implementa o serviço de calculadora
        :param con: objeto socket utilizado para enviar e receber dados
        :param client: é o endereço do cliente
        """
        print("Atendendo cliente ", client)
        while True:
            try: 
                msg = con.recv(1024)
                msg_s = str(msg.decode('ascii'))

                print("\n"+msg_s+"\n")

                listaMsg = msg_s.split()
                print("\n")
                print(listaMsg)
                print("\n")
                print(listaMsg[0])
                print("\n")
                print(listaMsg[1])
                print("\n")
                info = yq.Ticker(listaMsg[1])

                if listaMsg[0] == 'C':
                    con.send(bytes(info.company_officers))
                if listaMsg[0] == 'S':
                    con.send(bytes(info.summary_profile))
                if listaMsg[0] == 'H':
                    con.send(bytes(info.earning_history))
                if listaMsg[0] == 'P':
                    con.send(bytes(info.esg_scores))


                print(client," -> requisição atendida")
            except OSError as e:
                print("\nErro de conexão ",client,": ",e.args)
                return  
            except Exception as e:
                print("Erro nos dados recebidos pelo cliente ",client,": ",e.args)
                con.send(bytes("\nErro\n",'ascii'))