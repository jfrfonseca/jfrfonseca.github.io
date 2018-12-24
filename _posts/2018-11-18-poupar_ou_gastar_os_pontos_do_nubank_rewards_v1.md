---
layout: post
title: "Poupar ou Gastar os Pontos do NuBank Rewards? -V1"
date: 2018-12-24 11:39:13 -0200
categories:
    - jupyter notebook
---

# Poupar ou Gastar os Pontos do NuBank Rewards? - DEPRECATED

Edit: Este post foi originalmente escrito em 03 de Novembro de 2018. Em 13 de Novembro de 2018, o NuBank atualizou os termos do programa NuBank Rewards, ao qual agora esta análise está defasada. Veja a análise atualizada aqui.

## O que é o programa NuBank Rewards

O Rewards é um programa de recompensas por fidelidade do uso do cartão NuBank, um cartão de crédito sem anuidade de um dos primeiros bancos digitais do Brasil.

No NuBank Rewards, cada real que você gasta no cartão NuBank vale um ponto. Estes pontos nunca expiram e podem ser trocados por descontos na sua fatura do cartão de crédito NuBank no valor de compras já efetuadas com o cartão.
Ou seja, você usa seus pontos para apagar uma cobrança de algo de comprou da sua fatura, mesmo depois da compra já ter sido paga.

O programa NuBank rewards não é gratuito - existe uma cobrança mensal de R\$ 19.90 para todos os participantes do programa.

É importante ressaltar que a quantidade de pontos que você precisa para apagar uma compra não é a mesma que a quantidade de centavos na compra - cada ponto vale MENOS de 1 centavo na maioria das compras.

Auditando minhas faturas, descobri que cada ponto do NuBank Rewards vale 0.769 centavos de real para apagar compras feitas no UBER, CABIFY ou IFOOD.

| Uber - 0.007689 | Cabify - 0.007690 | Ifood - 0.007692 |
| --------------- | ----------------- | ---------------- |
| \$4.74 - 617    | \$6.90 - 897      | \$55.90 - 7267   |
| \$12.66 - 1646  | \$8.52 - 1108     | \$81.37 - 10579  |
| \$15.18 - 1974  | \$10.72 - 1394    | \$99.90 - 12987  |
| \$15.28 - 1987  | \$22.58 - 2936    | \$91.37 - 11879  |
| \$6.23 - 810    | \$7.42 - 965      | \$56.00 - 7280   |

Contudo, para compras de VOOS ou HOTÉIS, cada ponto vale um centavo, e para compras no SPOTIFY, 1.345 centavos

| Voos & Hotéis - 0.010000 | Spotify - 0.013450 |
| -- | -- |
| \$702.12 - 70212 | \$26.90 - 2000 |
| \$216.75 - 21675 | \$26.90 - 2000 |
| \$526.62 - 52662 | \$26.90 - 2000 |
| \$412.17 - 41217 | \$26.90 - 2000 |
| \$359.01 - 35901 | \$26.90 - 2000 |

**Ou seja, os pontos do NuBank Rewards são 30% mais valiosos para uso em VÔOS e HOTÉIS do que para uso em outros convênios, com exceção do Spotify**

## O NuBank Rewards vale a pena?

Para saber se o programa vale a pena, podemos pensar o valor descontado da fatura como o rendimento de um investimento. Para que esse investimento valha a pena, o rendimento tem que superar outros investimentos de investimento mínimo, liquidez e risco similares.

- O Investimento Mínimo (mínima quantidade de reais necessária para fazer o investimento) do Nubank Rewards é de R\$ 19.90, o valor da mensalidade.
- A Liquidez do Nubank Rewards não é diretamente comparável a liquidez da Caderneta de Poupança uma vez que os "rendimentos" somente podem ser usados para abater valores da fatura, mas tal abatimento afeta instantaneamente seu limite de crédito. Para esta análise, considero que os rendimentos da poupança, de fundos de investimento e do NuBank Rewards só são mensuraveis no momento do pagamento da fatura, ou seja, com liquidez em uma certa data do mês.
- O Risco de Mercado (risco de variação dos preços por forças de mercado) do NuBank Rewards é nulo, já que não há um fator de mercado que afete a relação de conversão entre os pontos do programa e as compras efetuadas. Para esta análise, consideraremos nulo o risco de mercado da Caderneta de Poupança.
- O Risco de Default do NuBank Rewards é o risco do banco NuBank quebrar. Para esta análise, consideraremos este e outros riscos técnicos negligíveis.
- Os elementos apagados da fatura do NuBank Rewards não são tributáveis pelo Imposto de Renda

