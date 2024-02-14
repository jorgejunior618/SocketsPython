import socket
import threading

class CliChatSocket:
  '''## class ChatSocket
  Classe com a implementação dos sockets para a comunicação em texto, e as threads de envio e recebimento das mensagens

  ### Parametros
  endereco_local : tuple[str, int]
      tupla contendo a string que representa o IP da maquina atual, e a porta que receberá a comunicação
  endereco_destino : tuple[str, int]
      tupla contendo a string que representa o IP da maquina de destino, e a porta que receberá a comunicação
  '''
  def __init__(self, endereco_local: tuple[str, int], endereco_destino: tuple[str, int]):
    self.endereco_destino = endereco_destino
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.sock.bind(endereco_local)

  def receber_mensagens(self):
    while True:
      dados, endereco = self.sock.recvfrom(1024)
      print(f"\n[{endereco}]: {dados.decode()}", end="\n> ")

  def enviar_mensagem(self):
    while True:
      mensagem = input("> ")
      self.sock.sendto(mensagem.encode(), self.endereco_destino)

  def iniciar(self):
    thread_recebimento = threading.Thread(target=self.receber_mensagens)
    thread_recebimento.daemon = True
    thread_recebimento.start()
    self.enviar_mensagem()
