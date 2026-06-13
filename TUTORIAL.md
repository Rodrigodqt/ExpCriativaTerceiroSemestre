# Tutorial de Uso

Este tutorial explica como utilizar a Plataforma de Avaliação da Síndrome do X Frágil do IBK, separado por perfil de usuario.

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

1. No menu, clique em **Usuários**.
2. Clique em **Novo Usuário**.
3. Preencha nome, email, tipo (admin, profissional ou paciente), CPF e senha.
4. Para profissionais, informe CRM e especialidade (opcionais).
5. Clique em **Salvar**.

### Dar Acesso a um Paciente

Para que um paciente consiga entrar no sistema e ver os proprios resultados, e preciso criar um usuario do tipo paciente com o MESMO CPF usado no cadastro do paciente:

1. Cadastre o paciente normalmente (menu **Pacientes**), informando o CPF.
2. No menu **Usuários**, clique em **Novo Usuário**.
3. Escolha o tipo **paciente** e informe o mesmo CPF do cadastro do paciente, digitado exatamente da mesma forma (com os mesmos pontos e tracos).
4. Informe email e senha, que serao as credenciais de login do paciente.
5. Ao entrar, o paciente vera apenas as avaliações vinculadas ao CPF dele.

Se o CPF for digitado diferente nos dois cadastros, o paciente entra no sistema mas não enxerga nenhum resultado.

### Cadastrar um Sintoma

1. No menu, clique em **Sintomas**.
2. Clique em **Novo Sintoma**.
3. Preencha nome, descrição, categoria, ordem e os pesos.
4. Deixe o peso feminino em branco quando o sintoma não se aplica a mulheres.
5. Clique em **Salvar**.

O administrador tambem pode cadastrar pacientes e realizar avaliações, da mesma forma que o profissional. No painel inicial, o administrador e o profissional veem um grafico com a distribuição dos resultados (Indicado e Sem Indicação).

## Perfil Profissional

O profissional cadastra pacientes e realiza avaliações. Ele visualiza apenas os pacientes e relatórios que cadastrou.

### Cadastrar um Paciente

1. No menu, clique em **Pacientes**.
2. Clique em **Novo Paciente**.
3. Preencha nome, data de nascimento, sexo, CPF, contato e historico familiar.
4. Clique em **Salvar**.

### Buscar um Paciente

1. No menu, clique em **Pacientes**.
2. Digite parte do nome ou do CPF no campo de busca e clique em **Buscar**.
3. Clique em **Limpar** para voltar a lista completa.

### Realizar uma Avaliação

1. No menu, clique em **Avaliações** e depois em **Nova Avaliação** (ou clique em **Avaliar** na lista de pacientes).
2. Selecione o paciente.
3. Marque os sintomas presentes no checklist.
   - Para pacientes do sexo feminino, o sintoma Macro-orquidismo não aparece.
4. Escreva observações se necessario.
5. Clique em **Calcular e Salvar**.
6. O sistema calcula o score no servidor e exibe o relatório com o resultado.

### Entender o Resultado

- O score e a soma dos pesos dos sintomas marcados.
- Para homens, o resultado e **Indicado para Teste Genético** se o score for maior que 0.56.
- Para mulheres, o resultado e **Indicado para Teste Genético** se o score for maior que 0.55.
- O relatório mostra de forma destacada se o resultado foi Indicado (vermelho) ou Sem Indicação (verde).

## Perfil Paciente

O paciente apenas visualiza os resultados das proprias avaliações.

1. Apos o login, o painel inicial mostra a lista **Meus Resultados**.
2. Clique em **Ver resultado** para abrir o relatório completo.
3. O paciente não pode cadastrar nem editar nada.

## Consultar Relatórios

1. No menu, clique em **Relatórios**.
2. A lista mostra as avaliações com data, score e resultado.
3. Use o filtro de **Data** para ver apenas as avaliações de um dia especifico.
4. O administrador tambem pode filtrar por **Profissional**, escolhendo o responsavel na lista.
5. Clique em **Ver detalhes** para abrir o relatório completo.

O profissional ve apenas os relatórios das avaliações que ele mesmo realizou. O administrador ve todos.

## Exportar o Relatório

Na tela de detalhes do relatório, estão disponiveis duas opções de exportação:

- **Exportar CSV**: baixa um arquivo com os dados da avaliação e a lista de sintomas.
- **Imprimir / PDF**: abre a janela de impressão do navegador. Escolha a opção "Salvar como PDF" para gerar um arquivo PDF. O layout de impressão esconde os menus e botoes, mostrando apenas o relatório.

## Alterar a Senha

1. No menu, clique em **Perfil**.
2. No formulario de edição, informe a senha atual e a nova senha.
3. Clique em **Salvar**.
