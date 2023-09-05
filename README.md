# Engenharia_de_Dados_Cotacao_Criptomoedas
O mercado de criptomoedas tem experimentado um crescimento exponencial nos últimos anos, com uma variedade cada vez maior de ativos digitais disponíveis para compra, venda e negociação. Para acompanhar a volatilidade e as flutuações de preços desses ativos, surgiram diversos projetos e ferramentas de cotação, sendo o CoinMarketCap um dos mais renomados e utilizados, e que usaremos para cotação dos ativos escolhidos.

# CoinMarketCap
Conforme comentado, o CoinMarketCap é um site que rastreia e fornece informações sobre uma ampla gama de criptomoedas, incluindo seus preços em tempo real, capitalização de mercado, volume de negociação e muito mais. Ele atua como uma plataforma de referência para investidores, traders, entusiastas de criptomoedas e qualquer pessoa interessada em acompanhar o mercado digital.

# Projeto
Conforme explicado, explanado, e visando a coleta e organização dos dados (que serão coletados tanto via web scraping quanto API), para concluir essa tarefa, e viabilizar o relatório à equipe de Dados, separei o projeto em algumas etapas, sendo elas:

# 1) Configuração de Acessos
- Visando uma melhor organização das informações de configurações, inseri as informações necessárias, e de acessos, em um arquivo json, de nome 'data' - localizado dentro da pasta utils, nesse arquivo há informações pertinentes a fonte extraída, configurações quanto ao acesso à tabela de banco de dados PostgreSQL usado, configurações API da Coin, credenciais da conta cloud AWS e se eu desejo coletar x moedas (melhores posicionadas no mercado, deixando a coins vazia (coins = []), e inserindo o limite de moedas inseridas no documento) ou moedas pontuais, pré-selecionadas pelo usuário;

# 2) criei um processo ETL:
- E: Extração dos dados respectivos oriundos da fonte https://coinmarketcap.com/pt-br/, a partir do acréscimo da moeda na url (exemplo: https://coinmarketcap.com/pt-br/currencies/bitcoin/), e buscando, na classe específica - do html, a classe que armazena os dados relacionados à moeda, sendo eles - os dados: nome da moeda, seu preço, variação de 1h e período. Além desses atributos, coletaremos a data e hora da captura, para montarmos uma base histórica.

- T: Posterior à coleta dos dados, e visando a geração de um relatório formal relacionado às cotações, tratei os dados, transformei em dicionário - pela facilidade de trabalhar como dataframe, e adicionei ao dataframe.

- L: Logo após os tratamentos, carreguei os dados em um arquivo csv - nomeado com a estrutura padrão: 'Moedas_[%Y%m%d].csv', um arquivo já tratado, limpo e em conformidade, disponível para ser utilizado como ferramenta para obtenção de insights.

# 3) criei um processo EL:
- E: Para validar a garantia dos dados, para a base que estou montando, extraí o html da página da moeda, página essa que contém as informações que coletei.

- L: Como a intenção é justamente usar como garantia de integridade, salvei o html em um arquivo txt, com a estrutura sendo a seguinte: 'html_[nome_moeda]_[data_captura].txt' - datacaptura sendo no formato %Y%m%d.

--- FAZER
# 4) orquestrei com Airflow
- Como a intenção é montar um histórico, usei o Apache Airflow para orquestar os códigos. As coletas serão realizadas a cada 5 minutos, diariamente, 7 dias por semana, durante todos os dias do ano.