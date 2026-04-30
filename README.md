# Projeto de prova de automação QA

Repositório único, em português brasileiro, para a prova de testes e qualidade de software. A proposta é reunir duas frentes no mesmo projeto:

- automação de API do Swagger Petstore com Postman/Newman
- automação web E2E do SauceDemo com Python e Selenium

O projeto já saiu da fundação estrutural e agora possui a suíte inicial de API executável localmente com Newman. As próximas entregas continuam focadas em automação web, CI e acabamento para apresentação.

## Objetivo da prova

Entregar um projeto apresentável que permita:

- organizar API, web e CI no mesmo repositório
- implementar a suíte de API para User, Store e Pet
- implementar o fluxo E2E do SauceDemo com login, carrinho e checkout
- integrar as duas frentes ao GitHub Actions
- explicar a solução em aula com estrutura legível e comandos previsíveis

## Estado atual

No estado atual, o projeto já possui:

- estrutura inicial de pastas para API, web e CI
- collection Postman da Petstore em `api/postman/petstore_collection.json`
- execução local da suíte de API por `npm run api:test`
- arquivo `package.json` com dependência de Newman e scripts da frente API
- arquivo `requirements.txt` preparando a stack Python da automação web
- arquivo `.env.example` para configuração segura da frente web

Ainda **não** existem nesta etapa:

- testes Selenium implementados
- workflow funcional de GitHub Actions
- evidências finais da execução web e do CI

Esses itens entram nas próximas slices.

## Estrutura do repositório

```text
.
├── .github/
│   └── workflows/
├── api/
│   └── postman/
│       ├── petstore_collection.json
│       └── petstore_environment.json
├── web/
│   ├── config/
│   ├── pages/
│   └── tests/
├── package.json
├── requirements.txt
├── .env.example
└── README.md
```

## Stacks e convenções escolhidas

### API

- Postman para modelagem e export da collection
- Newman para execução local e futura execução no CI
- collection localizada em `api/postman/petstore_collection.json`
- ambiente local em `api/postman/petstore_environment.json`

Cobertura atual da suíte API:

- **Pet**: listagem por status com validação de status code e formato da resposta
- **Store**: consulta de inventário com validação de objeto retornado
- **User**: login e logout com validação de sessão e encerramento

Script disponível em `package.json`:

```bash
npm run api:test
```

### Web

- Python
- Selenium
- `webdriver-manager`
- `python-dotenv`
- `pytest` como runner de testes

Dependências preparadas em `requirements.txt` para instalação futura.

## Configuração por ambiente

O projeto segue o padrão de configuração fora do código-fonte.

Arquivo disponível:

- `.env.example`

Quando a automação web for implementada, a configuração local esperada será baseada nesse modelo. O arquivo real `.env` não deve ser versionado.

## Próximas entregas previstas

- **S03**: automação web SauceDemo com Selenium
- **S04**: integração contínua para API e web
- **S05**: README final, evidências e acabamento para apresentação

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
pip install -r requirements.txt
```

A execução dos testes web será adicionada quando a suíte Selenium existir.

## Observações para apresentação

- O repositório foi estruturado para ficar simples de explicar em aula.
- A separação entre API, web e CI é intencional para reduzir confusão.
- Comentários no código serão mantidos apenas quando forem realmente necessários.
- O histórico incremental de commits será tratado como parte do entregável.
- A suíte API prioriza cenários representativos e estáveis para reduzir dependência de comportamento inconsistente da Petstore pública.
