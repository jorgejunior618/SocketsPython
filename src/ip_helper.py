from socket import gethostname, gethostbyname

class IPHelper:
  def __init__(self) -> None:
    self.ipLocal = gethostbyname(gethostname())
    self.portaChat: int = 4321
    self.portaJogo: int = 1234
    self.ipAdversario: str = None

  def ipValido(self, ip: str) -> bool:
    ''' # ipValido
    Função que valida se o [ip] informado no parâmetro está no formato esperado

    ## Parâmetros:
    ip : str
        Endereço de ip a ser validado

    ## Retorno:
    valido : bool
        Caso o [ip] seja válido, retorna True, e caso contrario retorna False
    '''
    if len(ip) < 7:
      return False
    
    identificadores = ip.split('.')
    if len(identificadores) < 4:
      return False

    id_int = None
    for id in identificadores:
      try:
        id_int = int(id)
        if id_int < 0 or id_int > 255:
          return False
      except:
        return False

    return True

  def setIpAdversario(self, ip: str) -> None:
    ''' # setIpAdversario
    Função que define, com o [ip] informado, o IP do usuário

    ## Parâmetros:
    ip : str
        Endereço de ip a ser guardado
    '''
    self.ipAdversario = ip

  def obterEnderecoLocalJogo(self) ->tuple[str, int]:
    ''' # obterEnderecoLocalJogo
    Função que define, com o [ip] informado, o IP do usuário

    ## Retorna:
    endereco : str
        O endereço de IP Local para ser utilizado no Jogo
    porta : int
        A porta Local para ser utilizada na comunicação no Jogo
    '''
    return self.ipLocal, self.portaJogo

  def obterEnderecoLocalChat(self) ->tuple[str, int]:
    ''' # obterEnderecoLocalChat
    Função que define, com o [ip] informado, o IP do usuário

    ## Retorna:
    endereco : str
        O endereço de IP Local para ser utilizado no Chat
    porta : int
        A porta Local para ser utilizada na comunicação no Chat
    '''
    return self.ipLocal, self.portaChat

  def obterEnderecoAdversarioJogo(self) ->tuple[str, int]:
    ''' # obterEnderecoAdversarioJogo
    Função que define, com o [ip] informado, o IP do usuário

    ## Retorna:
    endereco : str
        O endereço de IP do Adversario para ser utilizado no Jogo
    porta : int
        A porta do Adversario para ser utilizada na comunicação no Jogo
    '''
    return self.ipAdversario, self.portaJogo

  def obterEnderecoAdversarioChat(self) ->tuple[str, int]:
    ''' # obterEnderecoAdversarioChat
    Função que define, com o [ip] informado, o IP do usuário

    ## Retorna:
    endereco : str
        O endereço de IP do Adversario para ser utilizado no Chat
    porta : int
        A porta do Adversario para ser utilizada na comunicação no Chat
    '''
    return self.ipAdversario, self.portaChat
