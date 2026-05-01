# Prova QA — Automação de API e Web com CI

Este repositório apresenta uma solução única para a prova prática de Qualidade de Software, reunindo duas frentes de automação:

- **Automação de API** da Swagger Petstore com **Postman/Newman**
- **Automação web E2E** do SauceDemo com **Python, Selenium e pytest**

Além das suítes automatizadas, o projeto inclui **pipeline de integração contínua no GitHub Actions**, documentação detalhada dos testes e evidências visuais da execução.

---

## Objetivo do projeto

O projeto foi construído para atender aos requisitos da prova, cobrindo:

1. **API** — cobertura completa dos endpoints expostos dos grupos `Pet`, `Store` e `User` da Swagger Petstore v2
2. **Web** — fluxo ponta a ponta no SauceDemo com login, adição ao carrinho e finalização da compra
3. **CI/CD** — execução automatizada das duas frentes em pipeline
4. **Boas práticas** — organização clara, separação de responsabilidades, Page Objects, asserções legíveis e configuração por ambiente

---

## Tecnologias utilizadas

### Automação de API
- Postman
- Newman
- Node.js

### Automação Web
- Python 3
- Selenium
- pytest
- webdriver-manager
- python-dotenv

### Integração Contínua
- GitHub Actions

---

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
├── docs/
│   ├── evidencias/
│   ├── testes-api.md
│   └── testes-web.md
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
├── .env.example
├── package.json
├── pytest.ini
├── requirements.txt
├── README.md
└── ROTEIRO.md
```

---

## Cobertura implementada

### API — Swagger Petstore

A suíte de API cobre todos os endpoints expostos dos grupos principais da Petstore:

#### Pet
- `GET /pet/findByStatus`
- `GET /pet/findByTags`
- `POST /pet`
- `GET /pet/{petId}`
- `POST /pet/{petId}`
- `POST /pet/{petId}/uploadImage`
- `PUT /pet`
- `DELETE /pet/{petId}`

#### Store
- `GET /store/inventory`
- `POST /store/order`
- `GET /store/order/{orderId}`
- `DELETE /store/order/{orderId}`

#### User
- `POST /user`
- `POST /user/createWithArray`
- `POST /user/createWithList`
- `GET /user/{username}`
- `PUT /user/{username}`
- `GET /user/login`
- `GET /user/logout`
- `DELETE /user/{username}`

### Web — SauceDemo

A suíte web cobre o fluxo E2E principal:

- login com usuário válido
- acesso à tela de inventário
- adição de produto ao carrinho
- validação do item no carrinho
- início do checkout
- preenchimento das informações do comprador
- revisão do pedido
- finalização bem-sucedida da compra

---

## Como executar o projeto

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

### 4. Configurar variáveis de ambiente da automação web

Criar um `.env` a partir de `.env.example`:

```bash
cp .env.example .env
```

Exemplo de configuração:

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

---

## Execução local

### Rodar automação API

```bash
npm run api:test
```

### Rodar automação web

```bash
python -m pytest web/tests/test_checkout_e2e.py -q
```

### Rodar as duas frentes

```bash
npm run api:test
python -m pytest web/tests/test_checkout_e2e.py -q
```

---

## Integração contínua

A pipeline está definida em:

- `.github/workflows/ci.yml`

Jobs configurados:

- `api-tests`
- `web-tests`

A pipeline executa exatamente os mesmos comandos validados localmente.

---

## Documentação detalhada

O projeto possui documentação dedicada para cada frente de teste:

- `docs/testes-api.md` — documentação detalhada da suíte de API
- `docs/testes-web.md` — documentação detalhada da suíte web
- `ROTEIRO.md` — roteiro de apoio para apresentação e navegação do projeto

---

## Evidências

A pasta `docs/evidencias/` concentra imagens úteis para apresentação e comprovação do fluxo automatizado.

### Evidências web já presentes
- `docs/evidencias/01-login.png`
- `docs/evidencias/03-produto-no-carrinho.png`
- `docs/evidencias/06-checkout-resumo.png`
- `docs/evidencias/07-compra-finalizada.png`

### Evidências recomendadas para complementar
- `docs/evidencias/api-newman.png` — execução verde da suíte API no terminal
- `docs/evidencias/github-actions.png` — execução verde da pipeline no GitHub Actions

---

## Boas práticas aplicadas

- repositório único para API e web
- separação clara entre automação, configuração, documentação e pipeline
- uso de **Page Objects** na automação web
- waits explícitos para reduzir flaky tests
- asserções legíveis e orientadas a diagnóstico
- configuração por ambiente, sem hardcode de segredos
- histórico incremental de evolução no repositório

---

## Resultado atual

Verificação final validada localmente:

```bash
npm run api:test && python -m pytest web/tests/test_checkout_e2e.py -q
```

Resultado:

- **API**: 21 requests, 48 assertions, 0 failed
- **Web**: 1 teste E2E passando

---

## Observações finais

Este projeto foi estruturado para ser:

- executável localmente com comandos simples
- suficientemente organizado para manutenção, demonstração e evolução
- a automação API cobre todos os endpoints expostos dos grupos principais da Petstore (Pet, Store e User)
- a automação web cobre um fluxo E2E completo do SauceDemo
