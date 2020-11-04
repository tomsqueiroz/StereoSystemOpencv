# Documentacção do Trabalho 1 de Princípios de Visão Computacional

## Diretórios

É essencial para o bom funcionamento dos scripts que os próprios 
estejam em um mesmo diretório, junto às pastas contendo os datasets
de Calibração 1 e 2.

Cada um dos scripts acessa, automaticamente, as pastas necessárias 
de acordo com o PWD respectivo.

## Scripts

### intrinsicsCalibration

Script responsável por abrir os datasets de Calibração 1 e 2, dis-
ponibilizados pelo Professor e, a partir deles, determinar os parâ-
metros intrínsecos de cada câmera, i.e matrizes de calibração e ve-
tores de distorção.

O resultado será exibido no console e, também, salvo em arquivo na
extensão .json

### extractFrames

Script responsável por abrir os vídeos camera1.webm e camera2.webm
e, avançar frame por frame, até frames selecionados especificamente
para calibração de extrínsecos (pontos A, B, C e D visíveis). Feito
isso, remove a distorção radial de cada um deles e salva em pastas
de nome Camera1Undistorted e Camera2Undistorted.

### extrinsicsCalibration

Script responsável por abrir os frames selecionados anteriormente,
solicitar ao usuário cliques na tela para definição dos pontos a se-
rem usados na calibração. Feito isso, determina os parâmetros ex-
trínsecos da câmera, retornando os vetores de rotação e translação
e, por fim, a posição da câmera no sistema.

### disparityMap



### worldCoordinates

Script responsável por rodar o algoritmo de tracking para ambas as
câmeras. O primeiro frame é congelado e, via teclado, o usuário a-
vança, frame a frame, com a tecla N. Ao chegar no primeiro frame 
em que o objeto seja visível, deve-se pressionar S e será invocada
a rotina de definição da bounding box, via mouse. Deve-se clicar no
exato ponto a ser rastreado e, a partir dele, definir um quadrilá-
tero. 

Recomenda-se que essa zona de interesse não englobe trechos da ima-
gem além do lego a ser rastreado, e.g trechos do fundo da cena. Da
mesma forma, zonas de interesse demasiadamente pequenas também ten-
dem a gerar resultados ineficientes, uma vez que o tracker se perde
facilmente.

Caso o usuário perceba que a bounding box se afastou muito do ponto,
é possível redefini-la pressionando S mais uma vez.

No exato momento em que o objeto sair de cena, e o tracker perder
sua referência, o frame congela novamente. Cabe ao usuárioa avançar,
mais uma vez, pressionando N, até que o objeto esteja visível nova-
mente. Define-se mais uma vez a bounding box, através da tecla S.

Caso deseje redefinir a bounding box durante sua seleção, o usuário
deve apertar ESC. Caso deseje abortar, deve pressionar Q, mas tendo
ciência de que o processo falhará. Recomenda-se seu uso apenas para
reiniciar a execução.

Note que, para bom funcionamento do algoritmo, o usuário deve ras-
trear o mesmo objeto na câmera 1 e 2.

Verificou-se que a câmera 2 tende a apresentar mais problemas duran-
te o rastreamento. Por isso, ela é apresentada primeiro na execução,
facilitando caso seja necessário reiniciar o processo.

Uma vez que os tenha se obtido as posições do objeto nas duas câme-
ras, seleciona-se os frames que são sincronizados entre elas e en-
tão, uma rotina calcula as coordenadas para cada instante de tempo.

Por fim, os valores encontrados são salvos em output.json.

### plot

Script que acessa o arquivo .json gerado pelo script anterior e plo-
ta as coordenadas X, Y e Z com relação ao tempo. O gráfico é, então,
exibido na tela e pode ser salvo no comando próprio da GUI do pyplot
caso seja de interesse do usuário.

### trabalho1