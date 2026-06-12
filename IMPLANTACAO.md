# Guia de Implantacao

Este documento descreve como implantar e configurar a Plataforma de Avaliacao da Sindrome do X Fragil do IBK.

## Requisitos

- Docker e Docker Compose instalados.
- Porta 5000 livre para a aplicacao web.
- Porta 3306 livre para o banco MySQL.

Para rodar sem Docker, e necessario ter Python 3.11 e um servidor MySQL 8.0 instalados.

## Implantacao com Docker (recomendado)

1. Copie a pasta do projeto para o servidor.
2. Acesse a pasta do projeto pelo terminal:

```
cd ExpCriativaTerceiroSemestre-main
```

3. Construa e inicie os containers:

```
docker compose up --build
```

4. Aguarde o MySQL iniciar. A aplicacao espera o banco ficar disponivel antes de iniciar.
5. Acesse `http://localhost:5000`.

Para rodar em segundo plano:

```
docker compose up --build -d
```

Para parar os containers:

```
docker compose down
```

Para parar e apagar os dados do banco:

```
docker compose down -v
```

## Variaveis de Ambiente

As variaveis sao definidas no arquivo `docker-compose.yml`:

| Variavel | Descricao | Valor padrao |
|----------|-----------|--------------|
| DATABASE_URL | String de conexao com o banco. | mysql+pymysql://root:root123@db:3306/xfragil |
| SECRET_KEY | Chave secreta da aplicacao Flask. | ibk-xfragil-chave-2024 |
| MYSQL_ROOT_PASSWORD | Senha do usuario root do MySQL. | root123 |
| MYSQL_DATABASE | Nome do banco criado no MySQL. | xfragil |

Recomenda-se alterar SECRET_KEY e as senhas em um ambiente real.

## Inicializacao do Banco

- O arquivo `init.sql` e executado automaticamente na primeira vez que o container do MySQL e criado.
- Ele cria o banco `xfragil`, todas as tabelas e insere os 12 sintomas iniciais.
- O usuario administrador padrao (`admin@sistema.com` / `admin123`) e criado pela aplicacao no momento em que ela inicia.

## Implantacao sem Docker

1. Instale o MySQL 8.0 e crie o banco executando o arquivo `init.sql`:

```
mysql -u root -p < init.sql
```

2. Crie um ambiente virtual e instale as dependencias:

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure a variavel de ambiente DATABASE_URL apontando para o seu MySQL local. Exemplo no Windows (PowerShell):

```
$env:DATABASE_URL = "mysql+pymysql://root:suasenha@localhost:3306/xfragil"
```

4. Inicie a aplicacao:

```
python app.py
```

5. Acesse `http://localhost:5000`.

## Solucao de Problemas

- **A aplicacao nao conecta ao banco**: aguarde alguns segundos, pois o MySQL pode demorar para iniciar. A aplicacao tenta reconectar automaticamente.
- **Porta em uso**: altere o mapeamento de portas no `docker-compose.yml` (ex: trocar 5000 por outra porta).
- **Erro de autenticacao do MySQL**: confirme se a senha em DATABASE_URL e a mesma de MYSQL_ROOT_PASSWORD.
- **Dados antigos atrapalhando**: use `docker compose down -v` para recriar o banco do zero.
