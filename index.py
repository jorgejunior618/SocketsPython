import chat as chatService
import jogo as jogoService
from models.cli_tabuleiro import CliTabuleiroSocket
from gui_resta_um import GuiRestaUm
import threading

if __name__ == "__main__":
  # Inicializando o socket do cliente do jogador
  ct = CliTabuleiroSocket(('localhost', 1234), ('localhost', 4321))

  # Inicializando o objeto que instanciará o jogo
  meuJogo = GuiRestaUm(ct)

  # Criando a thread que recebe a jogada do adversário via Socket
  thread_jogo = threading.Thread(target=meuJogo.recebeJogadaAdversario)
  thread_jogo.daemon = True
  thread_jogo.start()

  # Inicializando a aplicação grafica do jogo
  meuJogo.iniciaAplicacao()
