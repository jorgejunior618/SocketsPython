'''
  Pacotes utilizados para comunicação via socket
'''
from socket import socket, gethostbyname, gethostname, AF_INET, SOCK_DGRAM

'''
  Pacotes utilizados para as interfaces graficas da aplicação
'''

from tkinter import Tk, StringVar, NW, PhotoImage, Canvas, Listbox
from tkinter.font import Font
from tkinter.ttk import Style, Button, Label, Entry
from time import sleep
from threading import Thread
from pygame import mixer

'''
  Codigo de classe do Socket para uso do chat
'''

class CliChatSocket:
  ''' # class ChatSocket
  Classe com a implementação dos sockets para a comunicação em texto, e as threads de envio e recebimento das mensagens

  ## Parâmetros:
  endereco_local : tuple[str, int]
      tupla contendo a string que representa o IP da maquina atual, e a porta que receberá a comunicação
  endereco_destino : tuple[str, int]
      tupla contendo a string que representa o IP da maquina de destino, e a porta que receberá a comunicação
  '''
  def __init__(self, endereco_local: tuple[str, int], endereco_destino: tuple[str, int]):
    ''' Inicializa o socket com o endereço local fornecido, e guarda o endereço do adversário '''
    self.endereco_destino = endereco_destino
    self.sock = socket(AF_INET, SOCK_DGRAM)
    self.sock.bind(endereco_local)

  def receber_mensagem(self) -> str:
    ''' # receber_mensagem
    Função que escuta a porta do endereço local esperando recebimento da mensagem do adversario

    ## Retorna:
    mensagem : str
        String com a mensagem recebida na comunicação do chat
    '''
    dados, _ = self.sock.recvfrom(1024)
    mensagem = dados.decode()
    return mensagem

  def enviar_mensagem(self, mensagem: str) -> None:
    ''' # enviar_mensagem
    Função que escuta a porta do endereço local esperando recebimento da mensagem do adversario

    ## Parâmetro:
    mensagem : str
        String com a mensagem para envio na comunicação do chat
    '''
    dados = mensagem.encode()
    self.sock.sendto(dados, self.endereco_destino)

'''
  Codigo de classe do Socket para uso do Jogo
'''
class CliTabuleiroSocket:
  '''# class TabuleiroSocket
  Classe com a implementação dos sockets para a comunicação em texto, e as threads de envio e recebimento das mensagens

  ## Parâmetros:
  endereco_local : tuple[str, int]
      tupla contendo a string que representa o IP da maquina atual, e a porta que receberá a comunicação
  endereco_destino : tuple[str, int]
      tupla contendo a string que representa o IP da maquina de destino, e a porta que receberá a comunicação
  '''

  def __init__(self, endereco_local: tuple[str, int], endereco_destino: tuple[str, int]):
    self.jogo = JogoRestaUm()
    self.endereco_destino = endereco_destino
    self.sock = socket(AF_INET, SOCK_DGRAM)
    self.sock.bind(endereco_local)

  def receberTurno(self) -> int:
    ''' # receberTurno
    Função que escuta a porta do endereço local esperando a decisão de turno do adversario

    ## Retorna:
    turno : int
        0 se o adversário decidiu ser o primeiro do jogo e 1 caso contrário
    '''
    turno, _ = self.sock.recvfrom(1024)
    turno = turno.decode()
    return int(turno)

  def definirTurno(self, turno: str):
    ''' # definirTurno
    Função que envia para o endereço destino  a decisão de turno do usuário local

    ## Parâmetros:
    turno : int
        0 se o usuário decidiu ser o primeiro do jogo e 1 caso contrário
    '''
    self.sock.sendto(turno.encode(), self.endereco_destino)

  def receberLance(self) -> bool:
    ''' # receber_lance
    Recebe o lance do adversário via Socket, verifica se foi o sinal de fim de jogo, faz o movimento na 
    estrutura de dados local e retorna se o movimento foi realizado

    ## Retorna:
    continuar : bool
        `False` caso seja recebido o final de fim de jogo, e `True` se o movimento do adversário for registrado
    '''
    dados, _ = self.sock.recvfrom(1024)
    movimento = dados.decode()
    if movimento == "fim":
      return False, False
    if movimento == "resign":
      return False, True

    mover, retirar = self.jogo.recebeMovimento(movimento)
    _, destino = self.jogo.movimentoValido(mover, retirar)
    self.jogo.fazMovimento(mover, retirar, destino)
    return True, False

  def enviarLance(self, movimento: str) -> bool:
    ''' # enviarLance
    Função que escuta a porta do endereço local esperando recebimento do movimento do adversario

    ## Parâmetro:
    movimento : str
        String com o movimento para envio na comunicação do chat
    
    ## Retorno:
    bool
        True caso o movimento/envio foi feito corretamente, false caso seja um movimento inválido
    '''
    if movimento == "fim":
      self.sock.sendto(movimento.encode(), self.endereco_destino)
      return True
    if movimento == "resign":
      self.sock.sendto(movimento.encode(), self.endereco_destino)
      return True

    mover, retirar = self.jogo.recebeMovimento(movimento)
    valido, destino = self.jogo.movimentoValido(mover, retirar)

    if not valido:
      return False

    self.jogo.fazMovimento(mover, retirar, destino)
    self.sock.sendto(movimento.encode(), self.endereco_destino)
    return True

