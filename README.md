# Projeto de prova de automação QA

Repositório único, em português brasileiro, para a prova de testes e qualidade de software. A proposta é reunir duas frentes no mesmo projeto:

- automação de API do Swagger Petstore com Postman/Newman
- automação web E2E do SauceDemo com Python e Selenium

Este repositório ainda está na fase de fundação estrutural. Nesta slice, o foco foi criar uma base clara para as próximas entregas, sem antecipar implementação que ainda não existe.

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
- arquivo `package.json` preparando a execução da suíte de API com Newman
- arquivo `requirements.txt` preparando a stack Python da automação web
- arquivo `.env.example` para configuração segura de credenciais e variáveis de ambiente

Ainda **não** existem nesta etapa:

- collection Postman da Petstore
- testes Selenium implementados
- workflow funcional de GitHub Actions
- evidências finais da execução

Esses itens entram nas próximas slices.

## Estrutura do repositório

```text
.
├── .github/
│   └── workflows/
├── api/
│   └── postman/
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
- caminho previsto da collection: `api/postman/petstore_collection.json`

Script preparado em `package.json`:

```bash
npm run api:test
```

Observação: o script depende da collection existir no caminho previsto. Isso será entregue na slice de API.

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

- **S02**: automação API Petstore com Postman/Newman
- **S03**: automação web SauceDemo com Selenium
- **S04**: integração contínua para API e web
- **S05**: README final, evidências e acabamento para apresentação

## Comandos previstos

### API

Instalar dependências Node:

```bash
npm install
```

Executar a suíte de API quando a collection existir:

```bash
npm run api:test
```

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
