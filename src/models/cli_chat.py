from socket import socket, AF_INET, SOCK_DGRAM

class CliChatSocket:
  ''' # class ChatSocket
  Classe com a implementação dos sockets para a comunicação em texto, e as threads de envio e recebimento das mensagens

  ## Parâmetros:
  endereco_local : tuple[str, int]
      tupla contendo a string que representa o IP da maquina atual, e a porta que receberá a comunicação
  endereco_destino : tuple[str, int]
      tupla contendo a string que representa o IP da maquina de destino, e a porta que receberá a comunicação
  '''
  def __init__(self, endereco_local: tuple[str, int], endereco_destino: tuple[str, int]):
    ''' Inicializa o socket com o endereço local fornecido, e guarda o endereço do adversário '''
    self.endereco_destino = endereco_destino
    self.sock = socket(AF_INET, SOCK_DGRAM)
    self.sock.bind(endereco_local)

  def receber_mensagem(self) -> str:
    ''' # receber_mensagem
    Função que escuta a porta do endereço local esperando recebimento da mensagem do adversario

    ## Retorna:
    mensagem : str
        String com a mensagem recebida na comunicação do chat
    '''
    dados, _ = self.sock.recvfrom(1024)
    mensagem = dados.decode()
    return mensagem

  def enviar_mensagem(self, mensagem: str) -> None:
    ''' # enviar_mensagem
    Função que escuta a porta do endereço local esperando recebimento da mensagem do adversario

    ## Parâmetro:
    mensagem : str
        String com a mensagem para envio na comunicação do chat
    '''
    dados = mensagem.encode()
    self.sock.sendto(dados, self.endereco_destino)
