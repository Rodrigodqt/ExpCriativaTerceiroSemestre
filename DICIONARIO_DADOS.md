# Dicionario de Dados

Plataforma de Avaliacao da Sindrome do X Fragil - Instituto Buko Kaesemodel (IBK).

O banco de dados foi modelado seguindo a Terceira Forma Normal (3FN). Todas as chaves estrangeiras possuem a regra ON DELETE CASCADE. O banco utiliza o MySQL 8.0 com charset utf8mb4.

## Visao Geral das Tabelas

| Tabela | Descricao |
|--------|-----------|
| usuarios | Pessoas que acessam o sistema (admin, profissional ou paciente). |
| pacientes | Pessoas avaliadas pela plataforma. |
| sintomas | Lista de sintomas usados na avaliacao, com seus pesos. |
| avaliacoes | Registro de cada avaliacao realizada para um paciente. |
| itens_avaliacao | Sintomas marcados (ou nao) em cada avaliacao. |

## Tabela: usuarios

Armazena os usuarios do sistema e suas credenciais de acesso.

| Campo | Tipo | Nulo | Chave | Descricao |
|-------|------|------|-------|-----------|
| id | INT (auto incremento) | Nao | PK | Identificador unico do usuario. |
| nome | VARCHAR(120) | Nao | | Nome completo do usuario. |
| email | VARCHAR(120) | Nao | UNIQUE | Email usado para login. Nao pode repetir. |
| senha_hash | VARCHAR(255) | Nao | | Senha criptografada com hash (Werkzeug). |
| tipo | VARCHAR(20) | Nao | | Perfil de acesso: admin, profissional ou paciente. |
| cpf | VARCHAR(14) | Sim | | CPF do usuario. |
| crm | VARCHAR(20) | Sim | | Registro profissional (CRM). Usado por profissionais. |
| especialidade | VARCHAR(120) | Sim | | Especialidade do profissional. |
| ativo | TINYINT(1) | Nao | | Indica se o usuario esta ativo (exclusao logica). |
| data_criacao | DATETIME | Sim | | Data e hora do cadastro. |

## Tabela: pacientes

Armazena os dados das pessoas avaliadas.

| Campo | Tipo | Nulo | Chave | Descricao |
|-------|------|------|-------|-----------|
| id | INT (auto incremento) | Nao | PK | Identificador unico do paciente. |
| nome | VARCHAR(120) | Nao | | Nome completo do paciente. |
| data_nascimento | DATE | Sim | | Data de nascimento do paciente. |
| sexo | VARCHAR(1) | Sim | | Sexo do paciente: M (masculino) ou F (feminino). |
| cpf | VARCHAR(14) | Sim | | CPF do paciente. |
| contato | VARCHAR(120) | Sim | | Telefone ou email de contato. |
| historico_familiar | TEXT | Sim | | Descricao do historico familiar relevante. |
| usuario_id | INT | Sim | FK -> usuarios.id | Usuario (profissional ou admin) que cadastrou o paciente. |
| ativo | TINYINT(1) | Nao | | Indica se o paciente esta ativo (exclusao logica). |
| data_criacao | DATETIME | Sim | | Data e hora do cadastro. |

## Tabela: sintomas

Armazena os sintomas utilizados nas avaliacoes e seus pesos por sexo.

| Campo | Tipo | Nulo | Chave | Descricao |
|-------|------|------|-------|-----------|
| id | INT (auto incremento) | Nao | PK | Identificador unico do sintoma. |
| nome | VARCHAR(120) | Nao | | Nome do sintoma. |
| descricao | TEXT | Sim | | Explicacao do sintoma. |
| categoria | VARCHAR(80) | Sim | | Agrupamento do sintoma (ex: Cognitivo, Fisico). |
| peso_masculino | FLOAT | Sim | | Peso do sintoma na avaliacao de pacientes do sexo masculino. |
| peso_feminino | FLOAT | Sim | | Peso do sintoma na avaliacao de pacientes do sexo feminino. Nulo quando nao se aplica (Macro-orquidismo). |
| ativo | TINYINT(1) | Nao | | Indica se o sintoma esta ativo (exclusao logica). |
| ordem | INT | Sim | | Ordem de exibicao do sintoma no checklist. |

## Tabela: avaliacoes

Armazena cada avaliacao realizada, com o score e o resultado calculados.

| Campo | Tipo | Nulo | Chave | Descricao |
|-------|------|------|-------|-----------|
| id | INT (auto incremento) | Nao | PK | Identificador unico da avaliacao. |
| paciente_id | INT | Sim | FK -> pacientes.id | Paciente avaliado. |
| usuario_id | INT | Sim | FK -> usuarios.id | Usuario que realizou a avaliacao. |
| data_avaliacao | DATETIME | Sim | | Data e hora em que a avaliacao foi feita. |
| score_total | FLOAT | Sim | | Soma dos pesos dos sintomas marcados. |
| limiar_aplicado | FLOAT | Sim | | Limiar usado na comparacao (0.56 homens, 0.55 mulheres). |
| resultado | VARCHAR(60) | Sim | | Resultado final: Indicado para Teste Genetico ou Sem Indicacao para Teste Genetico. |
| observacoes | TEXT | Sim | | Observacoes feitas pelo profissional. |
| data_criacao | DATETIME | Sim | | Data e hora do registro. |

## Tabela: itens_avaliacao

Tabela associativa que registra, para cada avaliacao, quais sintomas foram marcados.

| Campo | Tipo | Nulo | Chave | Descricao |
|-------|------|------|-------|-----------|
| id | INT (auto incremento) | Nao | PK | Identificador unico do item. |
| avaliacao_id | INT | Nao | FK -> avaliacoes.id (ON DELETE CASCADE) | Avaliacao a qual o item pertence. |
| sintoma_id | INT | Nao | FK -> sintomas.id (ON DELETE CASCADE) | Sintoma referenciado. |
| presente | TINYINT(1) | Nao | | Indica se o sintoma estava presente na avaliacao (1) ou nao (0). |

## Relacionamentos

- Um usuario pode cadastrar varios pacientes (1:N entre usuarios e pacientes).
- Um usuario pode realizar varias avaliacoes (1:N entre usuarios e avaliacoes).
- Um paciente pode ter varias avaliacoes (1:N entre pacientes e avaliacoes).
- Uma avaliacao possui varios itens de avaliacao (1:N entre avaliacoes e itens_avaliacao).
- Um sintoma pode aparecer em varios itens de avaliacao (1:N entre sintomas e itens_avaliacao).

## Observacoes sobre a Normalizacao (3FN)

- Cada tabela possui uma chave primaria propria e simples (id).
- Os atributos dependem apenas da chave primaria de sua tabela.
- Os sintomas ficam em uma tabela separada e sao referenciados pela tabela itens_avaliacao, evitando repeticao de dados na tabela avaliacoes.
- Os dados do paciente e do usuario nao sao repetidos na avaliacao, apenas referenciados por chave estrangeira.
