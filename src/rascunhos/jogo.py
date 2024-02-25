import threading
from models.cli_chat import CliChatSocket

def threadRecebimentoMensagens(cli: CliChatSocket):
  while True:
    try:
      msg = cli.receber_mensagem()
      print(f"\n[recebido]: {msg}", end="\n> ")
    except:
      print("[Rec. msg]: falha")

def envioMensagens(cli: CliChatSocket):
  while True:
    msg = input(">")

    try:
      cli.enviar_mensagem(msg)
    except:
      print("[Env. msg]: falha")

def iniciaChat():
  endereco_local = ('localhost', 4321)
  endereco_destino = ('localhost', 1234)

  chat = CliChatSocket(endereco_local, endereco_destino)

  thread_chat = threading.Thread(target=threadRecebimentoMensagens, args=(chat,))
  thread_chat.daemon = True
  thread_chat.start()
  envioMensagens(chat)

if __name__ == "__main__":
  iniciaChat()