'''
  Classe com as regras de negocio do jogo Resta Um
'''
class JogoRestaUm:
  def __init__(self):
    self.tabuleiro = []
    self.turno = 0

  def reiniciaTabuleiro(self) -> list[list[str]]:
    '''# reiniciaTabuleiro
    Função que retorna um novo tabuleiro de Resta Um

    ## Retorna:
    tabuleiro : list[list[str]]
        objeto que representa um novo tabuleiro com a posição inicial do jogo

    '''
    self.turno = 0
    self.tabuleiro = []
    posicoes = 9

    for i in range(posicoes):
      linha = []
      for j in range(posicoes):
        peca = '*'
        if i == 0 or i == 8 or j == 0 or j == 8:
          peca = ' '
        elif (i < 3 or i > 5) and (j < 3 or j > 5):
          peca = ' '
        if (i == j == 4):
          peca = 'O'
        linha.append(peca)
      self.tabuleiro.append(linha)

  def estaNoFim(self) -> tuple[bool, int]:
    '''# estaNoFim

    Função que verifica e retorna se o tabuleiro ainda possui movimentos a serem realizados,
    quantas peças faltaram ser removidas caso não

    ## Retorna:
    out : tuple[ fimDeJogo : bool, contagem : int ]
        onde: [fimDeJogo] indica se há movimentos válidos e [contagem] a quantidade de peças restantes em caso de fimDeJogo[True] e 0 em caso de fimDeJogo[False]
    '''
    contagemPecas = 0
    for i in range(9):
      linha = "".join(self.tabuleiro[i])
      contagemPecas += linha.count('*')
      coluna = "".join([lin[i] for lin in self.tabuleiro])
      if (linha.find("**O") != -1) or (linha.find("O**") != -1):
        return False, 0
      if (coluna.find("**O") != -1) or (coluna.find("O**") != -1):
        return False, 0
    return True, contagemPecas