Então vamos assumir que o investimento mínimo do NuBank Rewards (R\$ 20,00, para simplificar) seja investido em um fundo, que tem imposto de renda, ou numa Caderneta de Poupança, que não tem imposto de renda.

- Rendimento da Caderneta de Poupança: 6.5% ao ano, 0% de Imposto de Renda
- Rendimento do Fundo Fictício FicSAFE: 9.15% ao ano, 12.5% de Imposto de Renda
- Rendimento do Fundo Fictício FicRISK: 19.35% ao ano, 20% de Imposto de Renda

Obs: assumo que os fundos fictícios FicSAFE e FicRISK também tem investimento mínimo de R\$20


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
df_rendimentos_comparaveis.loc[:, 'Investimento'] = df_rendimentos_comparaveis['Mês'] * 20

df_rendimentos_comparaveis.loc[:, 'Poupança (M)'] = df_rendimentos_comparaveis['Mês'].apply(
    lambda m: rendimento_aplicacao_regular(m, 20, 0.065, 0))
df_rendimentos_comparaveis.loc[:, 'Poupança (R%)'] = \
    df_rendimentos_comparaveis['Poupança (M)'] / df_rendimentos_comparaveis['Investimento']

df_rendimentos_comparaveis.loc[:, 'FicSAFE (M)'] = df_rendimentos_comparaveis['Mês'].apply(
    lambda m: rendimento_aplicacao_regular(m, 20, 0.0915, 0.125))
df_rendimentos_comparaveis.loc[:, 'FicSAFE (R%)'] = \
    df_rendimentos_comparaveis['FicSAFE (M)'] / df_rendimentos_comparaveis['Investimento']

df_rendimentos_comparaveis.loc[:, 'FicRISK (M)'] = df_rendimentos_comparaveis['Mês'].apply(
    lambda m: rendimento_aplicacao_regular(m, 20, 0.1935, 0.2))
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
      <td>20</td>
      <td>20.11</td>
      <td>1.01</td>
      <td>20.13</td>
      <td>1.01</td>
      <td>20.24</td>
      <td>1.01</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>40</td>
      <td>40.32</td>
      <td>1.01</td>
      <td>40.39</td>
      <td>1.01</td>
      <td>40.72</td>
      <td>1.02</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>60</td>
      <td>60.63</td>
      <td>1.01</td>
      <td>60.77</td>
      <td>1.01</td>
      <td>61.44</td>
      <td>1.02</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>80</td>
      <td>81.06</td>
      <td>1.01</td>
      <td>81.29</td>
      <td>1.02</td>
      <td>82.41</td>
      <td>1.03</td>
    </tr>
    <tr>
      <th>4</th>
      <td>6</td>
      <td>120</td>
      <td>122.23</td>
      <td>1.02</td>
      <td>122.72</td>
      <td>1.02</td>
      <td>125.11</td>
      <td>1.04</td>
    </tr>
    <tr>
      <th>5</th>
      <td>9</td>
      <td>180</td>
      <td>184.80</td>
      <td>1.03</td>
      <td>185.88</td>
      <td>1.03</td>
      <td>191.13</td>
      <td>1.06</td>
    </tr>
    <tr>
      <th>6</th>
      <td>12</td>
      <td>240</td>
      <td>248.37</td>
      <td>1.03</td>
      <td>250.27</td>
      <td>1.04</td>
      <td>259.58</td>
      <td>1.08</td>
    </tr>
    <tr>
      <th>7</th>
      <td>15</td>
      <td>300</td>
      <td>312.94</td>
      <td>1.04</td>
      <td>315.92</td>
      <td>1.05</td>
      <td>330.59</td>
      <td>1.10</td>
    </tr>
    <tr>
      <th>8</th>
      <td>18</td>
      <td>360</td>
      <td>378.54</td>
      <td>1.05</td>
      <td>382.85</td>
      <td>1.06</td>
      <td>404.26</td>
      <td>1.12</td>
    </tr>
    <tr>
      <th>9</th>
      <td>24</td>
      <td>480</td>
      <td>512.88</td>
      <td>1.07</td>
      <td>520.69</td>
      <td>1.08</td>
      <td>560.10</td>
      <td>1.17</td>
    </tr>
    <tr>
      <th>10</th>
      <td>30</td>
      <td>600</td>
      <td>651.52</td>
      <td>1.09</td>
      <td>664.03</td>
      <td>1.11</td>
      <td>728.13</td>
      <td>1.21</td>
    </tr>
    <tr>
      <th>11</th>
      <td>36</td>
      <td>720</td>
      <td>794.59</td>
      <td>1.10</td>
      <td>813.11</td>
      <td>1.13</td>
      <td>909.49</td>
      <td>1.26</td>
    </tr>
    <tr>
      <th>12</th>
      <td>42</td>
      <td>840</td>
      <td>942.23</td>
      <td>1.12</td>
      <td>968.20</td>
      <td>1.15</td>
      <td>1105.39</td>
      <td>1.32</td>
    </tr>
    <tr>
      <th>13</th>
      <td>48</td>
      <td>960</td>
      <td>1094.60</td>
      <td>1.14</td>
      <td>1129.55</td>
      <td>1.18</td>
      <td>1317.19</td>
      <td>1.37</td>
    </tr>
  </tbody>
