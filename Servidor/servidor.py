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

                #print("\n"+msg_s)
                listaMsg = msg_s.split()
                # print(listaMsg)
                # print(listaMsg[0])
                # print(listaMsg[1])
                # print("\n")
                
                info = yq.Ticker(listaMsg[1])

                if listaMsg[0] == 'E':

                    # print(info.summary_profile["adress1"])
                    # a = info.summary_profile
                    # print('\n' + a)
                    # a = a["adress1"]
                    # print('\n' + a)

                    #con.send(bytes(info.summary_profile[listaMsg[1]]['address1'],'ascii'))
                    con.send(bytes(info.summary_detail[listaMsg[1]]['bid'], 'ascii'))
                if listaMsg[0] == 'T':
                    con.send(bytes(info.summary_profile[listaMsg[1]]['phone'],'ascii'))
                if listaMsg[0] == 'S':
                    con.send(bytes(info.summary_profile[listaMsg[1]]['website'],'ascii'))
                if listaMsg[0] == 'D':
                    con.send(bytes(info.summary_detail[listaMsg[1]]['dividendRate'],'ascii'))

                print(client," -> requisição atendida")
            except OSError as e:
                print("\nErro de conexão ",client,": ",e.args)
                return  
            except Exception as e:
                print("Erro nos dados recebidos pelo cliente ",client,": ",e.args)
                con.send(bytes("\nErro\n",'ascii'))
