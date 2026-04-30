# Projeto de prova de automação QA

Repositório único, em português brasileiro, para a prova de testes e qualidade de software.

O projeto entrega:

- automação de API do Swagger Petstore com Postman/Newman
- automação web E2E do SauceDemo com Python e Selenium
- pipeline GitHub Actions para as duas frentes
- organização pensada para apresentação em aula

## Visão geral

Este trabalho foi estruturado para atender ao enunciado da prova com foco em três pontos:

1. **execução real** das automações API e web
2. **legibilidade** do repositório e do fluxo de testes
3. **explicabilidade** na apresentação

As duas frentes vivem no mesmo repositório, com comandos previsíveis, CI separado por job e documentação alinhada ao estado real do código.

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

### CI

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

## O que foi automatizado

### API — Swagger Petstore

Collection em:

- `api/postman/petstore_collection.json`

Cobertura atual:

- **Pet**: listagem por status
- **Store**: consulta de inventário
- **User**: login e logout

A suíte foi mantida em cenários representativos e mais estáveis da API pública para reduzir falsos negativos em demonstração e CI.

### Web — SauceDemo

Teste em:

- `web/tests/test_checkout_e2e.py`

Fluxo coberto:

- login com `standard_user`
- adição do produto `Sauce Labs Backpack` ao carrinho
- acesso ao carrinho
- checkout com preenchimento de dados
- finalização do pedido

A automação usa **Page Objects** e **waits explícitos**, seguindo o guia da disciplina.

## Configuração do ambiente

Arquivo base:

- `.env.example`

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

Se quiser customizar valores localmente:

1. copie `.env.example` para `.env`
2. ajuste o que precisar

O arquivo `.env` **não deve ser versionado**.

## Instalação

### Dependências da API

```bash
npm install
```

### Dependências da automação web

```bash
python -m pip install -r requirements.txt
```

## Execução local

### Rodar automação API

```bash
npm run api:test
```

### Rodar automação web

```bash
python -m pytest web/tests/test_checkout_e2e.py -q
```

### Rodar as duas frentes antes da apresentação

```bash
npm run api:test
python -m pytest web/tests/test_checkout_e2e.py -q
```

## Integração contínua

Workflow:

- `.github/workflows/ci.yml`

Jobs configurados:

- `api-tests`
- `web-tests`

Resumo:

- o job de API executa `npm ci` e `npm run api:test`
- o job de web instala Python, instala Chrome no runner e executa `python -m pytest web/tests/test_checkout_e2e.py -q`

A separação por job ajuda a identificar rapidamente se a falha veio da frente API ou da frente web.

## Evidências

### Evidência da suíte API

Comando validado localmente:

```bash
npm run api:test
```

Resultado esperado:

- requests dos grupos `Pet`, `Store` e `User`
- asserções verdes no Newman
- sumário final com zero falhas

Na validação final local deste projeto, a suíte API passou com:

- 4 requests executados
- 10 asserções verdes
- 0 falhas

### Evidência da suíte web

Comando validado localmente:

```bash
python -m pytest web/tests/test_checkout_e2e.py -q
```

Resultado esperado:

- 1 teste passando
- fluxo completo de login, carrinho e checkout executado sem erro

Durante a estabilização final do projeto, esse teste foi executado repetidamente até ficar estável no ambiente local atual.

### Evidência da pipeline

Arquivo do workflow:

- `.github/workflows/ci.yml`

O workflow usa os mesmos comandos já validados localmente. Isso reduz a diferença entre execução manual e CI.

## Troubleshooting

### 1. API falhou no Newman

Possíveis causas:

- instabilidade momentânea da Petstore pública
- timeout temporário do serviço
- mudança de comportamento em endpoint público

O que fazer:

- rodar `npm run api:test` novamente
- verificar no terminal qual grupo/request falhou
- confirmar se a falha veio da API pública e não do projeto

### 2. Web falhou no Selenium

Possíveis causas:

- instabilidade momentânea do SauceDemo
- problema local com browser/driver
- diferença de ambiente em modo headless

O que fazer:

- rodar `python -m pytest web/tests/test_checkout_e2e.py -q` novamente
- se precisar observar visualmente, definir `HEADLESS=false` no `.env`
- verificar se o browser está instalado corretamente

### 3. CI falhou no GitHub Actions

O que verificar:

- qual job falhou: `api-tests` ou `web-tests`
- se o erro ocorreu no Newman ou no pytest
- se a falha foi de serviço externo ou de configuração do projeto

## Pontos fortes para explicar em aula

- repositório único para API, web e CI
- uso de Postman/Newman conforme o guia de API
- uso de Python + Selenium + Page Objects + waits explícitos conforme o guia web
- pipeline separada por jobs para leitura rápida de falhas
- histórico incremental de commits durante a evolução do trabalho

## Apresentação

Sugestão de roteiro curto:

1. mostrar a estrutura do repositório
2. abrir a collection da Petstore e explicar os grupos `Pet`, `Store` e `User`
3. mostrar o teste web e os Page Objects
4. executar localmente:
   - `npm run api:test`
   - `python -m pytest web/tests/test_checkout_e2e.py -q`
5. abrir `.github/workflows/ci.yml` e explicar os dois jobs
6. encerrar mostrando que README, código e pipeline estão alinhados

## Observações finais

- comentários foram mantidos no mínimo, priorizando nomes e estrutura claros
- a suíte API prioriza cenários representativos e mais estáveis da API pública
- a suíte web exigiu estabilização específica no checkout antes de sustentar o CI
- a documentação foi mantida fiel ao estado real do projeto, sem prometer o que não existe
