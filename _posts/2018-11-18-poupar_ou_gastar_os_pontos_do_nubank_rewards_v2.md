---
layout: post
title: "Poupar ou Gastar os Pontos do NuBank Rewards? -V2"
date: 2018-12-24 11:39:13 -0200
categories:
    - jupyter notebook
---

# Poupar ou Gastar os Pontos do NuBank Rewards? - UPDATE

Uma versão anterior deste artigo verificou uma disparidade na valorização dos pontos do NuBank Rewards por tipo de compra - cada ponto valia aproximadamente 0,77 centavos de real. Desde o feriado de 15 de novembro de 2018, [o NuBank normalizou a valorização de todos os pontos em 1 centavo de real - 100 pontos para cada real](https://blog.nubank.com.br/produtos/novidades-do-nubank-rewards/) na maioria das compras, e 1,25 centavos de real por ponto no caso de compras de passagens aéreas (80 pontos para cada real).
Devido a isso, muitos ajustes tiveram de ser feitos neste artigo.

## O que é o programa NuBank Rewards

O Rewards é um programa de recompensas por fidelidade do uso do cartão NuBank, um cartão de crédito sem anuidade de um dos primeiros bancos digitais do Brasil.

No NuBank Rewards, cada real que você gasta no cartão NuBank vale um ponto. Estes pontos nunca expiram e podem ser trocados por descontos na sua fatura do cartão de crédito NuBank no valor de compras já efetuadas com o cartão.
Ou seja, você usa seus pontos para apagar uma cobrança de algo de comprou da sua fatura, mesmo depois da compra já ter sido paga.

O programa NuBank rewards não é gratuito - existe uma cobrança mensal de R\$ 19,90 para todos os participantes do programa (ou de R\$ 190,00 anuais)

É importante ressaltar que a quantidade de pontos que você precisa para apagar uma compra típica é a mesma que a quantidade de centavos na compra - cada ponto vale 1 centavo, exceto no caso de passagens aéreas, em que cada ponto vale 1,25 centavos.

**Ou seja, os pontos do NuBank Rewards são 25% mais valiosos para uso em VÔOS do que para uso em outros convênios, com exceção do Spotify**


## O NuBank Rewards vale a pena?

Para saber se o programa vale a pena, podemos pensar o valor descontado da fatura como o rendimento de um investimento. Para que esse investimento valha a pena, o rendimento tem que superar outros investimentos de investimento mínimo, liquidez e risco similares.

- O Investimento Mínimo (mínima quantidade de reais necessária para fazer o investimento) do Nubank Rewards é de R\$ 19,90, o valor da mensalidade. Também serão feitos cálculos considerando o pagamento anual de R\$ 190,00.
- A Liquidez do Nubank Rewards não é diretamente comparável a liquidez da Caderneta de Poupança uma vez que os "rendimentos" somente podem ser usados para abater valores da fatura, mas tal abatimento afeta instantaneamente seu limite de crédito. Para esta análise, considero que os rendimentos da poupança, de fundos de investimento e do NuBank Rewards só são mensuraveis no momento do pagamento da fatura, ou seja, com liquidez em uma certa data do mês.
- O Risco de Mercado (risco de variação dos preços por forças de mercado) do NuBank Rewards é nulo, já que não há um fator de mercado que afete a relação de conversão entre os pontos do programa e as compras efetuadas. Para esta análise, consideraremos nulo o risco de mercado da Caderneta de Poupança.
- O Risco de Default do NuBank Rewards é o risco do banco NuBank quebrar. Para esta análise, consideraremos este e outros riscos técnicos negligíveis.
- Os elementos apagados da fatura do NuBank Rewards não são tributáveis pelo Imposto de Renda

Então vamos assumir que o investimento mínimo do NuBank Rewards seja investido em um fundo, que tem imposto de renda, ou numa Caderneta de Poupança, que não tem imposto de renda.

- Rendimento da Caderneta de Poupança: 6,5% ao ano, 0,00% de Imposto de Renda
- Rendimento do Fundo Fictício FicSAFE: 9,15% ao ano, 12,50% de Imposto de Renda
- Rendimento do Fundo Fictício FicRISK: 19,35% ao ano, 20,00% de Imposto de Renda

Obs: assumo que os fundos fictícios FicSAFE e FicRISK também tem investimento mínimo de R\$ 19,90


```python
def rendimento_aplicacao_regular(meses, valor_aplicacao_regular, rendimento_anual, aliquota_ir):
    lista_periodos_meses = list(range(meses+1))[1:]
    lista_periodos_meses.reverse()
    def _rendimento_ajustado(meses):
        anos = meses/12
        rend = (1+rendimento_anual)**anos
        ir = (rend-1)*aliquota_ir
        return rend - ir
    return sum([
        valor_aplicacao_regular * _rendimento_ajustado(m)
        for m in lista_periodos_meses
    ])

import pandas as pd

df_rendimentos_comparaveis = pd.DataFrame({
    'Mês': [1, 2, 3, 4, 6, 9, 12, 15, 18, 24, 30, 36, 42, 48]
})
df_rendimentos_comparaveis.loc[:, 'Investimento'] = df_rendimentos_comparaveis['Mês'] * 19.90

df_rendimentos_comparaveis.loc[:, 'Poupança (M)'] = df_rendimentos_comparaveis['Mês'].apply(
    lambda m: rendimento_aplicacao_regular(m, 19.90, 0.065, 0))
df_rendimentos_comparaveis.loc[:, 'Poupança (R%)'] = \
    df_rendimentos_comparaveis['Poupança (M)'] / df_rendimentos_comparaveis['Investimento']

df_rendimentos_comparaveis.loc[:, 'FicSAFE (M)'] = df_rendimentos_comparaveis['Mês'].apply(
    lambda m: rendimento_aplicacao_regular(m, 19.90, 0.0915, 0.125))
df_rendimentos_comparaveis.loc[:, 'FicSAFE (R%)'] = \
    df_rendimentos_comparaveis['FicSAFE (M)'] / df_rendimentos_comparaveis['Investimento']

df_rendimentos_comparaveis.loc[:, 'FicRISK (M)'] = df_rendimentos_comparaveis['Mês'].apply(
    lambda m: rendimento_aplicacao_regular(m, 19.90, 0.1935, 0.2))
df_rendimentos_comparaveis.loc[:, 'FicRISK (R%)'] = \
    df_rendimentos_comparaveis['FicRISK (M)'] / df_rendimentos_comparaveis['Investimento']

df_rendimentos_comparaveis.round(2)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Mês</th>
      <th>Investimento</th>
      <th>Poupança (M)</th>
      <th>Poupança (R%)</th>
      <th>FicSAFE (M)</th>
      <th>FicSAFE (R%)</th>
      <th>FicRISK (M)</th>
      <th>FicRISK (R%)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>19.9</td>
      <td>20.00</td>
      <td>1.01</td>
      <td>20.03</td>
      <td>1.01</td>
      <td>20.14</td>
      <td>1.01</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>39.8</td>
      <td>40.11</td>
      <td>1.01</td>
      <td>40.18</td>
      <td>1.01</td>
      <td>40.51</td>
      <td>1.02</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>59.7</td>
      <td>60.33</td>
      <td>1.01</td>
      <td>60.47</td>
      <td>1.01</td>
      <td>61.13</td>
      <td>1.02</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>79.6</td>
      <td>80.65</td>
      <td>1.01</td>
      <td>80.88</td>
      <td>1.02</td>
      <td>82.00</td>
      <td>1.03</td>
    </tr>
    <tr>
      <th>4</th>
      <td>6</td>
      <td>119.4</td>
      <td>121.62</td>
      <td>1.02</td>
      <td>122.11</td>
      <td>1.02</td>
      <td>124.49</td>
      <td>1.04</td>
    </tr>
    <tr>
      <th>5</th>
      <td>9</td>
      <td>179.1</td>
      <td>183.88</td>
      <td>1.03</td>
      <td>184.95</td>
      <td>1.03</td>
      <td>190.17</td>
      <td>1.06</td>
    </tr>
    <tr>
      <th>6</th>
      <td>12</td>
      <td>238.8</td>
      <td>247.13</td>
      <td>1.03</td>
      <td>249.02</td>
      <td>1.04</td>
      <td>258.28</td>
      <td>1.08</td>
    </tr>
    <tr>
      <th>7</th>
      <td>15</td>
      <td>298.5</td>
      <td>311.38</td>
      <td>1.04</td>
      <td>314.34</td>
      <td>1.05</td>
      <td>328.93</td>
      <td>1.10</td>
    </tr>
    <tr>
      <th>8</th>
      <td>18</td>
      <td>358.2</td>
      <td>376.65</td>
      <td>1.05</td>
      <td>380.94</td>
      <td>1.06</td>
      <td>402.24</td>
      <td>1.12</td>
    </tr>
    <tr>
      <th>9</th>
      <td>24</td>
      <td>477.6</td>
      <td>510.32</td>
      <td>1.07</td>
      <td>518.09</td>
      <td>1.08</td>
      <td>557.30</td>
      <td>1.17</td>
    </tr>
    <tr>
      <th>10</th>
      <td>30</td>
      <td>597.0</td>
      <td>648.26</td>
      <td>1.09</td>
      <td>660.71</td>
      <td>1.11</td>
      <td>724.49</td>
      <td>1.21</td>
    </tr>
    <tr>
      <th>11</th>
      <td>36</td>
      <td>716.4</td>
      <td>790.61</td>
      <td>1.10</td>
      <td>809.05</td>
      <td>1.13</td>
      <td>904.94</td>
      <td>1.26</td>
    </tr>
    <tr>
      <th>12</th>
      <td>42</td>
      <td>835.8</td>
      <td>937.52</td>
      <td>1.12</td>
      <td>963.36</td>
      <td>1.15</td>
      <td>1099.86</td>
      <td>1.32</td>
    </tr>
    <tr>
      <th>13</th>
      <td>48</td>
      <td>955.2</td>
      <td>1089.13</td>
      <td>1.14</td>
      <td>1123.90</td>
      <td>1.18</td>
      <td>1310.60</td>
      <td>1.37</td>
    </tr>
  </tbody>
</table>
</div>



Para que o NuBank Rewards valha a pena, o valor descontado da fatura deveria ser maior do que a rentabilidade de uma das alternativas acima no mesmo periodo.

Ou seja, em 3 anos (36 meses), se o valor total descontado da minha fatura for:
- MAIOR QUE R\$ 74,21 - valeu mais a pena que a poupança.
- MAIOR QUE R\$ 92,65 - Valeu mais a pena que a poupança e o fundo FicSAFE
- MAIOR QUE R\$ 188,54 - Valeu mais a pena que a poupança e os dois fundos

Utilizando o pior caso do valor dos pontos do NuBank Rewards (1 centavos/ponto), seriam necessários 18854 pontos para descontar compras que totalizem R\$ 188,54. Seriam necessários 90494 pontos no total, para descontar também os R\$ 716,40 pagos como mensalidade para programa.

**Assim, seria necessário que o titular do cartão NuBank gaste no mínimo R\$ 90.494,00 reais ao longo de três anos, ou R\$ 2.513,73 por mês. O valor de desconto na fatura mensal seria de R\$ 25,13, totalizando uma fatura de R\$ 2.488,60**

**Numa estimativa mais concervadora, seriam necessários 80905 pontos, R\$ 2.247,37 gastos por mês para uma fatura de R\$ 2.224,90 após o desconto de R\$ 22,47**

## Qual a melhor forma de usar os pontos do NuBank Rewards?

O ideal é priorizar os pontos para uso em compras de vôos, onde os pontos valem 25% a mais. Contudo, vôos tendem a ser compras mais esporádicas e de maior volume unitário, o que significa que é necessário uma maior quantidade de pontos acumulados para poder descontá-las da fatura.

É melhor conservar os pontos, acumulando para uso nas compras de voos, ou gastá-los imediatamente?

A vantagem de utilizar os pontos imediatamente é de liberar recursos que poderiam ser melhor investidos. A vantagem de acumular os pontos é que os mesmos seriam mais valorizados quando utilizados para descontar uma compra de voos.

Portanto, o custo de acumular os pontos é equivalente ao rendimento de uma aplicação na qual o valor dos pontos poderia ter sido investido. Vale a pena guardar os pontos quando o custo de acumulá-los é menor que o benefício dos mesmos.

Dada a natureza esporádica e variada das compras de vôos, prefiro calcular os custos de acumulação de pontos necessários para cada compra.

Contudo, é importante lembrar que a taxa de conversão de pontos para o caso de compras de vôos é de 80 pontos para cada real. Assim, uma compra de R\$ 1.000,00 pode ser apagada com 80000 pontos.

Assim sendo, assumindo um gasto mensal de R\$ 3.300,00, e uma compra de voo de R\$ 1.000,00:


```python
pontos_mensais = 3300
valor_compra = 1000

df_rendimentos_acumulo = pd.DataFrame({
    'Mês': list(range(41))[1:]
})
df_rendimentos_acumulo.loc[:, 'Pontos Gerados'] = df_rendimentos_acumulo['Mês'] * pontos_mensais

df_rendimentos_acumulo.loc[:, 'Valor (Uso Imediato - U.I.)'] = df_rendimentos_acumulo['Mês'].apply(
    lambda m: rendimento_aplicacao_regular(m, pontos_mensais/100.0, 0.0, 0))


df_rendimentos_acumulo.loc[:, 'U.I. (Poupanca)'] = df_rendimentos_acumulo['Mês'].apply(
    lambda m: rendimento_aplicacao_regular(m, pontos_mensais/100.0, 0.065, 0))


df_rendimentos_acumulo.loc[:, 'U.I. (FicSAFE)'] = df_rendimentos_acumulo['Mês'].apply(
    lambda m: rendimento_aplicacao_regular(m, pontos_mensais/100.0, 0.0915, 0.125))


df_rendimentos_acumulo.loc[:, 'U.I. (FicRISK)'] = df_rendimentos_acumulo['Mês'].apply(
    lambda m: rendimento_aplicacao_regular(m, pontos_mensais/100.0, 0.1935, 0.2))

def cor_se_maior_igual(v, ref):
    if v < ref:
        return ''
    else:
        return 'background-color: green'

df_rendimentos_acumulo.round(2).style.applymap(
    lambda i: cor_se_maior_igual(i, valor_compra),
    subset=['Valor (Uso Imediato - U.I.)', 'U.I. (Poupanca)', 'U.I. (FicSAFE)', 'U.I. (FicRISK)']
).applymap(
    lambda i: cor_se_maior_igual(i, valor_compra*80),
    subset=['Pontos Gerados']
)
```




<style  type="text/css" >
    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row24_col1 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row25_col1 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row25_col5 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row26_col1 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row26_col5 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row27_col1 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row27_col4 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row27_col5 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row28_col1 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row28_col3 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row28_col4 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row28_col5 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row29_col1 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row29_col3 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row29_col4 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row29_col5 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row30_col1 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row30_col2 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row30_col3 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row30_col4 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row30_col5 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row31_col1 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row31_col2 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row31_col3 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row31_col4 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row31_col5 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row32_col1 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row32_col2 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row32_col3 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row32_col4 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row32_col5 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row33_col1 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row33_col2 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row33_col3 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row33_col4 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row33_col5 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row34_col1 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row34_col2 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row34_col3 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row34_col4 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row34_col5 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row35_col1 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row35_col2 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row35_col3 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row35_col4 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row35_col5 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row36_col1 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row36_col2 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row36_col3 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row36_col4 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row36_col5 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row37_col1 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row37_col2 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row37_col3 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row37_col4 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row37_col5 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row38_col1 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row38_col2 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row38_col3 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row38_col4 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row38_col5 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row39_col1 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row39_col2 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row39_col3 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row39_col4 {
            background-color:  green;
        }    #T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row39_col5 {
            background-color:  green;
        }</style>  
<table id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502" > 
<thead>    <tr> 
        <th class="blank level0" ></th> 
        <th class="col_heading level0 col0" >Mês</th> 
        <th class="col_heading level0 col1" >Pontos Gerados</th> 
        <th class="col_heading level0 col2" >Valor (Uso Imediato - U.I.)</th> 
        <th class="col_heading level0 col3" >U.I. (Poupanca)</th> 
        <th class="col_heading level0 col4" >U.I. (FicSAFE)</th> 
        <th class="col_heading level0 col5" >U.I. (FicRISK)</th> 
    </tr></thead> 
<tbody>    <tr> 
        <th id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502level0_row0" class="row_heading level0 row0" >0</th> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row0_col0" class="data row0 col0" >1</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row0_col1" class="data row0 col1" >3300</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row0_col2" class="data row0 col2" >33</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row0_col3" class="data row0 col3" >33.17</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row0_col4" class="data row0 col4" >33.21</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row0_col5" class="data row0 col5" >33.39</td> 
    </tr>    <tr> 
        <th id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502level0_row1" class="row_heading level0 row1" >1</th> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row1_col0" class="data row1 col0" >2</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row1_col1" class="data row1 col1" >6600</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row1_col2" class="data row1 col2" >66</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row1_col3" class="data row1 col3" >66.52</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row1_col4" class="data row1 col4" >66.64</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row1_col5" class="data row1 col5" >67.18</td> 
    </tr>    <tr> 
        <th id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502level0_row2" class="row_heading level0 row2" >2</th> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row2_col0" class="data row2 col0" >3</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row2_col1" class="data row2 col1" >9900</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row2_col2" class="data row2 col2" >99</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row2_col3" class="data row2 col3" >100.05</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row2_col4" class="data row2 col4" >100.27</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row2_col5" class="data row2 col5" >101.38</td> 
    </tr>    <tr> 
        <th id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502level0_row3" class="row_heading level0 row3" >3</th> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row3_col0" class="data row3 col0" >4</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row3_col1" class="data row3 col1" >13200</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row3_col2" class="data row3 col2" >132</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row3_col3" class="data row3 col3" >133.75</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row3_col4" class="data row3 col4" >134.13</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row3_col5" class="data row3 col5" >135.98</td> 
    </tr>    <tr> 
        <th id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502level0_row4" class="row_heading level0 row4" >4</th> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row4_col0" class="data row4 col0" >5</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row4_col1" class="data row4 col1" >16500</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row4_col2" class="data row4 col2" >165</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row4_col3" class="data row4 col3" >167.62</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row4_col4" class="data row4 col4" >168.2</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row4_col5" class="data row4 col5" >171</td> 
    </tr>    <tr> 
        <th id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502level0_row5" class="row_heading level0 row5" >5</th> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row5_col0" class="data row5 col0" >6</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row5_col1" class="data row5 col1" >19800</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row5_col2" class="data row5 col2" >198</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row5_col3" class="data row5 col3" >201.68</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row5_col4" class="data row5 col4" >202.49</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row5_col5" class="data row5 col5" >206.44</td> 
    </tr>    <tr> 
        <th id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502level0_row6" class="row_heading level0 row6" >6</th> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row6_col0" class="data row6 col0" >7</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row6_col1" class="data row6 col1" >23100</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row6_col2" class="data row6 col2" >231</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row6_col3" class="data row6 col3" >235.91</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row6_col4" class="data row6 col4" >237.01</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row6_col5" class="data row6 col5" >242.31</td> 
    </tr>    <tr> 
        <th id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502level0_row7" class="row_heading level0 row7" >7</th> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row7_col0" class="data row7 col0" >8</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row7_col1" class="data row7 col1" >26400</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row7_col2" class="data row7 col2" >264</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row7_col3" class="data row7 col3" >270.33</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row7_col4" class="data row7 col4" >271.74</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row7_col5" class="data row7 col5" >278.61</td> 
    </tr>    <tr> 
        <th id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502level0_row8" class="row_heading level0 row8" >8</th> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row8_col0" class="data row8 col0" >9</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row8_col1" class="data row8 col1" >29700</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row8_col2" class="data row8 col2" >297</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row8_col3" class="data row8 col3" >304.92</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row8_col4" class="data row8 col4" >306.7</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row8_col5" class="data row8 col5" >315.36</td> 
    </tr>    <tr> 
        <th id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502level0_row9" class="row_heading level0 row9" >9</th> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row9_col0" class="data row9 col0" >10</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row9_col1" class="data row9 col1" >33000</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row9_col2" class="data row9 col2" >330</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row9_col3" class="data row9 col3" >339.7</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row9_col4" class="data row9 col4" >341.89</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row9_col5" class="data row9 col5" >352.55</td> 
    </tr>    <tr> 
        <th id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502level0_row10" class="row_heading level0 row10" >10</th> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row10_col0" class="data row10 col0" >11</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row10_col1" class="data row10 col1" >36300</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row10_col2" class="data row10 col2" >363</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row10_col3" class="data row10 col3" >374.66</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row10_col4" class="data row10 col4" >377.3</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row10_col5" class="data row10 col5" >390.2</td> 
    </tr>    <tr> 
        <th id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502level0_row11" class="row_heading level0 row11" >11</th> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row11_col0" class="data row11 col0" >12</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row11_col1" class="data row11 col1" >39600</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row11_col2" class="data row11 col2" >396</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row11_col3" class="data row11 col3" >409.81</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row11_col4" class="data row11 col4" >412.94</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row11_col5" class="data row11 col5" >428.31</td> 
    </tr>    <tr> 
        <th id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502level0_row12" class="row_heading level0 row12" >12</th> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row12_col0" class="data row12 col0" >13</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row12_col1" class="data row12 col1" >42900</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row12_col2" class="data row12 col2" >429</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row12_col3" class="data row12 col3" >445.14</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row12_col4" class="data row12 col4" >448.82</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row12_col5" class="data row12 col5" >466.88</td> 
    </tr>    <tr> 
        <th id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502level0_row13" class="row_heading level0 row13" >13</th> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row13_col0" class="data row13 col0" >14</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row13_col1" class="data row13 col1" >46200</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row13_col2" class="data row13 col2" >462</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row13_col3" class="data row13 col3" >480.65</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row13_col4" class="data row13 col4" >484.92</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row13_col5" class="data row13 col5" >505.94</td> 
    </tr>    <tr> 
        <th id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502level0_row14" class="row_heading level0 row14" >14</th> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row14_col0" class="data row14 col0" >15</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row14_col1" class="data row14 col1" >49500</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row14_col2" class="data row14 col2" >495</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row14_col3" class="data row14 col3" >516.36</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row14_col4" class="data row14 col4" >521.26</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row14_col5" class="data row14 col5" >545.47</td> 
    </tr>    <tr> 
        <th id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502level0_row15" class="row_heading level0 row15" >15</th> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row15_col0" class="data row15 col0" >16</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row15_col1" class="data row15 col1" >52800</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row15_col2" class="data row15 col2" >528</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row15_col3" class="data row15 col3" >552.25</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row15_col4" class="data row15 col4" >557.84</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row15_col5" class="data row15 col5" >585.49</td> 
    </tr>    <tr> 
        <th id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502level0_row16" class="row_heading level0 row16" >16</th> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row16_col0" class="data row16 col0" >17</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row16_col1" class="data row16 col1" >56100</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row16_col2" class="data row16 col2" >561</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row16_col3" class="data row16 col3" >588.33</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row16_col4" class="data row16 col4" >594.65</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row16_col5" class="data row16 col5" >626.01</td> 
    </tr>    <tr> 
        <th id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502level0_row17" class="row_heading level0 row17" >17</th> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row17_col0" class="data row17 col0" >18</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row17_col1" class="data row17 col1" >59400</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row17_col2" class="data row17 col2" >594</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row17_col3" class="data row17 col3" >624.6</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row17_col4" class="data row17 col4" >631.7</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row17_col5" class="data row17 col5" >667.03</td> 
    </tr>    <tr> 
        <th id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502level0_row18" class="row_heading level0 row18" >18</th> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row18_col0" class="data row18 col0" >19</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row18_col1" class="data row18 col1" >62700</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row18_col2" class="data row18 col2" >627</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row18_col3" class="data row18 col3" >661.06</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row18_col4" class="data row18 col4" >669</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row18_col5" class="data row18 col5" >708.56</td> 
    </tr>    <tr> 
        <th id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502level0_row19" class="row_heading level0 row19" >19</th> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row19_col0" class="data row19 col0" >20</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row19_col1" class="data row19 col1" >66000</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row19_col2" class="data row19 col2" >660</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row19_col3" class="data row19 col3" >697.71</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row19_col4" class="data row19 col4" >706.53</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row19_col5" class="data row19 col5" >750.62</td> 
    </tr>    <tr> 
        <th id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502level0_row20" class="row_heading level0 row20" >20</th> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row20_col0" class="data row20 col0" >21</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row20_col1" class="data row20 col1" >69300</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row20_col2" class="data row20 col2" >693</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row20_col3" class="data row20 col3" >734.55</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row20_col4" class="data row20 col4" >744.31</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row20_col5" class="data row20 col5" >793.19</td> 
    </tr>    <tr> 
        <th id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502level0_row21" class="row_heading level0 row21" >21</th> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row21_col0" class="data row21 col0" >22</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row21_col1" class="data row21 col1" >72600</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row21_col2" class="data row21 col2" >726</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row21_col3" class="data row21 col3" >771.59</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row21_col4" class="data row21 col4" >782.34</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row21_col5" class="data row21 col5" >836.31</td> 
    </tr>    <tr> 
        <th id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502level0_row22" class="row_heading level0 row22" >22</th> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row22_col0" class="data row22 col0" >23</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row22_col1" class="data row22 col1" >75900</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row22_col2" class="data row22 col2" >759</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row22_col3" class="data row22 col3" >808.82</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row22_col4" class="data row22 col4" >820.62</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row22_col5" class="data row22 col5" >879.96</td> 
    </tr>    <tr> 
        <th id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502level0_row23" class="row_heading level0 row23" >23</th> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row23_col0" class="data row23 col0" >24</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row23_col1" class="data row23 col1" >79200</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row23_col2" class="data row23 col2" >792</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row23_col3" class="data row23 col3" >846.25</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row23_col4" class="data row23 col4" >859.14</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row23_col5" class="data row23 col5" >924.17</td> 
    </tr>    <tr> 
        <th id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502level0_row24" class="row_heading level0 row24" >24</th> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row24_col0" class="data row24 col0" >25</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row24_col1" class="data row24 col1" >82500</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row24_col2" class="data row24 col2" >825</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row24_col3" class="data row24 col3" >883.88</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row24_col4" class="data row24 col4" >897.92</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row24_col5" class="data row24 col5" >968.93</td> 
    </tr>    <tr> 
        <th id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502level0_row25" class="row_heading level0 row25" >25</th> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row25_col0" class="data row25 col0" >26</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row25_col1" class="data row25 col1" >85800</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row25_col2" class="data row25 col2" >858</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row25_col3" class="data row25 col3" >921.7</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row25_col4" class="data row25 col4" >936.95</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row25_col5" class="data row25 col5" >1014.26</td> 
    </tr>    <tr> 
        <th id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502level0_row26" class="row_heading level0 row26" >26</th> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row26_col0" class="data row26 col0" >27</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row26_col1" class="data row26 col1" >89100</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row26_col2" class="data row26 col2" >891</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row26_col3" class="data row26 col3" >959.73</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row26_col4" class="data row26 col4" >976.24</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row26_col5" class="data row26 col5" >1060.17</td> 
    </tr>    <tr> 
        <th id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502level0_row27" class="row_heading level0 row27" >27</th> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row27_col0" class="data row27 col0" >28</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row27_col1" class="data row27 col1" >92400</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row27_col2" class="data row27 col2" >924</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row27_col3" class="data row27 col3" >997.95</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row27_col4" class="data row27 col4" >1015.78</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row27_col5" class="data row27 col5" >1106.66</td> 
    </tr>    <tr> 
        <th id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502level0_row28" class="row_heading level0 row28" >28</th> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row28_col0" class="data row28 col0" >29</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row28_col1" class="data row28 col1" >95700</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row28_col2" class="data row28 col2" >957</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row28_col3" class="data row28 col3" >1036.38</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row28_col4" class="data row28 col4" >1055.59</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row28_col5" class="data row28 col5" >1153.74</td> 
    </tr>    <tr> 
        <th id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502level0_row29" class="row_heading level0 row29" >29</th> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row29_col0" class="data row29 col0" >30</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row29_col1" class="data row29 col1" >99000</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row29_col2" class="data row29 col2" >990</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row29_col3" class="data row29 col3" >1075</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row29_col4" class="data row29 col4" >1095.65</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row29_col5" class="data row29 col5" >1201.42</td> 
    </tr>    <tr> 
        <th id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502level0_row30" class="row_heading level0 row30" >30</th> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row30_col0" class="data row30 col0" >31</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row30_col1" class="data row30 col1" >102300</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row30_col2" class="data row30 col2" >1023</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row30_col3" class="data row30 col3" >1113.83</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row30_col4" class="data row30 col4" >1135.98</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row30_col5" class="data row30 col5" >1249.71</td> 
    </tr>    <tr> 
        <th id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502level0_row31" class="row_heading level0 row31" >31</th> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row31_col0" class="data row31 col0" >32</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row31_col1" class="data row31 col1" >105600</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row31_col2" class="data row31 col2" >1056</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row31_col3" class="data row31 col3" >1152.87</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row31_col4" class="data row31 col4" >1176.57</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row31_col5" class="data row31 col5" >1298.63</td> 
    </tr>    <tr> 
        <th id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502level0_row32" class="row_heading level0 row32" >32</th> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row32_col0" class="data row32 col0" >33</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row32_col1" class="data row32 col1" >108900</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row32_col2" class="data row32 col2" >1089</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row32_col3" class="data row32 col3" >1192.11</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row32_col4" class="data row32 col4" >1217.44</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row32_col5" class="data row32 col5" >1348.17</td> 
    </tr>    <tr> 
        <th id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502level0_row33" class="row_heading level0 row33" >33</th> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row33_col0" class="data row33 col0" >34</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row33_col1" class="data row33 col1" >112200</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row33_col2" class="data row33 col2" >1122</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row33_col3" class="data row33 col3" >1231.55</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row33_col4" class="data row33 col4" >1258.57</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row33_col5" class="data row33 col5" >1398.34</td> 
    </tr>    <tr> 
        <th id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502level0_row34" class="row_heading level0 row34" >34</th> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row34_col0" class="data row34 col0" >35</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row34_col1" class="data row34 col1" >115500</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row34_col2" class="data row34 col2" >1155</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row34_col3" class="data row34 col3" >1271.21</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row34_col4" class="data row34 col4" >1299.97</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row34_col5" class="data row34 col5" >1449.17</td> 
    </tr>    <tr> 
        <th id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502level0_row35" class="row_heading level0 row35" >35</th> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row35_col0" class="data row35 col0" >36</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row35_col1" class="data row35 col1" >118800</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row35_col2" class="data row35 col2" >1188</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row35_col3" class="data row35 col3" >1311.07</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row35_col4" class="data row35 col4" >1341.64</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row35_col5" class="data row35 col5" >1500.65</td> 
    </tr>    <tr> 
        <th id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502level0_row36" class="row_heading level0 row36" >36</th> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row36_col0" class="data row36 col0" >37</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row36_col1" class="data row36 col1" >122100</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row36_col2" class="data row36 col2" >1221</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row36_col3" class="data row36 col3" >1351.14</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row36_col4" class="data row36 col4" >1383.59</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row36_col5" class="data row36 col5" >1552.8</td> 
    </tr>    <tr> 
        <th id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502level0_row37" class="row_heading level0 row37" >37</th> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row37_col0" class="data row37 col0" >38</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row37_col1" class="data row37 col1" >125400</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row37_col2" class="data row37 col2" >1254</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row37_col3" class="data row37 col3" >1391.42</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row37_col4" class="data row37 col4" >1425.81</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row37_col5" class="data row37 col5" >1605.62</td> 
    </tr>    <tr> 
        <th id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502level0_row38" class="row_heading level0 row38" >38</th> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row38_col0" class="data row38 col0" >39</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row38_col1" class="data row38 col1" >128700</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row38_col2" class="data row38 col2" >1287</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row38_col3" class="data row38 col3" >1431.92</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row38_col4" class="data row38 col4" >1468.32</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row38_col5" class="data row38 col5" >1659.14</td> 
    </tr>    <tr> 
        <th id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502level0_row39" class="row_heading level0 row39" >39</th> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row39_col0" class="data row39 col0" >40</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row39_col1" class="data row39 col1" >132000</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row39_col2" class="data row39 col2" >1320</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row39_col3" class="data row39 col3" >1472.63</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row39_col4" class="data row39 col4" >1511.1</td> 
        <td id="T_a3d6bde8_eb95_11e8_bddf_e8039af9b502row39_col5" class="data row39 col5" >1713.34</td> 
    </tr></tbody> 
</table> 



No gráfico/tabela acima, o objetivo é atingido quando as linhas de uma coluna se tornam verdes. O objetivo aqui é acumular pontos o bastante para pagar a compra ou acumular rendimento suficiente das aplicações dos pontos já utilizados para superar o valor da compra.

Assim, atingimos o objetivo de R\$ 1.000,00 por meio do acumulo de pontos em 25 meses, 29 caso tenhamos investido o valor dos pontos na poupança, 28 se em um fundo de rentabilidade similar ao do FicSAFE e 26 caso investido num fundo similar ao FicRISK FicRISK.

Logo, **acumular os pontos do NuBank Rewards é do maior interesse do membro do programa.**

Isso acontece porque os pontos são 25\% mais valiosos para troca por vôos, o que implica que o valor equivalente, caso investido, teria de ser valorizado em 25\% no mesmo periodo necessário para acumular pontos suficientes para a troca. 25\% é um alvo ambicioso para investimentos de aproximadamente dois anos, e frequentemente inatingivel.

## Análise geral


```python
def analisa_condicoes(valor_fatura_mensal, valor_compra,
                      rendimento_anual_benchmark, imposto_de_renda_benchmark,
                      max_periodo_analise=120):

    # DF Base
    df = pd.DataFrame({
        'mes': list(range(max_periodo_analise+1))[1:]
    })
    
    # Acumulo
    df.loc[:, 'acumulo_pontos'] = df['mes'] * valor_fatura_mensal

    # Benchmark
    df.loc[:, 'benchmark'] = df['mes'].apply(
        lambda m: rendimento_aplicacao_regular(m, valor_fatura_mensal/100.0,
                                               rendimento_anual_benchmark, imposto_de_renda_benchmark))
    
    # Identificamos o primeiro a atingir o valor de compra
    indice_acumulo = df[df['acumulo_pontos'] > valor_compra * 80]
    if len(indice_acumulo) > 0:
        indice_acumulo = int(indice_acumulo.loc[indice_acumulo['acumulo_pontos'].idxmin()]['mes'])
    else:
        indice_acumulo = max_periodo_analise

    indice_benchmark = df[df['benchmark'] > valor_compra]
    if len(indice_benchmark) > 0:
        indice_benchmark  = int(indice_benchmark.loc[indice_benchmark['benchmark'].idxmin()]['mes'])
    else:
        indice_benchmark = max_periodo_analise

    return indice_acumulo, indice_benchmark
```


```python
lista_pares_rendimentos_viaveis = [
    (0.065, 0.0),
    (0.075, 0.0),
    (0.085, 0.0),
    (0.0915, 0.125),
    (0.0100, 0.125),
    (0.1100, 0.125),
    (0.1200, 0.125),
    (0.1935, 0.2),
    (0.2000, 0.2),
    (0.2200, 0.2),
    (0.2500, 0.2),
    (0.2700, 0.2),
]
```


```python
max_periodo_analise = 120

def iterador():
    for rendimento_anual_benchmark, imposto_de_renda_benchmark in lista_pares_rendimentos_viaveis:
        for valor_fatura_mensal in range(2250, 6000, 250):
            for valor_compra in range(250, 5000, 250):
                yield {
                    'max_periodo_analise': max_periodo_analise,
                    'rendimento_anual_benchmark': rendimento_anual_benchmark,
                    'imposto_de_renda_benchmark': imposto_de_renda_benchmark,
                    'valor_fatura_mensal': valor_fatura_mensal,
                    'valor_compra': valor_compra,
                    # 'resultado': resultado,
                    # 'periodo': periodo
                }


def processar_resultado(parametros):
    
    mes_acumulo, mes_benchmark = analisa_condicoes(**parametros)
    parametros.update({'mes_acumulo': mes_acumulo, 'mes_benchmark': mes_benchmark})
    
    return parametros
                
from tqdm import tqdm_notebook as tqdm
from multiprocessing import Pool
pool_processos = Pool(4)
resultados = list(pool_processos.imap_unordered(processar_resultado, tqdm(iterador())))

def decide_resultado(linha):
    if linha['mes_acumulo'] == linha['mes_benchmark'] == 120:
        return 'NENHUM'
    elif linha['mes_acumulo'] == linha['mes_benchmark']:
        return 'ACUMULO'
    elif linha['mes_acumulo'] <= linha['mes_benchmark']:
        return 'ACUMULO'
    else:
        return 'BENCHMARK'

df_resultados = pd.DataFrame(resultados)
df_resultados = df_resultados.assign(
    resultado=df_resultados.apply(decide_resultado, axis=1)
)
```


    HBox(children=(IntProgress(value=1, bar_style='info', max=1), HTML(value='')))


    



```python
df_resultados.resultado.value_counts()
```




    ACUMULO      1846
    BENCHMARK    1532
    NENHUM         42
    Name: resultado, dtype: int64




```python
df_resultados[df_resultados['resultado'] == 'BENCHMARK']
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>imposto_de_renda_benchmark</th>
      <th>max_periodo_analise</th>
      <th>mes_acumulo</th>
      <th>mes_benchmark</th>
      <th>rendimento_anual_benchmark</th>
      <th>valor_compra</th>
      <th>valor_fatura_mensal</th>
      <th>resultado</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>9</th>
      <td>0.0</td>
      <td>120</td>
      <td>89</td>
      <td>88</td>
      <td>0.065</td>
      <td>2500</td>
      <td>2250</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>10</th>
      <td>0.0</td>
      <td>120</td>
      <td>98</td>
      <td>95</td>
      <td>0.065</td>
      <td>2750</td>
      <td>2250</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>11</th>
      <td>0.0</td>
      <td>120</td>
      <td>120</td>
      <td>114</td>
      <td>0.065</td>
      <td>3500</td>
      <td>2250</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>12</th>
      <td>0.0</td>
      <td>120</td>
      <td>107</td>
      <td>101</td>
      <td>0.065</td>
      <td>3000</td>
      <td>2250</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>13</th>
      <td>0.0</td>
      <td>120</td>
      <td>116</td>
      <td>108</td>
      <td>0.065</td>
      <td>3250</td>
      <td>2250</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>28</th>
      <td>0.0</td>
      <td>120</td>
      <td>89</td>
      <td>87</td>
      <td>0.065</td>
      <td>2750</td>
      <td>2500</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>30</th>
      <td>0.0</td>
      <td>120</td>
      <td>105</td>
      <td>99</td>
      <td>0.065</td>
      <td>3250</td>
      <td>2500</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>31</th>
      <td>0.0</td>
      <td>120</td>
      <td>97</td>
      <td>93</td>
      <td>0.065</td>
      <td>3000</td>
      <td>2500</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>32</th>
      <td>0.0</td>
      <td>120</td>
      <td>113</td>
      <td>105</td>
      <td>0.065</td>
      <td>3500</td>
      <td>2500</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>33</th>
      <td>0.0</td>
      <td>120</td>
      <td>120</td>
      <td>111</td>
      <td>0.065</td>
      <td>3750</td>
      <td>2500</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>34</th>
      <td>0.0</td>
      <td>120</td>
      <td>120</td>
      <td>116</td>
      <td>0.065</td>
      <td>4000</td>
      <td>2500</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>48</th>
      <td>0.0</td>
      <td>120</td>
      <td>88</td>
      <td>87</td>
      <td>0.065</td>
      <td>3000</td>
      <td>2750</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>50</th>
      <td>0.0</td>
      <td>120</td>
      <td>95</td>
      <td>92</td>
      <td>0.065</td>
      <td>3250</td>
      <td>2750</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>51</th>
      <td>0.0</td>
      <td>120</td>
      <td>120</td>
      <td>113</td>
      <td>0.065</td>
      <td>4250</td>
      <td>2750</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>52</th>
      <td>0.0</td>
      <td>120</td>
      <td>102</td>
      <td>98</td>
      <td>0.065</td>
      <td>3500</td>
      <td>2750</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>53</th>
      <td>0.0</td>
      <td>120</td>
      <td>110</td>
      <td>103</td>
      <td>0.065</td>
      <td>3750</td>
      <td>2750</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>54</th>
      <td>0.0</td>
      <td>120</td>
      <td>117</td>
      <td>108</td>
      <td>0.065</td>
      <td>4000</td>
      <td>2750</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>55</th>
      <td>0.0</td>
      <td>120</td>
      <td>120</td>
      <td>118</td>
      <td>0.065</td>
      <td>4500</td>
      <td>2750</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>68</th>
      <td>0.0</td>
      <td>120</td>
      <td>94</td>
      <td>91</td>
      <td>0.065</td>
      <td>3500</td>
      <td>3000</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>69</th>
      <td>0.0</td>
      <td>120</td>
      <td>87</td>
      <td>86</td>
      <td>0.065</td>
      <td>3250</td>
      <td>3000</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>70</th>
      <td>0.0</td>
      <td>120</td>
      <td>101</td>
      <td>96</td>
      <td>0.065</td>
      <td>3750</td>
      <td>3000</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>72</th>
      <td>0.0</td>
      <td>120</td>
      <td>107</td>
      <td>101</td>
      <td>0.065</td>
      <td>4000</td>
      <td>3000</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>73</th>
      <td>0.0</td>
      <td>120</td>
      <td>120</td>
      <td>116</td>
      <td>0.065</td>
      <td>4750</td>
      <td>3000</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>74</th>
      <td>0.0</td>
      <td>120</td>
      <td>120</td>
      <td>111</td>
      <td>0.065</td>
      <td>4500</td>
      <td>3000</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>77</th>
      <td>0.0</td>
      <td>120</td>
      <td>114</td>
      <td>106</td>
      <td>0.065</td>
      <td>4250</td>
      <td>3000</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>88</th>
      <td>0.0</td>
      <td>120</td>
      <td>87</td>
      <td>86</td>
      <td>0.065</td>
      <td>3500</td>
      <td>3250</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>89</th>
      <td>0.0</td>
      <td>120</td>
      <td>99</td>
      <td>95</td>
      <td>0.065</td>
      <td>4000</td>
      <td>3250</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>91</th>
      <td>0.0</td>
      <td>120</td>
      <td>105</td>
      <td>100</td>
      <td>0.065</td>
      <td>4250</td>
      <td>3250</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>92</th>
      <td>0.0</td>
      <td>120</td>
      <td>111</td>
      <td>104</td>
      <td>0.065</td>
      <td>4500</td>
      <td>3250</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>93</th>
      <td>0.0</td>
      <td>120</td>
      <td>93</td>
      <td>91</td>
      <td>0.065</td>
      <td>3750</td>
      <td>3250</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>3375</th>
      <td>0.2</td>
      <td>120</td>
      <td>50</td>
      <td>43</td>
      <td>0.270</td>
      <td>3250</td>
      <td>5250</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>3376</th>
      <td>0.2</td>
      <td>120</td>
      <td>54</td>
      <td>45</td>
      <td>0.270</td>
      <td>3500</td>
      <td>5250</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>3377</th>
      <td>0.2</td>
      <td>120</td>
      <td>58</td>
      <td>47</td>
      <td>0.270</td>
      <td>3750</td>
      <td>5250</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>3378</th>
      <td>0.2</td>
      <td>120</td>
      <td>61</td>
      <td>49</td>
      <td>0.270</td>
      <td>4000</td>
      <td>5250</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>3379</th>
      <td>0.2</td>
      <td>120</td>
      <td>65</td>
      <td>51</td>
      <td>0.270</td>
      <td>4250</td>
      <td>5250</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>3380</th>
      <td>0.2</td>
      <td>120</td>
      <td>69</td>
      <td>53</td>
      <td>0.270</td>
      <td>4500</td>
      <td>5250</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>3381</th>
      <td>0.2</td>
      <td>120</td>
      <td>73</td>
      <td>55</td>
      <td>0.270</td>
      <td>4750</td>
      <td>5250</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>3389</th>
      <td>0.2</td>
      <td>120</td>
      <td>30</td>
      <td>29</td>
      <td>0.270</td>
      <td>2000</td>
      <td>5500</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>3390</th>
      <td>0.2</td>
      <td>120</td>
      <td>33</td>
      <td>32</td>
      <td>0.270</td>
      <td>2250</td>
      <td>5500</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>3391</th>
      <td>0.2</td>
      <td>120</td>
      <td>37</td>
      <td>34</td>
      <td>0.270</td>
      <td>2500</td>
      <td>5500</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>3392</th>
      <td>0.2</td>
      <td>120</td>
      <td>41</td>
      <td>37</td>
      <td>0.270</td>
      <td>2750</td>
      <td>5500</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>3393</th>
      <td>0.2</td>
      <td>120</td>
      <td>44</td>
      <td>39</td>
      <td>0.270</td>
      <td>3000</td>
      <td>5500</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>3394</th>
      <td>0.2</td>
      <td>120</td>
      <td>48</td>
      <td>41</td>
      <td>0.270</td>
      <td>3250</td>
      <td>5500</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>3395</th>
      <td>0.2</td>
      <td>120</td>
      <td>51</td>
      <td>44</td>
      <td>0.270</td>
      <td>3500</td>
      <td>5500</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>3396</th>
      <td>0.2</td>
      <td>120</td>
      <td>55</td>
      <td>46</td>
      <td>0.270</td>
      <td>3750</td>
      <td>5500</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>3397</th>
      <td>0.2</td>
      <td>120</td>
      <td>59</td>
      <td>48</td>
      <td>0.270</td>
      <td>4000</td>
      <td>5500</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>3398</th>
      <td>0.2</td>
      <td>120</td>
      <td>62</td>
      <td>50</td>
      <td>0.270</td>
      <td>4250</td>
      <td>5500</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>3399</th>
      <td>0.2</td>
      <td>120</td>
      <td>66</td>
      <td>52</td>
      <td>0.270</td>
      <td>4500</td>
      <td>5500</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>3400</th>
      <td>0.2</td>
      <td>120</td>
      <td>70</td>
      <td>53</td>
      <td>0.270</td>
      <td>4750</td>
      <td>5500</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>3409</th>
      <td>0.2</td>
      <td>120</td>
      <td>32</td>
      <td>30</td>
      <td>0.270</td>
      <td>2250</td>
      <td>5750</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>3410</th>
      <td>0.2</td>
      <td>120</td>
      <td>35</td>
      <td>33</td>
      <td>0.270</td>
      <td>2500</td>
      <td>5750</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>3411</th>
      <td>0.2</td>
      <td>120</td>
      <td>39</td>
      <td>35</td>
      <td>0.270</td>
      <td>2750</td>
      <td>5750</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>3412</th>
      <td>0.2</td>
      <td>120</td>
      <td>42</td>
      <td>38</td>
      <td>0.270</td>
      <td>3000</td>
      <td>5750</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>3413</th>
      <td>0.2</td>
      <td>120</td>
      <td>46</td>
      <td>40</td>
      <td>0.270</td>
      <td>3250</td>
      <td>5750</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>3414</th>
      <td>0.2</td>
      <td>120</td>
      <td>49</td>
      <td>42</td>
      <td>0.270</td>
      <td>3500</td>
      <td>5750</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>3415</th>
      <td>0.2</td>
      <td>120</td>
      <td>53</td>
      <td>44</td>
      <td>0.270</td>
      <td>3750</td>
      <td>5750</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>3416</th>
      <td>0.2</td>
      <td>120</td>
      <td>56</td>
      <td>46</td>
      <td>0.270</td>
      <td>4000</td>
      <td>5750</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>3417</th>
      <td>0.2</td>
      <td>120</td>
      <td>60</td>
      <td>48</td>
      <td>0.270</td>
      <td>4250</td>
      <td>5750</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>3418</th>
      <td>0.2</td>
      <td>120</td>
      <td>63</td>
      <td>50</td>
      <td>0.270</td>
      <td>4500</td>
      <td>5750</td>
      <td>BENCHMARK</td>
    </tr>
    <tr>
      <th>3419</th>
      <td>0.2</td>
      <td>120</td>
      <td>67</td>
      <td>52</td>
      <td>0.270</td>
      <td>4750</td>
      <td>5750</td>
      <td>BENCHMARK</td>
    </tr>
  </tbody>
</table>
<p>1532 rows × 8 columns</p>
</div>


