# Prova QA — Automação de API e Web com CI

Projeto de automação de testes para a prova prática de **Qualidade de Software**, com duas frentes integradas em um único repositório:

| Frente | Alvo | Stack |
|--------|------|-------|
| **API** | Swagger Petstore v2 | Postman + Newman + Node.js |
| **Web E2E** | SauceDemo | Python + Selenium + pytest |

Pipeline de integração contínua no **GitHub Actions** executa ambas as suítes a cada push/PR na `main`.

---

## Resultados

| Suíte | Requests | Assertions | Falhas |
|-------|----------|------------|--------|
| API (Newman) | 21 | 48 | 0 |
| Web (pytest) | 1 teste E2E | 4 asserções | 0 |

---

## Estrutura do repositório

```text
.
├── .github/workflows/
│   └── ci.yml                          # Pipeline CI (API + Web)
├── api/postman/
│   ├── petstore_collection.json        # Collection Postman
│   └── petstore_environment.json       # Variáveis de ambiente
├── docs/
│   ├── evidencias/                     # Screenshots e capturas
│   ├── testes-api.md                   # Documentação da suíte API
│   └── testes-web.md                   # Documentação da suíte Web
├── web/
│   ├── config/
│   │   └── settings.py                 # Leitura de .env e configurações
│   ├── pages/
│   │   ├── login_page.py               # Page Object — Login
│   │   ├── inventory_page.py           # Page Object — Inventário
│   │   ├── cart_page.py                # Page Object — Carrinho
│   │   └── checkout_page.py            # Page Object — Checkout
│   ├── tests/
│   │   └── test_checkout_e2e.py        # Cenário E2E principal
│   ├── conftest.py                     # Fixtures do pytest
│   └── driver_factory.py              # Instanciação do WebDriver
├── .env.example
├── package.json
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## Cobertura

### API — Swagger Petstore v2

A suíte cobre **todos os endpoints expostos** dos três grupos principais:

<details>
<summary><strong>Pet</strong> — 8 endpoints</summary>

| Método | Endpoint | Teste |
|--------|----------|-------|
| `GET` | `/pet/findByStatus` | Listar pets por status |
| `GET` | `/pet/findByTags` | Listar pets por tags |
| `POST` | `/pet` | Criar pet |
| `GET` | `/pet/{petId}` | Buscar pet por ID |
| `POST` | `/pet/{petId}` | Atualizar pet por formulário |
| `POST` | `/pet/{petId}/uploadImage` | Upload de imagem |
| `PUT` | `/pet` | Atualizar pet completo |
| `DELETE` | `/pet/{petId}` | Excluir pet |

</details>

<details>
<summary><strong>Store</strong> — 4 endpoints</summary>

| Método | Endpoint | Teste |
|--------|----------|-------|
| `GET` | `/store/inventory` | Consultar inventário |
| `POST` | `/store/order` | Criar pedido |
| `GET` | `/store/order/{orderId}` | Buscar pedido por ID |
| `DELETE` | `/store/order/{orderId}` | Excluir pedido |

</details>

<details>
<summary><strong>User</strong> — 8 endpoints</summary>

| Método | Endpoint | Teste |
|--------|----------|-------|
| `POST` | `/user` | Criar usuário |
| `POST` | `/user/createWithArray` | Criar usuários com array |
| `POST` | `/user/createWithList` | Criar usuários com lista |
| `GET` | `/user/{username}` | Buscar usuário por username |
| `PUT` | `/user/{username}` | Atualizar usuário |
| `GET` | `/user/login` | Login |
| `GET` | `/user/logout` | Logout |
| `DELETE` | `/user/{username}` | Excluir usuário |

</details>

### Web — SauceDemo

O teste E2E cobre o fluxo principal de compra:

```
Login → Inventário → Adicionar ao carrinho → Carrinho → Checkout → Dados → Resumo → Compra finalizada
```

---

## Como executar

### Pré-requisitos

- **Node.js** 20+ e **npm**
- **Python** 3.12+ e **pip**
- **Google Chrome** instalado

### 1. Clonar e instalar

```bash
git clone <url-do-repositorio>
cd prova-qa

# Dependências API
npm install

# Dependências Web
python -m pip install -r requirements.txt
```

### 2. Configurar variáveis de ambiente (Web)

```bash
cp .env.example .env
```

Conteúdo do `.env`:

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

### 3. Executar

```bash
# Suíte API
npm run api:test

# Suíte Web
python -m pytest web/tests/test_checkout_e2e.py -q

# Ambas
npm run api:test && python -m pytest web/tests/test_checkout_e2e.py -q
```

---

## Integração contínua

A pipeline está em `.github/workflows/ci.yml` e roda automaticamente em push e PR para `main`.

| Job | Runner | O que faz |
|-----|--------|-----------|
| `api-tests` | Ubuntu + Node 20 | `npm ci && npm run api:test` |
| `web-tests` | Ubuntu + Python 3.12 + Chrome | `pytest` com `HEADLESS=true` |

Em caso de falha no job `web-tests`, screenshots e logs de debug são publicados como artefatos do workflow.

---

## Evidências visuais

A suíte web gera screenshots automaticamente em `docs/evidencias/`:

| Etapa | Arquivo |
|-------|---------|
| Tela de login | `01-login.png` |
| Inventário | `02-inventario.png` |
| Produto adicionado | `03-produto-no-carrinho.png` |
| Carrinho | `04-carrinho.png` |
| Checkout — dados | `05-checkout-informacoes.png` |
| Checkout — resumo | `06-checkout-resumo.png` |
| Compra finalizada | `07-compra-finalizada.png` |

Também disponível: `api-newman.png` com a execução verde da suíte API no terminal.

---

## Documentação detalhada

| Documento | Conteúdo |
|-----------|----------|
| [`docs/testes-api.md`](docs/testes-api.md) | Estratégia, detalhamento de cada teste, contratos validados |
| [`docs/testes-web.md`](docs/testes-web.md) | Fluxo E2E passo a passo, Page Objects, asserções |

---

## Boas práticas aplicadas

- **Repositório único** para API e Web, com separação clara de responsabilidades
- **Page Objects** na automação web para encapsular seletores e interações
- **Waits explícitos** para estabilidade em CI e ambientes headless
- **Dados dinâmicos** na API (IDs gerados em runtime) para evitar colisões
- **Configuração por ambiente** via `.env`, sem hardcode de segredos
- **Screenshots automáticos** como evidência de execução
- **Pipeline CI** reproduzível com os mesmos comandos da execução local
