from socket import gethostname, gethostbyname

class IPHelper:
  def __init__(self) -> None:
    self.ipLocal = gethostbyname(gethostname())
    self.portaChat: int = 4321
    self.portaJogo: int = 1234
    self.ipAdversario: str = None

  def ipValido(self, ip: str) -> bool:
    if len(ip) < 7:
      return False
    
    identificadores = ip.split('.')
    if len(identificadores) < 4:
      return False

    id_int = None
    for id in identificadores:
      try:
        id_int = int(id)
        if id_int < 0:
          return False
      except:
        return False

    return True

  def defineEnderecoLocalJogo(self) ->tuple[str, int]:
    return self.ipLocal, self.portaJogo

  def defineEnderecoLocalChat(self) ->tuple[str, int]:
    return self.ipLocal, self.portaChat

  def defineEnderecoAdversarioJogo(self) ->tuple[str, int]:
    return self.ipAdversario, self.portaJogo

  def defineEnderecoAdversarioChat(self) ->tuple[str, int]:
    return self.ipAdversario, self.portaChat

  def setIpAdversario(self, ip):
    self.ipAdversario = ip