</table>
</div>



Para que o NuBank Rewards valha a pena, o valor descontado da fatura deveria ser maior do que a rentabilidade de uma das alternativas acima no mesmo periodo.

Ou seja, em 3 anos (36 meses), se o valor total descontado da minha fatura for:
- MAIOR QUE R\$ 74.59 - valeu mais a pena que a poupança.
- MAIOR QUE R\$ 93.11 - Valeu mais a pena que a poupança e o fundo FicSAFE
- MAIOR QUE R\$ 189.49 - Valeu mais a pena que a poupança e os dois fundos

Utilizando o pior caso do valor dos pontos do NuBank Rewards (0.769 centavos/ponto), seriam necessários 24708 pontos para descontar compras que totalizem R\$ 190,00. Seriam necessários mais 93629 pontos para descontar os R\$ 720,00 pagos como mensalidade para programa.

**Assim, seria necessário que o titular do cartão NuBank gaste no mínimo R\$ 118.337,00 reais ao longo de três anos, ou R\$ 3.288,00 por mês. O valor de desconto na fatura mensal seria de R\$ 25.29, totalizando uma fatura de R\$ 3.262,71**

**Numa estimativa mais concervadora, seriam necessários 105853 pontos, R\$ 2.940,37 gastos por mês para uma fatura de R\$ 2.917,74 após o desconto de R\$ 22.62**

## Qual a melhor forma de usar os pontos do NuBank Rewards?

O ideal é priorizar os pontos para uso em compras de vôos e hotéis, onde os pontos chegam a valer 30% a mais. Contudo, vôos e hotéis tendem a ser compras mais esporádicas e de maior volume unitário, o que significa que é necessário uma maior quantidade de pontos acumulados para poder descontá-las da fatura.

É melhor conservar os pontos, acumulando para uso nas compras de voos e hotéis, ou gastá-los imediatamente?

A vantagem de utilizar os pontos imediatamente é de liberar recursos que poderiam ser melhor investidos. A vantagem de acumular os pontos é que os mesmos seriam mais valorizados quando utilizados para descontar uma compra de voos ou hotéis.

Portanto, o custo de acumular os pontos é equivalente ao rendimento de uma aplicação na qual o valor dos pontos poderia ter sido investido. Vale a pena guardar os pontos quando o custo de acumulá-los é menor que o benefício dos mesmos.

Dada a natureza esporádica e variada das compras de vôos e hotéis, prefiro calcular os custos de acumulação de pontos necessários para cada compra.

Assim sendo, assumindo um gasto mensal de R\$ 3.300,00, e uma compra de voo de R\$ 1.000,00:


