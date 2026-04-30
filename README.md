# Projeto de prova de automação QA

Repositório único, em português brasileiro, para a prova de testes e qualidade de software. A proposta reúne duas frentes no mesmo projeto:

- automação de API do Swagger Petstore com Postman/Newman
- automação web E2E do SauceDemo com Python e Selenium

Neste momento, o projeto já possui as duas automações principais executáveis localmente e uma pipeline GitHub Actions preparada para rodar ambas. Falta o acabamento final de documentação, evidências e narrativa de apresentação.

## Objetivo da prova

Entregar um projeto apresentável que permita:

- organizar API, web e CI no mesmo repositório
- implementar a suíte de API para User, Store e Pet
- implementar o fluxo E2E do SauceDemo com login, carrinho e checkout
- integrar as duas frentes ao GitHub Actions
- explicar a solução em aula com estrutura legível e comandos previsíveis

## Estado atual

No estado atual, o projeto já possui:

- estrutura única para API, web e CI
- collection Postman da Petstore em `api/postman/petstore_collection.json`
- execução local da suíte de API por `npm run api:test`
- suíte web Selenium em Python com Page Objects dentro de `web/`
- execução local do fluxo E2E web por `python -m pytest web/tests/test_checkout_e2e.py -q`
- workflow GitHub Actions em `.github/workflows/ci.yml`
- `package.json` com dependência de Newman e scripts da frente API
- `requirements.txt` com a stack da frente web
- `.env.example` com configuração de ambiente da automação web

Ainda **não** existem nesta etapa:

- README final com evidências visuais da execução
- narrativa final de apresentação e troubleshooting consolidado

Esses itens entram na próxima slice.

## Estrutura do repositório

```text
.
├── .github/
│   └── workflows/
│       └── ci.yml
├── api/
│   └── postman/
│       ├── petstore_collection.json
│       └── petstore_environment.json
├── web/
│   ├── config/
│   │   └── settings.py
│   ├── pages/
│   │   ├── cart_page.py
│   │   ├── checkout_page.py
│   │   ├── inventory_page.py
│   │   └── login_page.py
│   ├── tests/
│   │   └── test_checkout_e2e.py
│   ├── conftest.py
│   └── driver_factory.py
├── package.json
├── requirements.txt
├── pytest.ini
├── .env.example
└── README.md
```

## Stacks e convenções escolhidas

### API

- Postman para modelagem e export da collection
- Newman para execução local e execução no CI
- collection localizada em `api/postman/petstore_collection.json`
- ambiente local em `api/postman/petstore_environment.json`

Cobertura atual da suíte API:

- **Pet**: listagem por status com validação de status code e formato da resposta
- **Store**: consulta de inventário com validação de objeto retornado
- **User**: login e logout com validação de sessão e encerramento

Comando disponível:

```bash
npm run api:test
```

### Web

- Python
- Selenium
- `webdriver-manager`
- `python-dotenv`
- `pytest`
- Page Objects para separar login, inventário, carrinho e checkout
- waits explícitos nas transições principais do fluxo

Cobertura atual da suíte web:

- login com usuário de treino
- adição do produto `Sauce Labs Backpack` ao carrinho
- acesso ao carrinho
- checkout com preenchimento de dados
- finalização com confirmação de pedido

Comando disponível:

```bash
python -m pytest web/tests/test_checkout_e2e.py -q
```

## Configuração por ambiente

O projeto segue o padrão de configuração fora do código-fonte.

Arquivo disponível:

- `.env.example`

Variáveis previstas para a automação web:

```env
BASE_URL=https://www.saucedemo.com/
LOGIN_USER=standard_user
LOGIN_PASSWORD=secret_sauce
BROWSER=chrome
CHROME_BINARY=
HEADLESS=true
IMPLICIT_WAIT_SECONDS=0
EXPLICIT_WAIT_SECONDS=10
```

Para uso local, copie `.env.example` para `.env` se quiser customizar valores. O arquivo real `.env` não deve ser versionado.

## Integração contínua com GitHub Actions

A pipeline está definida em:

- `.github/workflows/ci.yml`

Jobs atuais:

- **API - Newman Petstore**
- **Web - Selenium SauceDemo**

A proposta do workflow é simples:

- o job de API faz checkout, instala Node e executa `npm ci` + `npm run api:test`
- o job web faz checkout, instala Python, instala Google Chrome no runner e executa `python -m pip install -r requirements.txt` + `python -m pytest web/tests/test_checkout_e2e.py -q`

Isso deixa claro na aba Actions qual frente falhou: API ou web.

## Comandos disponíveis

### API

Instalar dependências Node:

```bash
npm install
```

Executar a suíte de API:

```bash
npm run api:test
```

A saída do Newman mostra o grupo, o request e a asserção que falhou, o que facilita a explicação em aula e o diagnóstico local.

### Web

Instalar dependências Python:

```bash
python -m pip install -r requirements.txt
```

Executar a suíte web:

```bash
python -m pytest web/tests/test_checkout_e2e.py -q
```

Se quiser visualizar o navegador durante a execução, ajuste `HEADLESS=false` no `.env`.

## Próxima entrega prevista

- **S05**: README final, evidências e acabamento para apresentação

## Observações para apresentação

- O repositório foi estruturado para ficar simples de explicar em aula.
- A separação entre API, web e CI é intencional para reduzir confusão.
- Comentários no código foram mantidos no mínimo; a legibilidade vem da estrutura e dos nomes.
- O histórico incremental de commits continua sendo tratado como parte do entregável.
- A suíte API prioriza cenários representativos e estáveis para reduzir dependência de comportamento inconsistente da Petstore pública.
- A suíte web usa Page Objects e waits explícitos para aderir ao guia da disciplina e reduzir flakiness.
- A pipeline usa os mesmos comandos já validados localmente, reduzindo diferença entre máquina de desenvolvimento e CI.
