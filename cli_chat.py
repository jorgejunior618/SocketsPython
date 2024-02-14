import socket
import threading

class CliSocket:
  def __init__(self, endereco_local, endereco_destino):
    self.endereco_destino = endereco_destino
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.sock.bind(endereco_local)

  def receber_mensagens(self):
    while True:
      dados, endereco = self.sock.recvfrom(1024)
      print(f"\n[{endereco}]: {dados.decode()}", end="\n>")

  def enviar_mensagem(self):
    while True:
      mensagem = input(">")
      self.sock.sendto(mensagem.encode(), self.endereco_destino)

  def iniciar(self):
    thread_recebimento = threading.Thread(target=self.receber_mensagens)
    thread_recebimento.daemon = True
    thread_recebimento.start()
    self.enviar_mensagem()

def main():
  endereco_local_servidor = ('localhost', 12345)
  endereco_local_cliente = ('localhost', 54321)

  cliente = CliSocket(endereco_local_cliente, endereco_local_servidor)

  thread_cliente = threading.Thread(target=cliente.iniciar)
  thread_cliente.daemon = True
  thread_cliente.start()

  thread_cliente.join()

if __name__ == "__main__":
  main()