# Funções relacionadas aos movimentos e validadações do jogo
  def movimentoValido(self, mover: list[int], retirar: list[int]) -> tuple[bool, list[int]]:
    '''# movimentoValido

    Função que valida se o movimento recebido nos parâmetros é válido e retorna
    o destino da peça que será movida:

    ## Parâmetros:
    mover : list[int]
        indice da peça que será movida de posição
    retirar : list[int]
        indice da peça que será removida do tabuleiro
    tabuleiro : list[list[str]]
        objeto que representa o tabuleiro do jogo atual

    ## Retorna:
    out : tuple[ valido : bool, destino : list[int] ]
        onde: [valido] indica se o movimento recebido pode ser realizado ou não e [destino] é o indice para o qual a peça [mover] deverá ir
    '''

    moverLinha, moverColuna = mover
    retirarLinha, retirarColuna = retirar

    # Verificando se as posições estão dentro do tabuleiro
    if moverLinha > 7 or moverColuna > 7 or retirarLinha > 7 or retirarColuna > 7 or moverLinha < 1 or moverColuna < 1 or retirarLinha < 1 or retirarColuna < 1:
      return False, []

    # Verificando se as posições selecionadas são peças
    if self.tabuleiro[moverLinha][moverColuna] != '*':
      return False, []
    if self.tabuleiro[retirarLinha][retirarColuna] != '*':
      return False, []

    # Caso o movimento seja Horizontal
    if moverLinha == retirarLinha:
      if moverColuna == retirarColuna or abs(moverColuna - retirarColuna) != 1: # Caso as peças selecionadas sejam identicas
        return False, []
      # Caso seja um movimento da esquerda para a direita (->)
      if moverColuna < retirarColuna:
        if self.tabuleiro[retirarLinha][retirarColuna+1] != 'O':
          return False, []
        return True, [retirarLinha,retirarColuna+1]
      # Caso seja um movimento da direita para a esquerda (<-)
      else:
        if self.tabuleiro[retirarLinha][retirarColuna-1] != 'O':
          return False, []
        return True, [retirarLinha,retirarColuna-1]

    # Caso o movimento seja Vertical
    elif moverColuna == retirarColuna:
      if moverLinha == retirarLinha or abs(moverLinha - retirarLinha) != 1: # Caso as peças selecionadas sejam identicas
        return False, []
      # Caso seja um movimento de cima para baixo (\/)
      if moverLinha < retirarLinha:
        if self.tabuleiro[retirarLinha+1][retirarColuna] != 'O':
          return False, []
        return True, [retirarLinha+1,retirarColuna]
      # Caso seja um movimento de baixo para cima (/\)
      else:
        if self.tabuleiro[retirarLinha-1][retirarColuna] != 'O':
          return False, []
        return True, [retirarLinha-1,retirarColuna]
    # Caso as peças não estajam juntas
    else:
      return False, []

  def fazMovimento(self, mover: list[int], retirar: list[int], destino: list[int]):
    '''# fazMovimento

    Função recebe o movimento desejado e retorna o tabuleiro com a jogada realizada:

    ## Parâmetros:
    mover : list[int]
        indice da peça que será movida de posição
    retirar : list[int]
        indice da peça que será removida do tabuleiro
    destino : list[int]
        indice de para onde a peça [mover] deverá ir
    tab : list[list[str]]
        objeto que representa o tabuleiro do jogo atual

    ## Retorna:
    tabuleiro : list[list[str]]
        objeto que representa o tabuleiro com a nova posição depois de ser realizaada a jogada
    '''
    tab = []
    for i in range(9):
      linha = []
      for j in range(9):
        linha.append(self.tabuleiro[i][j])
      tab.append(linha)

    tab[mover[0]][mover[1]], tab[retirar[0]][retirar[1]], tab[destino[0]][destino[1]] = 'O','O' ,'*'

    self.turno = 1 - self.turno
    self.tabuleiro = tab

  def recebeMovimento(self, movimento: str) -> list[list[int]]:
    '''# recebeMovimento
    Função que recebe o input do usuário e retorna os indices indicados

    ## Retorna:
    mover : list[int]
        indice da peça que será movida de posição
    retirar : list[int]
        indice da peça que será removida do tabuleiro
    '''

    indiceLinha = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7}
    mover, retirar = movimento.split(' ')

    mover = [*mover]
    mover[0] = indiceLinha[mover[0]]
    mover[1] = int(mover[1])

    retirar = [*retirar]
    retirar[0] = indiceLinha[retirar[0]]
    retirar[1] = int(retirar[1])
    return mover, retirar

'''
  Classe de apoio pra obtenção do ip local e regras de validade de IP
'''
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

'''
  Codigo para instancia da interface grafica de inserir o ip do adversário
'''
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

'''
  Codigo para instancia da interface grafica do jogo
'''

