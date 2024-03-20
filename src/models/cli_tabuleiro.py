from socket import socket, AF_INET, SOCK_DGRAM
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
    self.sock = socket(AF_INET, SOCK_DGRAM)
    self.sock.bind(endereco_local)

  def receberTurno(self) -> int:
    ''' # receberTurno
    Função que escuta a porta do endereço local esperando a decisão de turno do adversario

    ## Retorna:
    turno : int
        0 se o adversário decidiu ser o primeiro do jogo e 1 caso contrário
    '''
    turno, _ = self.sock.recvfrom(1024)
    turno = turno.decode()
    return int(turno)

  def definirTurno(self, turno: str):
    ''' # definirTurno
    Função que envia para o endereço destino  a decisão de turno do usuário local

    ## Parâmetros:
    turno : int
        0 se o usuário decidiu ser o primeiro do jogo e 1 caso contrário
    '''
    self.sock.sendto(turno.encode(), self.endereco_destino)

  def receberLance(self) -> bool:
    ''' # receber_lance
    Recebe o lance do adversário via Socket, verifica se foi o sinal de fim de jogo, faz o movimento na 
    estrutura de dados local e retorna se o movimento foi realizado

    ## Retorna:
    continuar : bool
        `False` caso seja recebido o final de fim de jogo, e `True` se o movimento do adversário for registrado
    '''
    dados, _ = self.sock.recvfrom(1024)
    movimento = dados.decode()
    if movimento == "fim":
      return False, False
    if movimento == "resign":
      return False, True

    mover, retirar = self.jogo.recebeMovimento(movimento)
    _, destino = self.jogo.movimentoValido(mover, retirar)
    self.jogo.fazMovimento(mover, retirar, destino)
    return True, False

  def enviarLance(self, movimento: str) -> bool:
    ''' # enviarLance
    Função que escuta a porta do endereço local esperando recebimento do movimento do adversario

    ## Parâmetro:
    movimento : str
        String com o movimento para envio na comunicação do chat
    
    ## Retorno:
    bool
        True caso o movimento/envio foi feito corretamente, false caso seja um movimento inválido
    '''
    if movimento == "fim":
      self.sock.sendto(movimento.encode(), self.endereco_destino)
      return True
    if movimento == "resign":
      self.sock.sendto(movimento.encode(), self.endereco_destino)
      return True

    mover, retirar = self.jogo.recebeMovimento(movimento)
    valido, destino = self.jogo.movimentoValido(mover, retirar)

    if not valido:
      return False

    self.jogo.fazMovimento(mover, retirar, destino)
    self.sock.sendto(movimento.encode(), self.endereco_destino)
    return True
