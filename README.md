# <img src="icone.ico" alt="Icone da aplicação" title="ANTes que reste uma" width=50/> ANTes que reste uma <img src="https://img.shields.io/badge/py-blue?logo=python&logoColor=ffdd54"/>

Jogo de tabuleiro "Resta Um" - Multiplayer

## Como jogar
### Definição do adversário
Ao abrir o jogo abrirá uma tela (abaixo) onde será pedido para você informar o endereço de IP do computador que irá ser seu adversário, entre com o IP no formato "255.255.255.255" e clique em "Enviar"

<img src="demo/entrada_IP.jpg" alt="Tela de entrada de IP" title="ANTes que reste uma - Endereço do adversário" width=250/>

Caso o IP iformado seja válido, seguiremos para a proxima tela

### Gameplay
Na parte inferior direita da tela há uma entrada de texto, onde se pode enviar mensagens para o adversário.

Na caixa acima, é possivel observar o historico de conversas com o adversário.

Use o chat para decidir com o adversário que irá iniciar o jogo, e segundo o uqe decidirem, clique no Botão que representa a sua decisão (parte superior a direita, "1º" caso você comece ou "2º" caso contrário), o jogo so iniciará quando as respostas de ambos sejam compativeis.

<img src="demo/tabuleiro_1.jpg" alt="Tela inicial da gameplay" title="ANTes que reste uma - Jogo Multiplayer" width=700/>

Após decidirem quem irá iniciar a partida, as peças do tabuleiro estarão disponíveis para a pessoa do turno atual realizar a jogada.
Para jogar clique na peça que voce deseja movimentar, ela será selecionada (caso queira remover a seleção basta clicar novamente na mesma peça), em seguida clique na peça que deseja remover.
O turno só será passado para o próximo quando uma jogada válida for realizada.

<img src="demo/tabuleiro_2.jpg" alt="Tabuleiro com uma peça selecionada" title="ANTes que reste uma - Jogo Multiplayer" width=350/>
<img src="demo/tabuleiro_3.jpg" alt="Tabuleiro após uma jogada ser realizada" title="ANTes que reste uma - Jogo Multiplayer" width=350/>

### Fim de Jogo
O jogo acaba quando resta apenas uma peça no tabuleiro, ou quando não é ais possivel realizar jogadas. Ao clicar no botão "Novo Jogo" a fase de decisão de turnos será iniciada novamente para iniciar uma nova partida.

#### Condições de vitória
- Vence aquele realiza a jogada em que resta apenas uma peça no tabuleiro.
- Perde o jogador que realizar a jogada em que não é mais possível continuar o jogo e restar mais de uma peça no tabuleiro.

<img src="demo/tabuleiro_4.jpg" alt="Tabuleiro após o jogo finalizar" title="ANTes que reste uma - Jogo Multiplayer" width=700/>
