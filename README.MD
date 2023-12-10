#<h1 style="color: blue;">Back-end (Next Logistics WMS)</h1>

## Definação e propósito

Este projeto é API de um sistema de WMS podendo ser utilizado em qualquer local que envolva movimentação de produto. Ele resolve o problema da utilização de registros em papel para historico de movimentações de produto ou ausencia do mesmo.

## Funcionamento interno
A API feita utilizando flask como framework principal. É possivel testar todas as rotas e funcionamento princiapis utilizando a biblioteca swagger.


### Banco de Dados

O sistema é feito utilizando sqlite e utiliza duas tabelas, uma responsável pelo controle do usúario e outra pelas movimentações no estoque. Caso o local que está sendo executado o arquivo não possua as tabelas, o próprio sistema se encarregar de criar. O sistema só vai lidar com as requisões se as mesmas atenderem o schemas previamente estabelecidos

####cadastro

Nome da coluna | Tipo | 
:--------- | :------: 
id | integer (primary_key)
nome | string(255)
senha| string(255)

####endereço
Nome da coluna | Tipo | 
:--------- | :------: 
id| integer (primary_key)
material | string(255)
quantidade| integer
sku| string(255)
rua| string(255)
posicao| string(255)
nome| string(255)
data_insercao| date

### Rotas

O sistema é composto por seis rotas:

* /atualizar_cadastro
* /cadastro
* /login
* /endereco
* /endereco_apagar
* /endereco_buscar

### Como executar

Será necessário garantir que todas as bibliotecas Python listadas no arquivo `requirements`.txt estejam instaladas. Após clonar o repositório, navegue até o diretório raiz por meio do terminal para executar os comandos a seguir.

**É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).**



```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.

**Pontos de atenção**

  Para uma completa utilização do sistema é necessário uma aplicação em front-end solicitando as requisições