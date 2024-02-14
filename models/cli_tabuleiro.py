import socket
import threading
import rascunho.resta_um_terminal as r1

class CliTabuleiroSocket:
  '''## class TabuleiroSocket
  Classe com a implementação dos sockets para a comunicação em texto, e as threads de envio e recebimento das mensagens

  ### Parametros
  endereco_local : tuple[str, int]
      tupla contendo a string que representa o IP da maquina atual, e a porta que receberá a comunicação
  endereco_destino : tuple[str, int]
      tupla contendo a string que representa o IP da maquina de destino, e a porta que receberá a comunicação
  '''

  def __init__(self, endereco_local: tuple[str, int], endereco_destino: tuple[str, int]):
    self.jogo = r1.JogoRestaUm()
    self.jogo.reiniciaTabuleiro()
    self.endereco_destino = endereco_destino
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.sock.bind(endereco_local)

  def receber_lance(self):
    '''## receber_lance()
    Recebe o lance do adversário via Socket
    '''
    while True:
      dados, _ = self.sock.recvfrom(1024)

      movimento = dados.decode()
      print(f"\n[adversário]: {movimento}")
      mover, retirar = self.jogo.recebeMovimento(movimento)
      _, destino = self.jogo.movimentoValido(mover, retirar)
      self.jogo.fazMovimento(mover, retirar, destino)
      self.jogo.imprimeTabuleiro()

  def enviar_lance(self):
    '''## enviar_lance()
    Recebe o lance e envia para o adversário via Socket
    '''
    while True:
      movimento = input("Seu movimento: ")
      mover, retirar = self.jogo.recebeMovimento(movimento)
      valido, destino = self.jogo.movimentoValido(mover, retirar)

      while(not valido):
        valido, destino = self.jogo.movimentoValido(mover, retirar)

      self.jogo.fazMovimento(mover, retirar, destino)
      self.jogo.imprimeTabuleiro()
      self.sock.sendto(movimento.encode(), self.endereco_destino)

  def iniciar(self):
    thread_recebimento = threading.Thread(target=self.receber_lance)
    thread_recebimento.daemon = True
    thread_recebimento.start()
    self.enviar_lance()
