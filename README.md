# User API

Esta é uma API desenvolvida em Python utilizando o framework FastAPI, projetada para fornecer cadastro de usuários utilizando a autenticação via JWT.

## Tecnologias Utilizadas

- **Python**: Linguagem de programação utilizada para o desenvolvimento do projeto.
- **FastAPI**: Framework moderno e performático para construção de APIs RESTful.
- **Pydantic**: Biblioteca utilizada para validação e serialização de dados.
- **Uvicorn**: Servidor ASGI utilizado para executar a aplicação.
- **PyJWT**: Biblioteca utilizada para geração e validação de tokens JWT.

## Instalação

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/flaviohnm/user-api.git
   cd user-api
   ```

2. **Crie um ambiente virtual** (recomendado):
   ```bash
   python -m venv env
   source env/bin/activate  # No Windows: env\Scripts\activate
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuração do Banco de Dados**:
   Caso o arquivo `users.db` não exista, ele será criado automaticamente ao iniciar a API.

## Uso

1. **Inicie a aplicação**:
   Execute o seguinte comando para iniciar o servidor FastAPI com Uvicorn:
   ```bash
   uvicorn main:app --reload
   ```

   A aplicação estará disponível em `http://127.0.0.1:8000/`.

2. **Documentação interativa**:
   Acesse `http://127.0.0.1:8000/docs` para visualizar e testar os endpoints utilizando a interface Swagger UI.

3. **Endpoints Disponíveis**:
   - `POST /token`: Gera um token JWT para autenticação.
   - `POST /users`: Adiciona um novo usuário (requer autenticação JWT).
   - `GET /users`: Retorna uma lista de todos os usuários (requer autenticação JWT).
   - `GET /users/{id}`: Retorna os detalhes de um usuário específico (requer autenticação JWT). | (em desenvolviemnto)
   - `PUT /users/{id}`: Atualiza as informações de um usuário específico (requer autenticação JWT). | (em desenvolviemnto)
   - `DELETE /users/{id}`: Remove um usuário específico (requer autenticação JWT). | (em desenvolviemnto)

## Validação dos Dados

Os seguintes campos devem ser enviados ao cadastrar um usuário:

- `nome`: Não pode ser vazio.
- `email`: Deve ser um endereço de e-mail válido.
- `cpf`: Deve ser um CPF válido no formato `XXX.XXX.XXX-XX`.
- `data_nascimento`: Deve ser uma data válida no formato `YYYY-MM-DD`.

## Script de Integração via CSV

Além da API, foi desenvolvido um script Python para importar usuários a partir de um arquivo CSV.

1. **Formato do arquivo CSV**:
   ```csv
   nome,email,cpf,data_nascimento
   Ana Silva,ana.silva@example.com,123.456.789-00,1990-05-14
   Bruno Souza,bruno.souza@example.com,987.654.321-00,1985-08-23
   ```

2. **Execução do script**:
   ```bash
   python scripts.py users.csv
   ```

3. **O que o script faz**:
   - Lê o arquivo CSV e extrai os dados dos usuários.
   - Gera um token JWT para autenticação.
   - Envia os dados para a API via requisição `POST /users`.
   - Exibe no console o status de cada requisição (sucesso ou erro).

## Estrutura do Projeto

- `main.py`: Arquivo principal que inicia a aplicação FastAPI e define os endpoints.
- `data/`: Diretório onde o arquivo `users.csv` é armazenado.
- `scripts.py`: Script para envio de dados de um arquivo CSV para a API.

## Licença

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais informações.

## Contato

Desenvolvido por Flavio Monteiro. Para mais informações, entre em contato via [GitHub](https://github.com/flaviohnm).