```python
pontos_mensais = 3300
valor_compra = 1000

df_rendimentos_acumulo = pd.DataFrame({
    'Mês': list(range(41))[1:]
})
df_rendimentos_acumulo.loc[:, 'Pontos Gerados'] = df_rendimentos_acumulo['Mês'] * pontos_mensais

df_rendimentos_acumulo.loc[:, 'Valor U.I.'] = df_rendimentos_acumulo['Mês'].apply(
    lambda m: rendimento_aplicacao_regular(m, (pontos_mensais*0.769)/100.0, 0.0, 0))


df_rendimentos_acumulo.loc[:, 'U.I. (Poupanca)'] = df_rendimentos_acumulo['Mês'].apply(
    lambda m: rendimento_aplicacao_regular(m, (pontos_mensais*0.769)/100.0, 0.065, 0))


df_rendimentos_acumulo.loc[:, 'U.I. (FicSAFE)'] = df_rendimentos_acumulo['Mês'].apply(
    lambda m: rendimento_aplicacao_regular(m, (pontos_mensais*0.769)/100.0, 0.0915, 0.125))


df_rendimentos_acumulo.loc[:, 'U.I. (FicRISK)'] = df_rendimentos_acumulo['Mês'].apply(
    lambda m: rendimento_aplicacao_regular(m, (pontos_mensais*0.769)/100.0, 0.1935, 0.2))

def vermelho_se_maior_igual(v, ref):
    if v < ref:
        return ''
    else:
        return 'background-color: green'

df_rendimentos_acumulo.round(2).style.applymap(
    lambda i: vermelho_se_maior_igual(i, valor_compra),
    subset=['Valor U.I.', 'U.I. (Poupanca)', 'U.I. (FicSAFE)', 'U.I. (FicRISK)']
).applymap(
    lambda i: vermelho_se_maior_igual(i, valor_compra*100),
    subset=['Pontos Gerados']
)
```




<style  type="text/css" >
    #T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row30_col1 {
            background-color:  green;
        }    #T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row31_col1 {
            background-color:  green;
        }    #T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row32_col1 {
            background-color:  green;
        }    #T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row32_col5 {
            background-color:  green;
        }    #T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row33_col1 {
            background-color:  green;
        }    #T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row33_col5 {
            background-color:  green;
        }    #T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row34_col1 {
            background-color:  green;
        }    #T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row34_col5 {
            background-color:  green;
        }    #T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row35_col1 {
            background-color:  green;
        }    #T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row35_col3 {
            background-color:  green;
        }    #T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row35_col4 {
            background-color:  green;
        }    #T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row35_col5 {
            background-color:  green;
        }    #T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row36_col1 {
            background-color:  green;
        }    #T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row36_col3 {
            background-color:  green;
        }    #T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row36_col4 {
            background-color:  green;
        }    #T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row36_col5 {
            background-color:  green;
        }    #T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row37_col1 {
            background-color:  green;
        }    #T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row37_col3 {
            background-color:  green;
        }    #T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row37_col4 {
            background-color:  green;
        }    #T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row37_col5 {
            background-color:  green;
        }    #T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row38_col1 {
            background-color:  green;
        }    #T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row38_col3 {
            background-color:  green;
        }    #T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row38_col4 {
            background-color:  green;
        }    #T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row38_col5 {
            background-color:  green;
        }    #T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row39_col1 {
            background-color:  green;
        }    #T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row39_col2 {
            background-color:  green;
        }    #T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row39_col3 {
            background-color:  green;
        }    #T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row39_col4 {
            background-color:  green;
        }    #T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row39_col5 {
            background-color:  green;
        }</style>  
<table id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502" > 
<thead>    <tr> 
        <th class="blank level0" ></th> 
        <th class="col_heading level0 col0" >Mês</th> 
        <th class="col_heading level0 col1" >Pontos Gerados</th> 
        <th class="col_heading level0 col2" >Valor U.I.</th> 
        <th class="col_heading level0 col3" >U.I. (Poupanca)</th> 
        <th class="col_heading level0 col4" >U.I. (FicSAFE)</th> 
        <th class="col_heading level0 col5" >U.I. (FicRISK)</th> 
    </tr></thead> 
