# Engenharia_de_Dados_Cotacao_Criptomoedas
O mercado de criptomoedas tem experimentado um crescimento exponencial nos últimos anos, com uma variedade cada vez maior de ativos digitais disponíveis para compra, venda e negociação. Para acompanhar a volatilidade e as flutuações de preços desses ativos, surgiram diversos projetos e ferramentas de cotação, sendo o CoinMarketCap um dos mais renomados e utilizados, e que usaremos para cotação dos ativos escolhidos.

# CoinMarketCap
Conforme comentado, o CoinMarketCap é um site que rastreia e fornece informações sobre uma ampla gama de criptomoedas, incluindo seus preços em tempo real, capitalização de mercado, volume de negociação, suprimento circulante, histórico de preços e muito mais. Ele atua como uma plataforma de referência para investidores, traders, entusiastas de criptomoedas e qualquer pessoa interessada em acompanhar o mercado digital.

# Projeto
Conforme explicado, explanado e visando a coleta e organização dos dados relacionados às moedas para obtenção de insights e conclusão dessa tarefa:

# 1) criei um processo ETL:
    # E: Extração dos dados respectivos oriundos da fonte https://coinmarketcap.com/pt-br/, a partir do acréscimo da moeda na url e buscando, na classe específica, a classe que armazena os dados que queremos, sendo eles: Moeda, Sigla da Moeda, Preço, 1h%, Unidade, Data da Captura

    # T: Posterior à coleta dos dados, e visando a geração de um relatório formal relacionado às cotações, elaborei uma lógica para coletar cada informação, tratei os dados, transformei em dicionário - pela facilidade de trabalhar como dataframe, e adicionei ao dataframe

    # L: Logo após os tratamentos, fiz o carregamento em um arquivo csv, um arquivo já tratado, limpo e em conformidade ao que esperamos para facilidade de obtenção de insights.

# 