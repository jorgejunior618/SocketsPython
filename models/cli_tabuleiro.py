import socket
import models.resta_um as r1

class CliTabuleiroSocket:
  '''# class TabuleiroSocket
  Classe com a implementação dos sockets para a comunicação em texto, e as threads de envio e recebimento das mensagens

  ## Parâmetros:
  endereco_local : tuple[str, int]
      tupla contendo a string que representa o IP da maquina atual, e a porta que receberá a comunicação
  endereco_destino : tuple[str, int]
      tupla contendo a string que representa o IP da maquina de destino, e a porta que receberá a comunicação
  '''

  def __init__(self, endereco_local: tuple[str, int], endereco_destino: tuple[str, int]):
    self.jogo = r1.JogoRestaUm()
    self.endereco_destino = endereco_destino
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.sock.bind(endereco_local)

  def receberTurno(self):
    turno, _ = self.sock.recvfrom(1024)
    turno = turno.decode()
    return int(turno)

  def definirTurno(self, turno: str):
    self.sock.sendto(turno.encode(), self.endereco_destino)

  def receberLance(self):
    '''## receber_lance()
    Recebe o lance do adversário via Socket
    '''
    dados, _ = self.sock.recvfrom(1024)
    movimento = dados.decode()
    if movimento == "fim":
      return False

    mover, retirar = self.jogo.recebeMovimento(movimento)
    _, destino = self.jogo.movimentoValido(mover, retirar)
    self.jogo.fazMovimento(mover, retirar, destino)
    return True
    # self.jogo.imprimeTabuleiro()

  def enviarLance(self, movimento: str) -> bool:
    '''## enviar_lance()
    Recebe o lance e envia para o adversário via Socket
    '''
    if movimento == "fim":
      self.sock.sendto(movimento.encode(), self.endereco_destino)
      return True

    mover, retirar = self.jogo.recebeMovimento(movimento)
    valido, destino = self.jogo.movimentoValido(mover, retirar)

    if not valido:
      return False

    self.jogo.fazMovimento(mover, retirar, destino)
    self.sock.sendto(movimento.encode(), self.endereco_destino)
    return True
