import socket
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

  def defineTurno(self):
    turno, _ = self.sock.recvfrom(1024)
    print(f" Seu adversário escolheu ser o jogador {turno}")
    return int(turno)

  def recebeTurno(self):
    turno = input("\n Sua opção: ")
    while turno != '1' and turno != '2':
      turno = input(" Digite apenas 1 ou 2: ")

    self.sock.sendto(turno, self.endereco_destino)
    turno = int(turno)
    return turno

  def receberLance(self):
    '''## receber_lance()
    Recebe o lance do adversário via Socket
    '''
    dados, _ = self.sock.recvfrom(1024)
    movimento = dados.decode()

    print(f"\n [adversário]: {movimento}")
    mover, retirar = self.jogo.recebeMovimento(movimento)
    _, destino = self.jogo.movimentoValido(mover, retirar)
    self.jogo.fazMovimento(mover, retirar, destino)
    self.jogo.imprimeTabuleiro()

  def enviarLance(self):
    '''## enviar_lance()
    Recebe o lance e envia para o adversário via Socket
    '''
    movimento = input(" Seu movimento: ")
    mover, retirar = self.jogo.recebeMovimento(movimento)
    valido, destino = self.jogo.movimentoValido(mover, retirar)

    while(not valido):
      valido, destino = self.jogo.movimentoValido(mover, retirar)

    self.jogo.fazMovimento(mover, retirar, destino)
    self.jogo.imprimeTabuleiro()
    self.sock.sendto(movimento.encode(), self.endereco_destino)

  def iniciarJogador1(self):
    self.jogo.imprimeTabuleiro()

    acabou, contPecas = self.jogo.estaNoFim()
    while not acabou:
      self.enviarLance()
      acabou, contPecas = self.jogo.estaNoFim()
      if acabou: break
      self.receberLance()
      acabou, contPecas = self.jogo.estaNoFim()

    self.jogo.imprimeTabuleiro(self.jogo.tabuleiro)
    if contPecas > 1:
      print(f"\n Peças restantes: {contPecas}")
      print(f" O vencedor é do jogador {2 - self.jogo.turno}\n")
    else:
      print(f" Parabens restou {contPecas}!")
      print(f" O vencedor é do jogador {self.jogo.turno + 1}\n")

  def iniciarJogador2(self):
    self.jogo.imprimeTabuleiro()

    acabou, contPecas = self.jogo.estaNoFim()
    while not acabou:
      self.receberLance()
      acabou, contPecas = self.jogo.estaNoFim()
      if acabou: break
      self.enviarLance()
      acabou, contPecas = self.jogo.estaNoFim()

    self.jogo.imprimeTabuleiro(self.jogo.tabuleiro)
    if contPecas > 1:
      print(f"\n Peças restantes: {contPecas}")
      print(f" O vencedor é do jogador {2 - self.jogo.turno}\n")
    else:
      print(f" Parabens restou {contPecas}!")
      print(f" O vencedor é do jogador {self.jogo.turno + 1}\n")
