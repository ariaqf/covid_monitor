# Estudos Preditivos da COVID-19 com Python

## Objetivo
Esse projeto tem por objetivo prever e avaliar a evolução do COVID-19 no Brasil, usando dados comparativos com os outros países do mundo.

## Bibliotecas necessárias
Os módulos essenciais para esse projeto são o numpy e o sci-kit-learn.

## Metodologia
A primeira avaliação que faremos será baseada em utilizar os dados de mortes e infecções totais e diárias e os aproximar das curvas respectivas:

### Mortes e infecções totais 
Serão aproximadas para uma "curva S" ou seja com a função logística. Países que estiverem com uma maior proximidade com a função serão utilizados para treinar o software de regressão para permitir que esse avalie o momento atual do Brasil e faça uma previsão.

Iremos pegar os países cuja curva já se aproximou da curva logística e validar qual o limiar do erro de regressão que separa os países que já terminaram a curva dos demais. Assim, em seguida usaremos esses para treinar um modelo que irá estimar valores futuros para o Brasil.

