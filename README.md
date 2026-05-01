# Projeto de Prova de Automação QA

Repositório único para a prova de testes e qualidade de software, reunindo:

- automação de API do Swagger Petstore com Postman/Newman
- automação web E2E do SauceDemo com Python e Selenium
- pipeline GitHub Actions para as duas frentes

## Tecnologias usadas

### API

- Postman
- Newman
- Node.js

### Web

- Python 3
- Selenium
- webdriver-manager
- python-dotenv
- pytest

### CI/CD

- GitHub Actions

## Estrutura do projeto

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

## Instalação

### 1. Clonar o repositório

```bash
git clone <url-do-repositorio>
cd prova-qa
```

### 2. Instalar dependências da API

```bash
npm install
```

### 3. Instalar dependências da automação web

```bash
python -m pip install -r requirements.txt
```

### 4. Configurar ambiente da automação web

Copie o arquivo `.env.example` para `.env` se quiser personalizar o ambiente:

```bash
cp .env.example .env
```

Variáveis disponíveis:

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

## Execução

### Executar automação API

```bash
npm run api:test
```

Cobertura atual:

- Pet
- Store
- User

### Executar automação web

```bash
python -m pytest web/tests/test_checkout_e2e.py -q
```

Fluxo atual:

- login
- adição de produto ao carrinho
- carrinho
- checkout
- finalização da compra

### Executar pipeline localmente por equivalência

Os mesmos comandos usados no CI são:

```bash
npm run api:test
python -m pytest web/tests/test_checkout_e2e.py -q
```

## Documentação detalhada dos testes

Documentações dedicadas por frente:

- `docs/testes-api.md`
- `docs/testes-web.md`

## Pipeline

O workflow do GitHub Actions está em:

- `.github/workflows/ci.yml`

Jobs configurados:

- `api-tests`
- `web-tests`

## Prints do funcionamento

> Observação: o enunciado pede prints do funcionamento. A pasta de evidências pode ser mantida no repositório com capturas reais feitas antes da entrega final.

### Sugestão de prints para incluir

- execução verde da automação API no terminal
- execução verde da automação web no terminal
- execução da aba Actions no GitHub com os jobs `api-tests` e `web-tests`
- execução visual do SauceDemo com login/carrinho/checkout (opcional)

### Caminhos recomendados para evidências

```text
/docs/evidencias/api-newman.png
/docs/evidencias/web-pytest.png
/docs/evidencias/github-actions.png
/docs/evidencias/saucedemo-checkout.png
```

## Boas práticas aplicadas

- repositório único para as duas automações
- Page Objects na automação web
- waits explícitos no Selenium
- asserções legíveis na API e na web
- configuração por ambiente sem segredos no código
- pipeline separada por job para facilitar leitura de falhas

## Observações finais

- a automação API cobre todos os endpoints expostos dos grupos principais da Petstore (Pet, Store e User)
- a automação web cobre um fluxo E2E completo do SauceDemo
- a pipeline executa as duas frentes como pedido no enunciado
