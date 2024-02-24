from models.cli_tabuleiro import CliTabuleiroSocket
from models.cli_chat import CliChatSocket
from gui_resta_um import GuiRestaUm
from ip_helper import IPHelper
from gui_define_ip import GuiDefineAdversario

def mainApp():
  # Inicializando o socket do cliente do jogador
  iph = IPHelper()
  gdefAdv = GuiDefineAdversario(iph)
  gdefAdv.iniciaAplicacao()
  if iph.ipAdversario == None:
    return None
  
  print("CliJogo: ",iph.defineEnderecoLocalJogo(),iph.defineEnderecoAdversarioJogo(),)
  print("CliChat: ",iph.defineEnderecoLocalChat(),iph.defineEnderecoAdversarioChat(),)

  ct = CliTabuleiroSocket(iph.defineEnderecoLocalJogo(), iph.defineEnderecoAdversarioJogo())
  cc = CliChatSocket(iph.defineEnderecoLocalChat(), iph.defineEnderecoAdversarioChat())

  # Inicializando o objeto que instanciará o jogo
  meuJogo = GuiRestaUm(ct, cc)

  # Inicializando a aplicação grafica do jogo
  meuJogo.iniciaAplicacao()


if __name__ == "__main__":
  mainApp()