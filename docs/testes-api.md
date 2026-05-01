# Documentação detalhada dos testes de API

## Visão geral

Esta suíte automatiza a API pública **Swagger Petstore v2** usando **Postman/Newman**.

- Base URL: `https://petstore.swagger.io/v2`
- Arquivo principal: `api/postman/petstore_collection.json`
- Comando de execução: `npm run api:test`
- Runner de CI: GitHub Actions (`.github/workflows/ci.yml`)

A coleção foi estruturada por domínio funcional da API:

- `Pet`
- `Store`
- `User`

O objetivo desta documentação é explicar **o que cada teste cobre**, **qual contrato valida** e **por que ele existe**.

---

## Estratégia da suíte

A suíte cobre **todos os endpoints expostos** dos grupos principais `Pet`, `Store` e `User` presentes na especificação Swagger Petstore v2.

### Princípios adotados

1. **Cobertura completa dos endpoints expostos**
   - Cada endpoint publicado nesses três grupos possui ao menos um teste correspondente na collection.

2. **Dados dinâmicos por execução**
   - IDs e usernames são gerados em runtime para reduzir colisões entre execuções locais e de CI.

3. **Asserções legíveis**
   - Os nomes dos testes foram escritos para deixar claro no terminal do Newman qual contrato falhou.

4. **Fluxo stateful quando necessário**
   - Alguns endpoints dependem de entidades criadas anteriormente na mesma execução, como pet, order e user.

5. **Ênfase em observabilidade**
   - A saída do Newman funciona como superfície principal de diagnóstico.

---

## Inicialização dinâmica da execução

A collection possui um script global de `prerequest` que inicializa, uma única vez por run:

- `petId`
- `orderId`
- `username`
- `password`
- `petName`
- `petUpdatedName`
- `petFinalName`
- `userFirstName`
- `userUpdatedFirstName`
- `userEmail`
- `userUpdatedEmail`

### Motivo

A Petstore é pública. Reutilizar IDs e usuários fixos aumenta a chance de conflito, sujeira de ambiente e falsos negativos.

---

# Grupo Pet

## 1. Listar pets por status
- **Endpoint:** `GET /pet/findByStatus`
- **Request na collection:** `Listar pets por status`
- **Objetivo:** validar a consulta de pets por status.

### O que é validado
- status code `200`
- resposta é uma lista
- a lista possui pelo menos um item

### Por que esse teste existe
Esse endpoint representa a consulta pública mais simples e previsível do grupo `Pet`.

---

## 2. Listar pets por tags
- **Endpoint:** `GET /pet/findByTags`
- **Request na collection:** `Listar pets por tags`
- **Objetivo:** validar a consulta de pets por tag.

### O que é validado
- status code `200`
- resposta é uma lista

### Por que esse teste existe
Garante cobertura de um endpoint de busca alternativo do mesmo domínio.

---

## 3. Criar pet
- **Endpoint:** `POST /pet`
- **Request na collection:** `Criar pet`
- **Objetivo:** criar um pet dinâmico para cobrir criação e sustentar testes dependentes.

### O que é validado
- status code `200`
- `id` retornado corresponde ao `petId` gerado
- `name` retornado corresponde ao nome criado

### Dependências
- usa variáveis dinâmicas geradas no início da execução

---

## 4. Buscar pet por ID
- **Endpoint:** `GET /pet/{petId}`
- **Request na collection:** `Buscar pet por ID`
- **Objetivo:** confirmar que o pet criado está acessível por identificador.

### O que é validado
- status code `200`
- `id` retornado corresponde ao `petId` criado

### Dependências
- depende do sucesso de `Criar pet`

---

## 5. Atualizar pet por formulário
- **Endpoint:** `POST /pet/{petId}`
- **Request na collection:** `Atualizar pet por formulário`
- **Objetivo:** validar a atualização parcial via form-urlencoded.

### O que é validado
- status code `200`
- resposta confirma a operação no `petId` esperado

### Dependências
- depende da existência prévia do pet

---

## 6. Upload de imagem do pet
- **Endpoint:** `POST /pet/{petId}/uploadImage`
- **Request na collection:** `Upload de imagem do pet`
- **Objetivo:** validar o endpoint multipart do grupo `Pet`.

### O que é validado
- status code `200`
- mensagem contém indicação de upload realizado

### Observação
No runner atual pode surgir um warning de depreciação interno do stack multipart, mas isso não invalida o teste.

---

## 7. Atualizar pet completo
- **Endpoint:** `PUT /pet`
- **Request na collection:** `Atualizar pet completo`
- **Objetivo:** validar a atualização completa da entidade pet.

### O que é validado
- status code `200`
- `status` final é `pending`
- `name` final corresponde ao valor atualizado

### Dependências
- depende da existência do pet criado anteriormente

---

## 8. Excluir pet
- **Endpoint:** `DELETE /pet/{petId}`
- **Request na collection:** `Excluir pet`
- **Objetivo:** validar a exclusão do pet criado.

