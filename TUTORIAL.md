# Tutorial de Uso

Este tutorial explica como utilizar a Plataforma de Avaliacao da Sindrome do X Fragil do IBK, separado por perfil de usuario.

## Acesso ao Sistema

1. Abra o navegador e acesse `http://localhost:5000`.
2. Informe email e senha na tela de login.
3. Acesso padrao do administrador:
   - Email: `admin@sistema.com`
   - Senha: `admin123`

Apos o login, voce e direcionado ao painel inicial (Inicio), que mostra resumos de acordo com o seu perfil.

## Perfil Administrador (admin)

O administrador tem acesso total ao sistema.

### Cadastrar um Usuario

1. No menu, clique em **Usuarios**.
2. Clique em **Novo Usuario**.
3. Preencha nome, email, tipo (admin, profissional ou paciente), CPF e senha.
4. Para profissionais, informe CRM e especialidade (opcionais).
5. Clique em **Salvar**.

### Dar Acesso a um Paciente

Para que um paciente consiga entrar no sistema e ver os proprios resultados, e preciso criar um usuario do tipo paciente com o MESMO CPF usado no cadastro do paciente:

1. Cadastre o paciente normalmente (menu **Pacientes**), informando o CPF.
2. No menu **Usuarios**, clique em **Novo Usuario**.
3. Escolha o tipo **paciente** e informe o mesmo CPF do cadastro do paciente, digitado exatamente da mesma forma (com os mesmos pontos e tracos).
4. Informe email e senha, que serao as credenciais de login do paciente.
5. Ao entrar, o paciente vera apenas as avaliacoes vinculadas ao CPF dele.

Se o CPF for digitado diferente nos dois cadastros, o paciente entra no sistema mas nao enxerga nenhum resultado.

### Cadastrar um Sintoma

1. No menu, clique em **Sintomas**.
2. Clique em **Novo Sintoma**.
3. Preencha nome, descricao, categoria, ordem e os pesos.
4. Deixe o peso feminino em branco quando o sintoma nao se aplica a mulheres.
5. Clique em **Salvar**.

O administrador tambem pode cadastrar pacientes e realizar avaliacoes, da mesma forma que o profissional. No painel inicial, o administrador e o profissional veem um grafico com a distribuicao dos resultados (Indicado e Sem Indicacao).

## Perfil Profissional

O profissional cadastra pacientes e realiza avaliacoes. Ele visualiza apenas os pacientes e relatorios que cadastrou.

### Cadastrar um Paciente

1. No menu, clique em **Pacientes**.
2. Clique em **Novo Paciente**.
3. Preencha nome, data de nascimento, sexo, CPF, contato e historico familiar.
4. Clique em **Salvar**.

### Buscar um Paciente

1. No menu, clique em **Pacientes**.
2. Digite parte do nome ou do CPF no campo de busca e clique em **Buscar**.
3. Clique em **Limpar** para voltar a lista completa.

### Realizar uma Avaliacao

1. No menu, clique em **Avaliacoes** e depois em **Nova Avaliacao** (ou clique em **Avaliar** na lista de pacientes).
2. Selecione o paciente.
3. Marque os sintomas presentes no checklist.
   - Para pacientes do sexo feminino, o sintoma Macro-orquidismo nao aparece.
4. Escreva observacoes se necessario.
5. Clique em **Calcular e Salvar**.
6. O sistema calcula o score no servidor e exibe o relatorio com o resultado.

### Entender o Resultado

- O score e a soma dos pesos dos sintomas marcados.
- Para homens, o resultado e **Indicado para Teste Genetico** se o score for maior que 0.56.
- Para mulheres, o resultado e **Indicado para Teste Genetico** se o score for maior que 0.55.
- O relatorio mostra de forma destacada se o resultado foi Indicado (vermelho) ou Sem Indicacao (verde).

## Perfil Paciente

O paciente apenas visualiza os resultados das proprias avaliacoes.

1. Apos o login, o painel inicial mostra a lista **Meus Resultados**.
2. Clique em **Ver resultado** para abrir o relatorio completo.
3. O paciente nao pode cadastrar nem editar nada.

## Consultar Relatorios

1. No menu, clique em **Relatorios**.
2. A lista mostra as avaliacoes com data, score e resultado.
3. Use o filtro de **Data** para ver apenas as avaliacoes de um dia especifico.
4. O administrador tambem pode filtrar por **Profissional**, escolhendo o responsavel na lista.
5. Clique em **Ver detalhes** para abrir o relatorio completo.

O profissional ve apenas os relatorios das avaliacoes que ele mesmo realizou. O administrador ve todos.

## Exportar o Relatorio

Na tela de detalhes do relatorio, estao disponiveis duas opcoes de exportacao:

- **Exportar CSV**: baixa um arquivo com os dados da avaliacao e a lista de sintomas.
- **Imprimir / PDF**: abre a janela de impressao do navegador. Escolha a opcao "Salvar como PDF" para gerar um arquivo PDF. O layout de impressao esconde os menus e botoes, mostrando apenas o relatorio.

## Alterar a Senha

1. No menu, clique em **Perfil**.
2. No formulario de edicao, informe a senha atual e a nova senha.
3. Clique em **Salvar**.