class GuiRestaUm:
  ''' # RestaUmInterface

  Classe que inicializa uma interface grafica, com `TKinter`, para o jogo Resta Um.

  ## Parâmetros:
    cli_tabuleiro : CliTabuleiroSocket
        O cliente socket ja inicializado que será utilizado para a conexão multiplayer
    '''
  jogada = ""
  pecaDestacada = -1
  meuTurno = -1
  prontoPJogar = False
  turnoVar: StringVar = None
  labelInfoTurno: Label = None
  tagFimJogo = None
  img_tabuleiro = None
  img_peca = None
  img_vazio = None
  img_peca_high = None
  fim_jogo = None
  dictImgs = {}

  def __init__(self, cli_tabuleiro: CliTabuleiroSocket, cli_chat: CliChatSocket):
    '''
    Inicializa a interface grafica do jogo

    ## Parâmetros:
    cli_tabuleiro : CliTabuleiroSocket
        O cliente socket ja inicializado que será utilizado para a conexão multiplayer
    '''
    self.cliTab: CliTabuleiroSocket = cli_tabuleiro
    self.cliChat: CliChatSocket = cli_chat
    self.desistiu = False
    self.cliTab.jogo.reiniciaTabuleiro()
    self.criaComponenteJanela()
    mixer.init()

    GuiRestaUm.fonteText = Font(size=11, family="Trebuchet MS")
    GuiRestaUm.turnoVar = StringVar()
    GuiRestaUm.labelInfoTurno = Label(self.janela, textvariable=GuiRestaUm.turnoVar)
    GuiRestaUm.img_tabuleiro = PhotoImage(file="assets/tabuleiro.png")
    GuiRestaUm.img_peca = PhotoImage(file="assets/peca.png")
    GuiRestaUm.img_vazio = PhotoImage(file="assets/vazio.png")
    GuiRestaUm.img_peca_high = PhotoImage(file="assets/peca_highlight.png")
    GuiRestaUm.fim_jogo = PhotoImage(file="assets/fim_jogo.png")

    GuiRestaUm.dictImgs['peca'] = GuiRestaUm.img_peca.name[-1]
    GuiRestaUm.dictImgs['vazio'] = GuiRestaUm.img_vazio.name[-1]
    GuiRestaUm.dictImgs['destacada'] = GuiRestaUm.img_peca_high.name[-1]
    
    self.criaComponenteTabuleiro()
    self.criaComponenteEstilos()
    self.criaComponentePecas()
    self.criaComponenteTurnos()
    
    self.mensagens: list[str] = []
    self.minhaMensagem = StringVar()
    self.criaComponenteChat()

  @staticmethod
  def reproduzSom(efeito: str):
    ''' ## reproduzSom(efeito)

    Reproduz um efeito sonoro referente ao movimento/ação do jogo

    ## Parâmetro:
    efeito : str
        A ação realizada, gatilho para o efeito sonoro
    '''
    efeitos = {
      'derrota': 'derrota_1',
      'vitoria': 'vitoria_1',
      'movimento': 'movimento_1',
      'mov_erro': 'mov_erro_2',
    }
    arq = f"assets/{efeitos[efeito]}.mp3"
    if mixer.music.get_busy():
      mixer.music.queue(arq)
    else:
      mixer.music.load(arq)

    mixer.music.set_volume(0.7)
    mixer.music.play()

  @staticmethod
  def selecionaPeca(
    x: int,
    y: int,
    tag: int,
    ct: CliTabuleiroSocket
  ) -> tuple[bool, int, bool]:
    ''' # selecionaPeca

    Função que gerencia o clique do usuário nas peças segundo a seguinte lógica:
    - Se nenhuma peça estiver selecionada, seleciona a clicada
    - Se uma peça estiver selecionada eseja um movimento válido, realiza o movimento
    - Se uma peça estiver selecionada e o movimento inválido, seleciona a nova peça

    ## Parâmetros:
    x : int
        indice da linha da peça

    y : int
        indice da coluna da peça

    tag : int
        identificador do componente da peça

    ct : CliTabuleiroSocket
        cli do socket de Jogo

    ## Retorno:
    r : tuple[reposicionar: bool , rmDst: int , movErrado: bool]
        reposicionar: indica se o tabuleiro tem que ser re-renderizado

        removeDestaque: indica o idnetificador que deve ser removido o destaque

        movErrado: indica se o som de movimento errado deve ser reproduzido
    '''
    posicaoJogada = ["","a", "b", "c", "d", "e", "f", "g",""]
    pecaSelecionada = f"{posicaoJogada[x]}{y}"
    removerDestaque = GuiRestaUm.pecaDestacada

    if (removerDestaque == tag):
      GuiRestaUm.jogada = ""
      GuiRestaUm.pecaDestacada = -1
      return False, tag, False
    GuiRestaUm.pecaDestacada = tag

    if len(GuiRestaUm.jogada) == 0:
      GuiRestaUm.jogada = f"{pecaSelecionada}"
      return False, removerDestaque, False

    GuiRestaUm.jogada = f"{GuiRestaUm.jogada} {pecaSelecionada}"
    minhaVez = not ct.enviarLance(GuiRestaUm.jogada)

    if minhaVez:
      GuiRestaUm.pecaDestacada = tag
      GuiRestaUm.jogada = pecaSelecionada
      return False, removerDestaque, True

    GuiRestaUm.jogada = ""
    GuiRestaUm.pecaDestacada = -1
    return True, removerDestaque, False

  def criaComponenteJanela(self):
    ''' # criaComponenteJanela

    Função de criação de componentes: cria a janela raiz da interface gráfica
    '''
    self.janela = Tk()
    self.janela.iconbitmap("./assets/icone.ico")
    self.janela.title("ANTes que Reste Um")
    self.janela.geometry("800x500")
    self.janela.resizable(False, False)

  def criaComponenteEstilos(self):
    ''' # criaComponenteEstilos

    Função de criação de componentes: cria o estilo padrão para os botões da GUI
    '''
    style = Style()
    style.configure(
      "Estilizado.TButton",
        width=6,
        font=GuiRestaUm.fonteText
      )

  def criaComponenteTabuleiro(self):
    ''' # criaComponenteTabuleiro

    Função de criação de componentes: cria o canvas que receberá o tabuleiro e peças e posiciona as peças
    '''
    self.canvas = Canvas(self.janela, width=500, height=500)
    self.canvas.place(x=0, y=0)
    self.canvas.create_image(0,0, anchor=NW, image=GuiRestaUm.img_tabuleiro)

  def criaComponenteTurnos(self, texto: str = "Escolha seu turno"):
    ''' # criaComponenteTurnos

    Função de criação de componentes: cria as labels e botões utilizados para decisão de turnos
    '''
    # fonteText = Font(size=11, family="Trebuchet MS")
    GuiRestaUm.botaoT1 = Button(self.janela, text="1º", command=lambda t=0: self._setTurno(t), style="Estilizado.TButton")
    GuiRestaUm.botaoT2 = Button(self.janela, text="2º", command=lambda t=1: self._setTurno(t), style="Estilizado.TButton")
    GuiRestaUm.labelDecTurno = Label(self.janela, text=texto, font=GuiRestaUm.fonteText)
    
    GuiRestaUm.botaoT1.place(x=520, y=45)
    GuiRestaUm.botaoT2.place(x=590, y=45)
    GuiRestaUm.labelDecTurno.place(x=520, y=15)

  def criaComponentePecas(self):
    ''' # criaComponentePecas

    Função de criação de componentes: cria e posiciona as peças no tabuleiro
    '''
    self.tagPecas = []
    for i in range(1, 8):
      linha = []
      for j in range(1, 8):
        lin = 90 + ((i-1) * 40) + ((i-1) * 5)
        col = 35 + ((j-1) * 50) + ((j-1) * 10)
        tagItem = -1
        if self.cliTab.jogo.tabuleiro[i][j] == '*':
          tagItem = self.canvas.create_image(col, lin, anchor=NW, image=GuiRestaUm.img_peca)
        if self.cliTab.jogo.tabuleiro[i][j] == 'O':
          tagItem = self.canvas.create_image(col, lin, anchor=NW, image=GuiRestaUm.img_vazio)
        self.canvas.tag_bind(
          tagItem,
          "<Button-1>",
          lambda e, x=i, y=j, id=tagItem: self.fazJogada(x, y, id)
        )
        linha.append(tagItem)
      self.tagPecas.append(linha[:])

  def criaComponenteChat(self):
    ''' # criaComponenteChat

    Função de criação de componentes: cria a entrada e componentes do chat do jogo
    '''
    fonteChat = Font(size=11, family="Comic Sans MS")
    GuiRestaUm.variavelMensagens = StringVar(value=self.mensagens)

    GuiRestaUm.lboxMensagens = Listbox(
      self.janela,
      listvariable=GuiRestaUm.variavelMensagens,
      height=12,
      width=29,
      font=fonteChat,
      foreground="#7C3509"
    )
    GuiRestaUm.inputChat = Entry(
      self.janela,
      textvariable=self.minhaMensagem,
      width=20,
      font=fonteChat
    )
    GuiRestaUm.botaoEnviarChat = Button(
      self.janela,
      text="Enviar",
      command=self.chatEnviaMensagem,
      width=8,
      style="Estilizado.TButton"
    )

    GuiRestaUm.lboxMensagens.place(x=520, y=190)
    GuiRestaUm.inputChat.place(x=520, y=460)
    GuiRestaUm.botaoEnviarChat.place(x=715, y=457)

    def enviaMsgEnter(kc):
      if kc == 13: # Pressionou enter
        self.chatEnviaMensagem()
    GuiRestaUm.inputChat.bind("<Key>", lambda e: enviaMsgEnter(e.keycode))

  def reproduzFimDeJogo(self):
    ''' # reproduzFimDeJogo

    Função que cria a thread que  de animação do componente da placa de fim de jogo
    '''
    if GuiRestaUm.tagFimJogo == None:
      GuiRestaUm.tagFimJogo = self.canvas.create_image(75,-330, anchor=NW, image=GuiRestaUm.fim_jogo)
    def desce():
      cont = 0
      for i in range(104):
        alturaAtual = i*3.2 - 330
        balancoAtual = 0
        if GuiRestaUm.meuTurno == -1:
          self.canvas.moveto(GuiRestaUm.tagFimJogo, 75, -330)
          break
        if cont < 20:
          balancoAtual = 0 - cont*2
        elif cont < 56:
          balancoAtual = cont*2 - 78
        elif cont < 82:
          balancoAtual = 144 - cont*2
        elif cont < 98:
          balancoAtual = cont*2 - 180
        else:
          balancoAtual = 210 - cont*2

        self.canvas.moveto(GuiRestaUm.tagFimJogo, 35 + balancoAtual, alturaAtual)
        cont += 1

        sleep(0.025)

    thread_placa = Thread(target=desce, daemon=True)
    thread_placa.start()

  def fazJogada(self, x: int, y: int, tag: int):
    ''' # fazJogada

    Função para ser utilizada no clique das peças do jogo, ativada apenas no turno do jogador,
    identifica a posição selecionada e envia para a função `selecionaPeca` para realizar as funções
    gráficas

    ## Parâmetros:
    x : int
        indice da linha da peça

    y : int
        indice da coluna da peça

    tag : int
        identificador do componente da peça

    ct : CliTabuleiroSocket
        cli do socket de Jogo

    '''
    if self.cliTab.jogo.turno == GuiRestaUm.meuTurno and GuiRestaUm.prontoPJogar:
      pecaID = self.canvas.itemcget(tag, 'image')[-1]
      if pecaID != GuiRestaUm.dictImgs['vazio']:
        reposicionar, rmDst, movErrado = GuiRestaUm.selecionaPeca(x, y, tag, self.cliTab)
        if GuiRestaUm.pecaDestacada != -1:
          self.canvas.itemconfigure(tag, image=GuiRestaUm.img_peca_high)
        if rmDst != -1:
          self.canvas.itemconfigure(rmDst, image=GuiRestaUm.img_peca)

        if reposicionar:
          GuiRestaUm.reproduzSom('movimento')
          self.reposicionaPecas()
        if movErrado:
          GuiRestaUm.reproduzSom('mov_erro')

  def recebeJogadaAdversario(self):
    ''' # recebeJogadaAdversario

    Função para ser inicializada por execução de Threads que controla o recebimento de lances do adversário
    e para quando é dado o sinal de fim de jogo
    '''
    while True:
      try:
        recebeu, advDesistiu = self.cliTab.receberLance()

        if recebeu:
          GuiRestaUm.reproduzSom('movimento')
          self.reposicionaPecas()
        elif advDesistiu:
          self.checaFimDeJogo(desistencia=True)
          break
        else: break
      except:
        print("[Movimento]: nenhuma resposta obtida")

  def setTurnoAdversario(self):
    ''' # setTurnoAdversario

    Função para ser inicializada por execução de Threads que controla o recebimento da decisão
    de turno feita pelo adversário

    Aguarda até receber a mensagem e até o usuário local realizar a sua decisão, e caso as
    respostas entrem em conflito, reposiciona os componentes de decisão de turno
    '''
    while True:
      try:
        turnoAdv = self.cliTab.receberTurno()
        while GuiRestaUm.meuTurno == -1:
          sleep(0.5)

        GuiRestaUm.turnoVar.set("")
        if turnoAdv != GuiRestaUm.meuTurno:
          GuiRestaUm.prontoPJogar = True
          if GuiRestaUm.meuTurno == 0:
            GuiRestaUm.turnoVar.set("Você inicia a partida")
          elif GuiRestaUm.meuTurno == 1:
            GuiRestaUm.turnoVar.set("Seu adversario iniciará a partida")
          GuiRestaUm.botaoDesistencia = Button(self.janela, text="Desisitir", command=self._desistir, style="Estilizado.TButton")
          GuiRestaUm.botaoDesistencia.place(x=520, y=45)
          thread_jogo = Thread(target=self.recebeJogadaAdversario, daemon=True)
          thread_jogo.start()
          break
        else:
          GuiRestaUm.meuTurno = -1
          self.criaComponenteTurnos(texto="Conflito, tentem novamente")
      except:
        print("[Turno]: nenhuma resposta obtida")

  def _setTurno(self, t: int):
    ''' # _setTurno

    Função dos botões de decisão de turno que define o desejo do usuário local de iniciar ou não a partida
    e envia para o adversário para verificação

    ## Parâmetro
    
    t : int (0 or 1)
        0 se o usuario local quiser iniciar a partida, ou 1 caso contrário
    '''
    GuiRestaUm.meuTurno = t
    self.cliTab.definirTurno(f"{t}")
    GuiRestaUm.botaoT1.destroy()
    GuiRestaUm.botaoT2.destroy()
    GuiRestaUm.labelDecTurno.destroy()

    GuiRestaUm.turnoVar.set("Aguardando resposta do seu adversário")
    GuiRestaUm.labelInfoTurno = Label(self.janela, textvariable=GuiRestaUm.turnoVar, font=GuiRestaUm.fonteText)
    GuiRestaUm.labelInfoTurno.place(x=520, y=15)

  def _desistir(self):
    self.desistiu = True
    self.checaFimDeJogo(desistencia=True)
    self.cliTab.enviarLance("resign")

  def reposicionaPecas(self):
    ''' # reposicionaPecas

    Função para realizar a re-renderização da posição das peças no tabuleiro
    '''
    for i in range(1, 8):
      for j in range(1, 8):
        if self.cliTab.jogo.tabuleiro[i][j] == '*':
          self.canvas.itemconfigure(self.tagPecas[i-1][j-1], image=GuiRestaUm.img_peca)
        if self.cliTab.jogo.tabuleiro[i][j] == 'O':
          self.canvas.itemconfigure(self.tagPecas[i-1][j-1], image=GuiRestaUm.img_vazio)
    if GuiRestaUm.meuTurno == self.cliTab.jogo.turno:
      GuiRestaUm.turnoVar.set("Sua vez")
    else:
      GuiRestaUm.turnoVar.set("Vez do adversário")

    self.checaFimDeJogo()

  def checaFimDeJogo(self, desistencia=False):
    ''' # checaFimDeJogo

    Função que verifica se o jogo finalizou, se restou apenas uma peça, e se o usuário
    local venceu ou perdeu a partida

    Em caso de termino da partida, mostra o resultado em tela, inicia a animação de
    fim de jogo e adiciona a opção de jogar novamente
    '''
    terminou, contPecas = self.cliTab.jogo.estaNoFim()
    if terminou or desistencia:
      GuiRestaUm.turnoVar.set("")
      self.reproduzFimDeJogo()
      GuiRestaUm.prontoPJogar = False
      if not desistencia:
        self.cliTab.enviarLance("fim")

      vencedor = False
      if desistencia:
        if not self.desistiu: vencedor = True
      elif contPecas > 1:
        vencedor = self.cliTab.jogo.turno == GuiRestaUm.meuTurno
      else:
        vencedor = self.cliTab.jogo.turno != GuiRestaUm.meuTurno
      fonteResultado = Font(size=18, weight="bold")

      if vencedor:
        if desistencia:
          GuiRestaUm.labelInfoResultado = Label(self.janela,text="Parabéns, você venceu!\nSeu adversario desistiu!",font=fonteResultado)
        elif contPecas == 1:
          GuiRestaUm.labelInfoResultado = Label(self.janela,text="Parabéns, você venceu!\n         Restou Um!",font=fonteResultado)
        else:
          GuiRestaUm.labelInfoResultado = Label(self.janela,text=f"Fim de movimentos\n     Você venceu!\n      Restaram {contPecas}",font=fonteResultado)
        self.reproduzSom("vitoria")
      else:
        if desistencia:
          GuiRestaUm.labelInfoResultado = Label(self.janela,text="Você perdeu :(",font=fonteResultado)
        elif contPecas == 1:
          GuiRestaUm.labelInfoResultado = Label(self.janela,text="Você perdeu :(\n   Restou Um  ",font=fonteResultado)
        else:
          GuiRestaUm.labelInfoResultado = Label(self.janela,text=f"Fim de movimentos\n    Você perdeu :(  \n      Restaram {contPecas}",font=fonteResultado)
        self.reproduzSom("derrota")

      GuiRestaUm.labelInfoResultado.place(x=650, y=65, anchor="center")
      GuiRestaUm.botaoResetaJogo = Button(
        self.janela,
        text="Novo Jogo",
        command=self.resetaJogo,
        style="Estilizado.TButton",
        width=10
      )
      GuiRestaUm.botaoResetaJogo.place(x=650, y=150, anchor="center")
      GuiRestaUm.botaoDesistencia.destroy()

  def resetaJogo(self):
    ''' # resetaJogo

    Função que limpa os componentes de resultado do jogo finalizado, reinicia a
    Thread de escolha de turnos, interrompe a Thread de animação de Fim de Jogo,
    reposiciona e renderiza as peças do tabuleiro e chama a função `criaComponenteTurnos`
    '''
    thread_turno = Thread(target=self.setTurnoAdversario, daemon=True)
    thread_turno.start()

    GuiRestaUm.meuTurno = -1

    self.cliTab.jogo.reiniciaTabuleiro()
    self.reposicionaPecas()
    GuiRestaUm.turnoVar.set("")
    GuiRestaUm.labelInfoResultado.destroy()
    GuiRestaUm.botaoResetaJogo.destroy()
    self.canvas.moveto(GuiRestaUm.tagFimJogo, 75, -330)

    self.criaComponenteTurnos()
  
  def addMensagem(self,identificador: str, msg: str):
    ''' # addMensagem

    Função que recebe uma nova mensagem registrada e a renderiza no componente
    da conversa do chat

    ## Parâmetros:
    
    identificador : str
        Identifica se a mensagem é do usuário local ou do adversário
    msg : str
        O texto da mensagem a ser exibida
    '''
    self.mensagens.append(f"{identificador}: {msg}")
    qtdMsg = len(self.mensagens) # 4
    lm = list(reversed(self.mensagens))
    mensagens: list[str] = []
    for i in range(11, -1, -1):
      if qtdMsg > i:
        mensagens.append(lm[i])
      else :
        mensagens.append("")
    GuiRestaUm.variavelMensagens.set(mensagens)
    if qtdMsg > 12:
      qtdMsg = 12
    for i in range(11, 11-qtdMsg, -1):
      if mensagens[i].startswith("Voc"):
        GuiRestaUm.lboxMensagens.itemconfigure(i, background='#F0F0FF')
      else:
        GuiRestaUm.lboxMensagens.itemconfigure(i, background='#FFF')

  def chatRecebeMensagem(self):
    ''' # chatRecebeMensagem

    Função para ser inicializada por execução de Threads que controla o recebimento de
    mensagens do chat entre os usuários
    '''
    while True:
      try:
        msg = self.cliChat.receber_mensagem()
        self.addMensagem("Adversário", msg)
      except:
        print("[Rec. msg]: nenhuma resposta obtida")

  def chatEnviaMensagem(self):
    ''' # chatEnviaMensagem

    Função que captura o texto digitado pelo usuário e envia para o adversário
    '''
    try:
      msg = self.minhaMensagem.get()
      if len(msg) > 0:
        self.addMensagem("Você", msg)
        self.minhaMensagem.set("")
        self.cliChat.enviar_mensagem(msg)
    except:
      print("[Env. Msg.]: nenhuma resposta obtida")

  def iniciaAplicacao(self):
    '''# iniciaAplicacao
    Inicia as Threads de recebimento de decisão de turnos do Jogo e de
    recebimento de mensagens do chat, e inicializa a interface gráfica
    '''
    # Criando a thread que recebe a escolha do turno do adversário via Socket
    thread_turno = Thread(target=self.setTurnoAdversario, daemon=True)
    thread_turno.start()

    # Criando a thread que recebe as mensagens do adversário via Socket
    thread_chat = Thread(target=self.chatRecebeMensagem, daemon=True)
    thread_chat.start()

    self.janela.mainloop()