### O que é validado
- status code `200`
- resposta confirma exclusão do `petId`

---

## 9. Confirmar pet excluído
- **Endpoint:** `GET /pet/{petId}`
- **Request na collection:** `Confirmar pet excluído`
- **Objetivo:** provar o efeito da exclusão.

### O que é validado
- status code `404`
- mensagem indica que o pet não foi encontrado

### Por que esse teste existe
Ele não cobre um endpoint novo, mas fecha a verificação do ciclo CRUD com prova do estado final.

---

# Grupo Store

## 10. Consultar inventário
- **Endpoint:** `GET /store/inventory`
- **Request na collection:** `Consultar inventário`
- **Objetivo:** validar o endpoint público de inventário.

### O que é validado
- status code `200`
- resposta é um objeto
- o objeto possui ao menos uma chave

---

## 11. Criar pedido
- **Endpoint:** `POST /store/order`
- **Request na collection:** `Criar pedido`
- **Objetivo:** criar um pedido para cobrir o fluxo principal do grupo `Store`.

### O que é validado
- status code `200`
- `id` retornado corresponde ao `orderId`
- `petId` do pedido corresponde ao `petId` usado na execução

### Dependências
- usa o `petId` dinâmico da execução

---

## 12. Buscar pedido por ID
- **Endpoint:** `GET /store/order/{orderId}`
- **Request na collection:** `Buscar pedido por ID`
- **Objetivo:** confirmar que o pedido criado está acessível.

### O que é validado
- status code `200`
- `id` retornado corresponde ao `orderId`

### Dependências
- depende do sucesso de `Criar pedido`

---

## 13. Excluir pedido
- **Endpoint:** `DELETE /store/order/{orderId}`
- **Request na collection:** `Excluir pedido`
- **Objetivo:** validar a exclusão do pedido criado.

### O que é validado
- status code `200`
- resposta confirma exclusão do `orderId`

---

# Grupo User

## 14. Criar usuário
- **Endpoint:** `POST /user`
- **Request na collection:** `Criar usuário`
- **Objetivo:** criar um usuário dinâmico principal para os testes do grupo `User`.

### O que é validado
- status code `200`
- resposta confirma operação

---

## 15. Criar usuários com array
- **Endpoint:** `POST /user/createWithArray`
- **Request na collection:** `Criar usuários com array`
- **Objetivo:** validar a criação em lote via array.

### O que é validado
- status code `200`
- resposta contém confirmação `ok`

---

## 16. Criar usuários com lista
- **Endpoint:** `POST /user/createWithList`
- **Request na collection:** `Criar usuários com lista`
- **Objetivo:** validar a criação em lote via lista.

### O que é validado
- status code `200`
- resposta contém confirmação `ok`

---

## 17. Buscar usuário por username
- **Endpoint:** `GET /user/{username}`
- **Request na collection:** `Buscar usuário por username`
- **Objetivo:** confirmar a persistência do usuário criado.

### O que é validado
- status code `200`
- `username` retornado corresponde ao esperado
- `email` retornado corresponde ao esperado

### Dependências
- depende do sucesso de `Criar usuário`

---

## 18. Atualizar usuário
- **Endpoint:** `PUT /user/{username}`
- **Request na collection:** `Atualizar usuário`
- **Objetivo:** validar a atualização de dados do usuário.

### O que é validado
- status code `200`
- resposta confirma operação

---

## 19. Login do usuário
- **Endpoint:** `GET /user/login`
- **Request na collection:** `Login do usuário`
- **Objetivo:** validar autenticação do usuário criado na execução.

### O que é validado
- status code `200`
- mensagem contém sessão iniciada

---

## 20. Logout do usuário
- **Endpoint:** `GET /user/logout`
- **Request na collection:** `Logout do usuário`
- **Objetivo:** validar o encerramento de sessão.

### O que é validado
- status code `200`
- mensagem contém `ok`

---

## 21. Excluir usuário
- **Endpoint:** `DELETE /user/{username}`
- **Request na collection:** `Excluir usuário`
- **Objetivo:** validar a remoção do usuário criado.

### O que é validado
- status code `200`
- resposta confirma exclusão do `username`

---

## Resumo da cobertura

### Endpoints cobertos por domínio

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

---

## Como executar

### Local

```bash
npm install
npm run api:test
```

### CI

A pipeline executa:

```bash
npm ci
npm run api:test
```

---

## Resultado validado até aqui

Na execução validada após a ampliação da collection:

- `21 requests`
- `48 assertions`
- `0 failed`

---

## Limitações conhecidas

1. A API Petstore é pública e externa ao projeto.
2. Isso significa que instabilidades de disponibilidade, persistência ou timing podem afetar execuções futuras.
3. A suíte foi desenhada para ser executável e explicável, mas ainda depende do comportamento do serviço remoto.

---

## Arquivos relacionados

- `api/postman/petstore_collection.json`
- `api/postman/petstore_environment.json`
- `package.json`
- `.github/workflows/ci.yml`
- `README.md`
- `ROTEIRO.md`
