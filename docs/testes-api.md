# Testes de API — Swagger Petstore v2

## Visão geral

| Item | Detalhe |
|------|---------|
| **API alvo** | Swagger Petstore v2 |
| **Base URL** | `https://petstore.swagger.io/v2` |
| **Ferramenta** | Postman + Newman |
| **Collection** | `api/postman/petstore_collection.json` |
| **Execução** | `npm run api:test` |
| **CI** | GitHub Actions — job `api-tests` |

### Números da suíte

| Métrica | Valor |
|---------|-------|
| Requests | 21 |
| Assertions | 48 |
| Falhas | 0 |

---

## Estratégia

A suíte cobre **todos os endpoints expostos** dos grupos `Pet`, `Store` e `User` da especificação Petstore v2, seguindo estes princípios:

1. **Cobertura completa** — cada endpoint publicado possui ao menos um teste
2. **Dados dinâmicos** — IDs e usernames gerados em runtime para evitar colisões em ambiente público
3. **Fluxo stateful** — endpoints que dependem de entidades criadas anteriormente na mesma execução respeitam a ordem do CRUD
4. **Asserções claras** — nomes descritivos que indicam exatamente qual contrato falhou na saída do Newman

### Inicialização dinâmica

Um script de `prerequest` global gera variáveis únicas por execução:

| Variável | Exemplo de uso |
|----------|---------------|
| `petId` | Identificador do pet no ciclo CRUD |
| `orderId` | Identificador do pedido no grupo Store |
| `username`, `password` | Credenciais do usuário de teste |
| `petName`, `petUpdatedName`, `petFinalName` | Nomes para criação e atualização |
| `userFirstName`, `userUpdatedFirstName` | Nomes para criação e atualização |
| `userEmail`, `userUpdatedEmail` | Emails para criação e atualização |

---

## Grupo Pet

### 1. Listar pets por status

| | |
|-|-|
| **Endpoint** | `GET /pet/findByStatus` |
| **Validações** | Status `200`, resposta é array, array tem pelo menos 1 item |
| **Propósito** | Consulta pública mais simples do grupo Pet |

### 2. Listar pets por tags

| | |
|-|-|
| **Endpoint** | `GET /pet/findByTags` |
| **Validações** | Status `200`, resposta é array |
| **Propósito** | Cobertura do endpoint de busca alternativo |

### 3. Criar pet

| | |
|-|-|
| **Endpoint** | `POST /pet` |
| **Validações** | Status `200`, `id` e `name` correspondem aos valores gerados |
| **Propósito** | Criação do pet que sustenta os testes subsequentes do ciclo CRUD |

### 4. Buscar pet por ID

| | |
|-|-|
| **Endpoint** | `GET /pet/{petId}` |
| **Validações** | Status `200`, `id` corresponde ao `petId` criado |
| **Depende de** | Criar pet (#3) |

### 5. Atualizar pet por formulário

| | |
|-|-|
| **Endpoint** | `POST /pet/{petId}` |
| **Validações** | Status `200`, resposta confirma operação no `petId` esperado |
| **Depende de** | Criar pet (#3) |

### 6. Upload de imagem do pet

| | |
|-|-|
| **Endpoint** | `POST /pet/{petId}/uploadImage` |
| **Validações** | Status `200`, mensagem indica upload realizado |
| **Observação** | Pode surgir warning de depreciação no stack multipart — não invalida o teste |

### 7. Atualizar pet completo

| | |
|-|-|
| **Endpoint** | `PUT /pet` |
| **Validações** | Status `200`, `status` é `pending`, `name` atualizado |
| **Depende de** | Criar pet (#3) |

### 8. Excluir pet

| | |
|-|-|
| **Endpoint** | `DELETE /pet/{petId}` |
| **Validações** | Status `200`, resposta confirma exclusão do `petId` |

### 9. Confirmar pet excluído

| | |
|-|-|
| **Endpoint** | `GET /pet/{petId}` (após exclusão) |
| **Validações** | Status `404`, mensagem indica pet não encontrado |
| **Propósito** | Fecha o ciclo CRUD com prova do estado final |

---

## Grupo Store

### 10. Consultar inventário

| | |
|-|-|
| **Endpoint** | `GET /store/inventory` |
| **Validações** | Status `200`, resposta é objeto com pelo menos uma chave |

### 11. Criar pedido

| | |
|-|-|
| **Endpoint** | `POST /store/order` |
| **Validações** | Status `200`, `id` corresponde ao `orderId`, `petId` corresponde ao usado na execução |

### 12. Buscar pedido por ID

| | |
|-|-|
| **Endpoint** | `GET /store/order/{orderId}` |
| **Validações** | Status `200`, `id` corresponde ao `orderId` |
| **Depende de** | Criar pedido (#11) |

### 13. Excluir pedido

| | |
|-|-|
| **Endpoint** | `DELETE /store/order/{orderId}` |
| **Validações** | Status `200`, resposta confirma exclusão do `orderId` |

---

## Grupo User

### 14. Criar usuário

| | |
|-|-|
| **Endpoint** | `POST /user` |
| **Validações** | Status `200`, resposta confirma operação |

### 15. Criar usuários com array

| | |
|-|-|
| **Endpoint** | `POST /user/createWithArray` |
| **Validações** | Status `200`, resposta contém `ok` |

### 16. Criar usuários com lista

| | |
|-|-|
| **Endpoint** | `POST /user/createWithList` |
| **Validações** | Status `200`, resposta contém `ok` |

### 17. Buscar usuário por username

| | |
|-|-|
| **Endpoint** | `GET /user/{username}` |
| **Validações** | Status `200`, `username` e `email` correspondem aos esperados |
| **Depende de** | Criar usuário (#14) |

### 18. Atualizar usuário

| | |
|-|-|
| **Endpoint** | `PUT /user/{username}` |
| **Validações** | Status `200`, resposta confirma operação |

### 19. Login do usuário

| | |
|-|-|
| **Endpoint** | `GET /user/login` |
| **Validações** | Status `200`, mensagem contém indicação de sessão iniciada |

### 20. Logout do usuário

| | |
|-|-|
| **Endpoint** | `GET /user/logout` |
| **Validações** | Status `200`, mensagem contém `ok` |

### 21. Excluir usuário

| | |
|-|-|
| **Endpoint** | `DELETE /user/{username}` |
| **Validações** | Status `200`, resposta confirma exclusão do `username` |

---

## Resumo da cobertura

| Grupo | Endpoints | Requests | Ordem |
|-------|-----------|----------|-------|
| Pet | 8 | 9 (inclui confirmação de exclusão) | #1 – #9 |
| Store | 4 | 4 | #10 – #13 |
| User | 8 | 8 | #14 – #21 |
| **Total** | **20** | **21** | |

---

## Execução

```bash
# Local
npm install
npm run api:test

# CI (GitHub Actions)
npm ci
npm run api:test
```

---

## Limitações conhecidas

- A API Petstore é pública e compartilhada — instabilidades de disponibilidade ou persistência podem causar falhas intermitentes
- A suíte depende da ordem de execução para endpoints que consomem entidades criadas na mesma run
- Não há mock local; todos os testes atingem o serviço remoto

---

## Arquivos relacionados

- `api/postman/petstore_collection.json` — Collection Postman
- `api/postman/petstore_environment.json` — Variáveis de ambiente
- `package.json` — Script `api:test`
- `.github/workflows/ci.yml` — Pipeline CI