def mainApp():
  # # Inicializando o socket do cliente do jogador
  # print("Se tento criar um executavel sem esse console,")
  # print("o arquivo é acusado como virus")
  # print(";-;")

  # iph = IPHelper() # para o jogo em diferentes maquinas
  # gdefAdv = GuiDefineAdversario(iph)
  # gdefAdv.iniciaAplicacao()
  # if iph.ipAdversario == None:
  #   return None
  
  # ct = CliTabuleiroSocket(iph.obterEnderecoLocalJogo(), iph.obterEnderecoAdversarioJogo())
  # cc = CliChatSocket(iph.obterEnderecoLocalChat(), iph.obterEnderecoAdversarioChat())

  try: # permitindo apenas duas instancias do jogo em uma mesma maquina
    ct = CliTabuleiroSocket(('localhost', 4321), ('localhost', 1234))
    cc = CliChatSocket(('localhost', 54321), ('localhost', 12345))
  except:
    ct = CliTabuleiroSocket(('localhost', 1234), ('localhost', 4321))
    cc = CliChatSocket(('localhost', 12345), ('localhost', 54321))

  try: # Inicializando o objeto que instanciará o jogo
    meuJogo = GuiRestaUm(ct, cc)
  except Exception as e:
    print(e)

  meuJogo.iniciaAplicacao() # Inicializando a aplicação grafica do jogo

if __name__ == "__main__":
  mainApp()