<tbody>    <tr> 
        <th id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502level0_row0" class="row_heading level0 row0" >0</th> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row0_col0" class="data row0 col0" >1</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row0_col1" class="data row0 col1" >3300</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row0_col2" class="data row0 col2" >25.38</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row0_col3" class="data row0 col3" >25.51</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row0_col4" class="data row0 col4" >25.54</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row0_col5" class="data row0 col5" >25.68</td> 
    </tr>    <tr> 
        <th id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502level0_row1" class="row_heading level0 row1" >1</th> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row1_col0" class="data row1 col0" >2</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row1_col1" class="data row1 col1" >6600</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row1_col2" class="data row1 col2" >50.75</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row1_col3" class="data row1 col3" >51.16</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row1_col4" class="data row1 col4" >51.24</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row1_col5" class="data row1 col5" >51.66</td> 
    </tr>    <tr> 
        <th id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502level0_row2" class="row_heading level0 row2" >2</th> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row2_col0" class="data row2 col0" >3</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row2_col1" class="data row2 col1" >9900</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row2_col2" class="data row2 col2" >76.13</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row2_col3" class="data row2 col3" >76.93</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row2_col4" class="data row2 col4" >77.11</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row2_col5" class="data row2 col5" >77.96</td> 
    </tr>    <tr> 
        <th id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502level0_row3" class="row_heading level0 row3" >3</th> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row3_col0" class="data row3 col0" >4</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row3_col1" class="data row3 col1" >13200</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row3_col2" class="data row3 col2" >101.51</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row3_col3" class="data row3 col3" >102.85</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row3_col4" class="data row3 col4" >103.15</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row3_col5" class="data row3 col5" >104.57</td> 
    </tr>    <tr> 
        <th id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502level0_row4" class="row_heading level0 row4" >4</th> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row4_col0" class="data row4 col0" >5</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row4_col1" class="data row4 col1" >16500</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row4_col2" class="data row4 col2" >126.89</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row4_col3" class="data row4 col3" >128.9</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row4_col4" class="data row4 col4" >129.35</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row4_col5" class="data row4 col5" >131.5</td> 
    </tr>    <tr> 
        <th id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502level0_row5" class="row_heading level0 row5" >5</th> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row5_col0" class="data row5 col0" >6</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row5_col1" class="data row5 col1" >19800</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row5_col2" class="data row5 col2" >152.26</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row5_col3" class="data row5 col3" >155.09</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row5_col4" class="data row5 col4" >155.72</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row5_col5" class="data row5 col5" >158.75</td> 
    </tr>    <tr> 
        <th id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502level0_row6" class="row_heading level0 row6" >6</th> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row6_col0" class="data row6 col0" >7</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row6_col1" class="data row6 col1" >23100</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row6_col2" class="data row6 col2" >177.64</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row6_col3" class="data row6 col3" >181.42</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row6_col4" class="data row6 col4" >182.26</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row6_col5" class="data row6 col5" >186.34</td> 
    </tr>    <tr> 
        <th id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502level0_row7" class="row_heading level0 row7" >7</th> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row7_col0" class="data row7 col0" >8</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row7_col1" class="data row7 col1" >26400</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row7_col2" class="data row7 col2" >203.02</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row7_col3" class="data row7 col3" >207.88</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row7_col4" class="data row7 col4" >208.97</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row7_col5" class="data row7 col5" >214.25</td> 
    </tr>    <tr> 
        <th id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502level0_row8" class="row_heading level0 row8" >8</th> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row8_col0" class="data row8 col0" >9</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row8_col1" class="data row8 col1" >29700</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row8_col2" class="data row8 col2" >228.39</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row8_col3" class="data row8 col3" >234.49</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row8_col4" class="data row8 col4" >235.85</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row8_col5" class="data row8 col5" >242.51</td> 
    </tr>    <tr> 
        <th id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502level0_row9" class="row_heading level0 row9" >9</th> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row9_col0" class="data row9 col0" >10</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row9_col1" class="data row9 col1" >33000</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row9_col2" class="data row9 col2" >253.77</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row9_col3" class="data row9 col3" >261.23</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row9_col4" class="data row9 col4" >262.91</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row9_col5" class="data row9 col5" >271.11</td> 
    </tr>    <tr> 
        <th id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502level0_row10" class="row_heading level0 row10" >10</th> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row10_col0" class="data row10 col0" >11</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row10_col1" class="data row10 col1" >36300</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row10_col2" class="data row10 col2" >279.15</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row10_col3" class="data row10 col3" >288.12</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row10_col4" class="data row10 col4" >290.14</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row10_col5" class="data row10 col5" >300.06</td> 
    </tr>    <tr> 
        <th id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502level0_row11" class="row_heading level0 row11" >11</th> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row11_col0" class="data row11 col0" >12</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row11_col1" class="data row11 col1" >39600</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row11_col2" class="data row11 col2" >304.52</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row11_col3" class="data row11 col3" >315.14</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row11_col4" class="data row11 col4" >317.55</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row11_col5" class="data row11 col5" >329.37</td> 
    </tr>    <tr> 
        <th id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502level0_row12" class="row_heading level0 row12" >12</th> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row12_col0" class="data row12 col0" >13</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row12_col1" class="data row12 col1" >42900</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row12_col2" class="data row12 col2" >329.9</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row12_col3" class="data row12 col3" >342.31</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row12_col4" class="data row12 col4" >345.14</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row12_col5" class="data row12 col5" >359.03</td> 
    </tr>    <tr> 
        <th id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502level0_row13" class="row_heading level0 row13" >13</th> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row13_col0" class="data row13 col0" >14</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row13_col1" class="data row13 col1" >46200</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row13_col2" class="data row13 col2" >355.28</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row13_col3" class="data row13 col3" >369.62</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row13_col4" class="data row13 col4" >372.9</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row13_col5" class="data row13 col5" >389.06</td> 
    </tr>    <tr> 
        <th id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502level0_row14" class="row_heading level0 row14" >14</th> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row14_col0" class="data row14 col0" >15</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row14_col1" class="data row14 col1" >49500</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row14_col2" class="data row14 col2" >380.66</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row14_col3" class="data row14 col3" >397.08</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row14_col4" class="data row14 col4" >400.85</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row14_col5" class="data row14 col5" >419.47</td> 
    </tr>    <tr> 
        <th id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502level0_row15" class="row_heading level0 row15" >15</th> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row15_col0" class="data row15 col0" >16</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row15_col1" class="data row15 col1" >52800</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row15_col2" class="data row15 col2" >406.03</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row15_col3" class="data row15 col3" >424.68</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row15_col4" class="data row15 col4" >428.98</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row15_col5" class="data row15 col5" >450.24</td> 
    </tr>    <tr> 
        <th id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502level0_row16" class="row_heading level0 row16" >16</th> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row16_col0" class="data row16 col0" >17</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row16_col1" class="data row16 col1" >56100</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row16_col2" class="data row16 col2" >431.41</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row16_col3" class="data row16 col3" >452.42</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row16_col4" class="data row16 col4" >457.29</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row16_col5" class="data row16 col5" >481.4</td> 
    </tr>    <tr> 
        <th id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502level0_row17" class="row_heading level0 row17" >17</th> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row17_col0" class="data row17 col0" >18</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row17_col1" class="data row17 col1" >59400</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row17_col2" class="data row17 col2" >456.79</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row17_col3" class="data row17 col3" >480.31</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row17_col4" class="data row17 col4" >485.78</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row17_col5" class="data row17 col5" >512.95</td> 
    </tr>    <tr> 
        <th id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502level0_row18" class="row_heading level0 row18" >18</th> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row18_col0" class="data row18 col0" >19</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row18_col1" class="data row18 col1" >62700</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row18_col2" class="data row18 col2" >482.16</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row18_col3" class="data row18 col3" >508.35</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row18_col4" class="data row18 col4" >514.46</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row18_col5" class="data row18 col5" >544.89</td> 
    </tr>    <tr> 
        <th id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502level0_row19" class="row_heading level0 row19" >19</th> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row19_col0" class="data row19 col0" >20</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row19_col1" class="data row19 col1" >66000</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row19_col2" class="data row19 col2" >507.54</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row19_col3" class="data row19 col3" >536.54</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row19_col4" class="data row19 col4" >543.32</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row19_col5" class="data row19 col5" >577.22</td> 
    </tr>    <tr> 
        <th id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502level0_row20" class="row_heading level0 row20" >20</th> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row20_col0" class="data row20 col0" >21</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row20_col1" class="data row20 col1" >69300</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row20_col2" class="data row20 col2" >532.92</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row20_col3" class="data row20 col3" >564.87</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row20_col4" class="data row20 col4" >572.38</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row20_col5" class="data row20 col5" >609.97</td> 
    </tr>    <tr> 
        <th id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502level0_row21" class="row_heading level0 row21" >21</th> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row21_col0" class="data row21 col0" >22</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row21_col1" class="data row21 col1" >72600</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row21_col2" class="data row21 col2" >558.29</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row21_col3" class="data row21 col3" >593.35</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row21_col4" class="data row21 col4" >601.62</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row21_col5" class="data row21 col5" >643.12</td> 
    </tr>    <tr> 
        <th id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502level0_row22" class="row_heading level0 row22" >22</th> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row22_col0" class="data row22 col0" >23</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row22_col1" class="data row22 col1" >75900</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row22_col2" class="data row22 col2" >583.67</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row22_col3" class="data row22 col3" >621.99</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row22_col4" class="data row22 col4" >631.05</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row22_col5" class="data row22 col5" >676.69</td> 
    </tr>    <tr> 
        <th id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502level0_row23" class="row_heading level0 row23" >23</th> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row23_col0" class="data row23 col0" >24</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row23_col1" class="data row23 col1" >79200</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row23_col2" class="data row23 col2" >609.05</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row23_col3" class="data row23 col3" >650.77</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row23_col4" class="data row23 col4" >660.68</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row23_col5" class="data row23 col5" >710.69</td> 
    </tr>    <tr> 
        <th id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502level0_row24" class="row_heading level0 row24" >24</th> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row24_col0" class="data row24 col0" >25</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row24_col1" class="data row24 col1" >82500</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row24_col2" class="data row24 col2" >634.42</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row24_col3" class="data row24 col3" >679.7</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row24_col4" class="data row24 col4" >690.5</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row24_col5" class="data row24 col5" >745.11</td> 
    </tr>    <tr> 
        <th id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502level0_row25" class="row_heading level0 row25" >25</th> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row25_col0" class="data row25 col0" >26</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row25_col1" class="data row25 col1" >85800</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row25_col2" class="data row25 col2" >659.8</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row25_col3" class="data row25 col3" >708.79</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row25_col4" class="data row25 col4" >720.52</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row25_col5" class="data row25 col5" >779.97</td> 
    </tr>    <tr> 
        <th id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502level0_row26" class="row_heading level0 row26" >26</th> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row26_col0" class="data row26 col0" >27</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row26_col1" class="data row26 col1" >89100</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row26_col2" class="data row26 col2" >685.18</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row26_col3" class="data row26 col3" >738.03</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row26_col4" class="data row26 col4" >750.73</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row26_col5" class="data row26 col5" >815.27</td> 
    </tr>    <tr> 
        <th id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502level0_row27" class="row_heading level0 row27" >27</th> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row27_col0" class="data row27 col0" >28</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row27_col1" class="data row27 col1" >92400</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row27_col2" class="data row27 col2" >710.56</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row27_col3" class="data row27 col3" >767.42</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row27_col4" class="data row27 col4" >781.14</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row27_col5" class="data row27 col5" >851.02</td> 
    </tr>    <tr> 
        <th id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502level0_row28" class="row_heading level0 row28" >28</th> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row28_col0" class="data row28 col0" >29</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row28_col1" class="data row28 col1" >95700</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row28_col2" class="data row28 col2" >735.93</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row28_col3" class="data row28 col3" >796.97</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row28_col4" class="data row28 col4" >811.75</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row28_col5" class="data row28 col5" >887.22</td> 
    </tr>    <tr> 
        <th id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502level0_row29" class="row_heading level0 row29" >29</th> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row29_col0" class="data row29 col0" >30</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row29_col1" class="data row29 col1" >99000</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row29_col2" class="data row29 col2" >761.31</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row29_col3" class="data row29 col3" >826.68</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row29_col4" class="data row29 col4" >842.56</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row29_col5" class="data row29 col5" >923.89</td> 
    </tr>    <tr> 
        <th id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502level0_row30" class="row_heading level0 row30" >30</th> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row30_col0" class="data row30 col0" >31</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row30_col1" class="data row30 col1" >102300</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row30_col2" class="data row30 col2" >786.69</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row30_col3" class="data row30 col3" >856.54</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row30_col4" class="data row30 col4" >873.57</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row30_col5" class="data row30 col5" >961.03</td> 
    </tr>    <tr> 
        <th id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502level0_row31" class="row_heading level0 row31" >31</th> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row31_col0" class="data row31 col0" >32</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row31_col1" class="data row31 col1" >105600</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row31_col2" class="data row31 col2" >812.06</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row31_col3" class="data row31 col3" >886.55</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row31_col4" class="data row31 col4" >904.79</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row31_col5" class="data row31 col5" >998.64</td> 
    </tr>    <tr> 
        <th id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502level0_row32" class="row_heading level0 row32" >32</th> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row32_col0" class="data row32 col0" >33</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row32_col1" class="data row32 col1" >108900</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row32_col2" class="data row32 col2" >837.44</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row32_col3" class="data row32 col3" >916.73</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row32_col4" class="data row32 col4" >936.21</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row32_col5" class="data row32 col5" >1036.74</td> 
    </tr>    <tr> 
        <th id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502level0_row33" class="row_heading level0 row33" >33</th> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row33_col0" class="data row33 col0" >34</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row33_col1" class="data row33 col1" >112200</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row33_col2" class="data row33 col2" >862.82</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row33_col3" class="data row33 col3" >947.06</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row33_col4" class="data row33 col4" >967.84</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row33_col5" class="data row33 col5" >1075.33</td> 
    </tr>    <tr> 
        <th id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502level0_row34" class="row_heading level0 row34" >34</th> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row34_col0" class="data row34 col0" >35</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row34_col1" class="data row34 col1" >115500</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row34_col2" class="data row34 col2" >888.19</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row34_col3" class="data row34 col3" >977.56</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row34_col4" class="data row34 col4" >999.67</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row34_col5" class="data row34 col5" >1114.41</td> 
    </tr>    <tr> 
        <th id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502level0_row35" class="row_heading level0 row35" >35</th> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row35_col0" class="data row35 col0" >36</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row35_col1" class="data row35 col1" >118800</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row35_col2" class="data row35 col2" >913.57</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row35_col3" class="data row35 col3" >1008.21</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row35_col4" class="data row35 col4" >1031.72</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row35_col5" class="data row35 col5" >1154</td> 
    </tr>    <tr> 
        <th id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502level0_row36" class="row_heading level0 row36" >36</th> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row36_col0" class="data row36 col0" >37</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row36_col1" class="data row36 col1" >122100</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row36_col2" class="data row36 col2" >938.95</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row36_col3" class="data row36 col3" >1039.03</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row36_col4" class="data row36 col4" >1063.98</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row36_col5" class="data row36 col5" >1194.1</td> 
    </tr>    <tr> 
        <th id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502level0_row37" class="row_heading level0 row37" >37</th> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row37_col0" class="data row37 col0" >38</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row37_col1" class="data row37 col1" >125400</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row37_col2" class="data row37 col2" >964.33</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row37_col3" class="data row37 col3" >1070.01</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row37_col4" class="data row37 col4" >1096.45</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row37_col5" class="data row37 col5" >1234.73</td> 
    </tr>    <tr> 
        <th id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502level0_row38" class="row_heading level0 row38" >38</th> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row38_col0" class="data row38 col0" >39</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row38_col1" class="data row38 col1" >128700</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row38_col2" class="data row38 col2" >989.7</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row38_col3" class="data row38 col3" >1101.15</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row38_col4" class="data row38 col4" >1129.14</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row38_col5" class="data row38 col5" >1275.88</td> 
    </tr>    <tr> 
        <th id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502level0_row39" class="row_heading level0 row39" >39</th> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row39_col0" class="data row39 col0" >40</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row39_col1" class="data row39 col1" >132000</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row39_col2" class="data row39 col2" >1015.08</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row39_col3" class="data row39 col3" >1132.45</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row39_col4" class="data row39 col4" >1162.04</td> 
        <td id="T_4b086e1a_eb7b_11e8_bddf_e8039af9b502row39_col5" class="data row39 col5" >1317.56</td> 
    </tr></tbody> 
</table> 



No gráfico/tabela acima, o objetivo é atingido quando as linhas de uma coluna se tornam verdes. O objetivo aqui é acumular pontos o bastante para pagar a compra ou acumular rendimento suficiente das aplicações dos pontos já utilizados para superar o valor da compra.

Assim, atingimos o objetivo de R\$ 1.000,00 por meio do acumulo de pontos em 31 meses, 33 caso tenhamos investido o valor dos pontos em um fundo de rentabilidade similar ao do FicRISK e 36 caso investido na poupança ou no FicSAFE. Caso os pontos não tenham sido investidos, o objetivo é atingido em 40 meses.

Logo, **acumular os pontos do NuBank Rewards oferece uma vantagem para o membro do programa.**
