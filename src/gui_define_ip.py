from tkinter import Tk, StringVar
from tkinter.font import Font
from tkinter.ttk import Style, Button, Label, Entry
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
    self.janela.iconbitmap("./assets/icone.ico")
    self.janela.title("ANTes que Reste Um - definir adversário")
    self.janela.geometry("270x115")
    self.janela.resizable(False, False)

  def criaComponenteEstilos(self):
    ''' # criaComponenteEstilos

    Função de criação de componentes: cria o estilo padrão para os botões e fontes da GUI
    '''
    self.fonteGeral = Font(size=12, family="Trebuchet MS")
    self.fonteErro = Font(size=9, family="Trebuchet MS")

    style = Style()
    style.configure(
      "Estilizado.TButton",
        width=6,
        font=self.fonteGeral
      )

  def criaComponenteIP(self):
    ''' # criaComponenteIP

    Função de criação de componentes: cria a entrada e componentes para
    receber o IP do jogador adversário
    '''
    self.varIP = StringVar()
    self.varValidadeIP = StringVar()

    Label(self.janela, text="Digite o IP do seu adversário:", font=self.fonteGeral).place(x=20, y=20)

    self.inputIP = Entry(self.janela, textvariable=self.varIP, width=16, font=self.fonteGeral)
    self.botVerifIP = Button(self.janela, text="Enviar", command=self.recebeEnderecoIP, style="Estilizado.TButton")
    self.labelIPValido = Label(self.janela, textvariable=self.varValidadeIP, font=self.fonteErro, foreground="#F03131")

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
    ''' # recebeEnderecoIP

    Função que captura o texto digitado na entrada e valida o IP informado
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
    '''# iniciaAplicacao
    Inicializa a janel da interface gráfica para receber o IP
    '''
    self.janela.mainloop()
