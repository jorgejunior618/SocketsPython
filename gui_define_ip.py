from tkinter import *
from tkinter import font
from tkinter import ttk
import threading
from ip_helper import IPHelper

class GuiDefineAdversario:
  ''' # RestaUmInterface

  Classe que inicializa uma interface grafica, com `TKinter`, para o jogo Resta Um.

  ## Parâmetros:
    cli_tabuleiro : CliTabuleiroSocket
        O cliente socket ja inicializado que será utilizado para a conexão multiplayer
    '''
  ip_adversario = ""
  def __init__(self, validador: IPHelper):
    '''
    Inicializa a interface grafica do jogo

    ## Parâmetros:
    cli_tabuleiro : CliTabuleiroSocket
        O cliente socket ja inicializado que será utilizado para a conexão multiplayer
    '''
    self.validador = validador

    self.criaComponenteJanela()
    self.criaComponenteEstilos()
    self.criaComponenteIP()

  def criaComponenteJanela(self):
    ''' # criaComponenteJanela

    Função de criação de componentes: cria a janela raiz da interface gráfica
    '''
    self.janela = Tk()
    self.janela.title("Resta um - definir adversário")
    self.janela.geometry("270x115")
    self.janela.resizable(False, False)

  def criaComponenteEstilos(self):
    ''' # criaComponenteEstilos

    Função de criação de componentes: cria o estilo padrão para os botões da GUI
    '''
    self.fonteGeral = font.Font(size=12, family="Trebuchet MS")
    self.fonteErro = font.Font(size=9, family="Trebuchet MS")

    style = ttk.Style()
    style.configure(
      "Estilizado.TButton",
        width=6,
        font=self.fonteGeral
      )

  def criaComponenteIP(self):
    ''' # criaComponenteChat

    Função de criação de componentes: cria a entrada e componentes do chat do jogo
    '''
    self.varIP = StringVar()
    self.varValidadeIP = StringVar()

    ttk.Label(self.janela, text="Digite o IP do seu adversário:", font=self.fonteGeral).place(x=20, y=20)

    self.inputIP = ttk.Entry(self.janela, textvariable=self.varIP, width=16, font=self.fonteGeral)
    self.botVerifIP = ttk.Button(self.janela, text="Enviar", command=self.recebeEnderecoIP, style="Estilizado.TButton")
    self.labelIPValido = ttk.Label(self.janela, textvariable=self.varValidadeIP, font=self.fonteErro, foreground="#F03131")

    self.inputIP.place(x=20, y=52)
    self.botVerifIP.place(x=170, y=50)
    self.labelIPValido.place(x=20, y=85)

    def bindEnter(kc):
      if len(self.varValidadeIP.get()) > 0:
        self.varValidadeIP.set("")
      if kc == 13: # Pressionou enter
        self.recebeEnderecoIP()
    self.inputIP.bind("<Key>", lambda e: bindEnter(e.keycode))

  def recebeEnderecoIP(self):
    ''' # chatEnviaMensagem

    Função que captura o texto digitado pelo usuário e envia para o adversário
    '''
    try:
      ip = self.varIP.get()
      if self.validador.ipValido(ip):
        self.validador.setIpAdversario(ip)
        self.janela.destroy()
      else:
        self.varValidadeIP.set("IP inválido, tente novamente")
    except:
      print("[Env. Msg.]: nenhuma resposta obtida")

  def iniciaAplicacao(self):
    self.janela.mainloop()
