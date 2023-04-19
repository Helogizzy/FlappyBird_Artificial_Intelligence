# FlappyBird_Artificial_Intelligence

>Colaboradores: [Eduarda Elger](https://github.com/EduardaElger), [Ellen Bonafin](https://github.com/EllenBonafin), [Heloisa Alves](https://github.com/Helogizzy) e [Pedro Zoz](https://github.com/Pfzoz)

## Sobre o trabalho
Consiste em um jogo de FlappyBird onde uma inteligência artificial controla o passáro. 

## Sobre o código
### Main.py
O código apresenta funções sobre o jogo em si, tais como: 
- criação dos objetos do jogo;
- função de pulo do pássaro;
- função para a movimentação do pássaro; 
- ângulo do pássaro;
- função de desenho do pássaro e efeito visual;
- função para o cano;
- função para o chão;
- função para desenhar a tela do jogo.

### Agbird.py
Aqui estão todas as implentações do comportamento da IA, a sua construção foi feita a partir de um algoritmo genético junto com uma rede neural. O cruzamento dos indivíduos são feitos somente com os genes dos melhores pássaros. 

## Sobre o programa
- São utilizados 100 pássaros a cada geração.
- A IA decide qual é o melhor pássaro da geração através do tempo que ele permanece vivo.
- Todos os pássaros que vão em direção a parte superior e inferior do cenário são dados como mortos.
- Para fim de desafio foi implementada uma máquina de estado onde a cada 5 pontuações a velocidade aumenta gradativamente.
