from models.cli_tabuleiro import CliTabuleiroSocket
from models.cli_chat import CliChatSocket
from gui_resta_um import GuiRestaUm
from ip_helper import IPHelper
from gui_define_ip import GuiDefineAdversario

def mainApp():
  # Inicializando o socket do cliente do jogador
  print("Se tento criar um executavel sem esse console,")
  print("o arquivo é acusado como virus")
  print(";-;")

  iph = IPHelper()
  gdefAdv = GuiDefineAdversario(iph)
  gdefAdv.iniciaAplicacao()
  if iph.ipAdversario == None:
    return None
  
  ct = CliTabuleiroSocket(iph.obterEnderecoLocalJogo(), iph.obterEnderecoAdversarioJogo())
  cc = CliChatSocket(iph.obterEnderecoLocalChat(), iph.obterEnderecoAdversarioChat())

  # Inicializando o objeto que instanciará o jogo
  try:
    meuJogo = GuiRestaUm(ct, cc)
  except Exception as e:
    print(e)

  # Inicializando a aplicação grafica do jogo
  meuJogo.iniciaAplicacao()

if __name__ == "__main__":
  mainApp()