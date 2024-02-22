import chat as chatService
import jogo as jogoService
from models.cli_tabuleiro import CliTabuleiroSocket
from models.cli_chat import CliChatSocket
from gui_resta_um import GuiRestaUm
import threading

if __name__ == "__main__":
  # Inicializando o socket do cliente do jogador
  ct = CliTabuleiroSocket(('localhost', 1234), ('localhost', 4321))
  cc = CliChatSocket(('localhost', 12345), ('localhost', 54321))

  # Inicializando o objeto que instanciará o jogo
  meuJogo = GuiRestaUm(ct, cc)

  # Inicializando a aplicação grafica do jogo
  meuJogo.iniciaAplicacao()
