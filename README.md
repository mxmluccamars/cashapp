uvicorn app.main:app --reload --reload-exclude "*.db" --reload-exclude "*.db-journal"

arquivos

core/config: arquivos de configuração como nome do projeto, banco de dados, etc.

core/database: arquivos de configuração da base de dados

app/main: ponto de entrada do aplicativo

app/api/v1/router: ele agrupa as rotas pelo nome

app/api/v1/endpoints: arquivos de rotas

app/schemas: arquivos de schemas para validação de dados

app/services:  arquivos de regras de negócio

app/repositories: arquivos que mexem no banco de dados

app/models: arquivos que mapeiam objetos do banco de dados

flow:

endpoint recebe uma requisição -> o schema verifica se os dados estão no formato correto -> o service avalia as regras de negócio -> o repository faz a operação -> o model diz como o banco de dados deve ser mapeado -> o endpoint retorna o resultado



raciocionio para novas rotas:
1. criar modelo de dados
    como os dados serao salvos no banco de dados?

2. criar schema de dados
    como eu quero que o usuario me envie os dados e como vou retornar para ele?

3. criar repository
    como eu vou fazer a operação no banco de dados?

4. criar service
    como eu vou fazer a validação dos dados?

5. criar endpoint
    como eu vou receber e retornar os dados?

6. criar rota
    como o usuario vai fazer a requisição?
