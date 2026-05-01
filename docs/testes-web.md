# Documentação detalhada dos testes web

## Visão geral

Esta suíte automatiza o fluxo E2E do **SauceDemo** usando **Python + Selenium + pytest**.

- URL base: `https://www.saucedemo.com/`
- Arquivo principal de teste: `web/tests/test_checkout_e2e.py`
- Comando de execução: `python -m pytest web/tests/test_checkout_e2e.py -q`
- Runner de CI: GitHub Actions (`.github/workflows/ci.yml`)

O cenário cobre o fluxo funcional pedido no enunciado:

- login
- seleção de produto
- carrinho
- checkout
- finalização da compra

---

## Objetivo da suíte

O teste foi construído para provar, de ponta a ponta, que um usuário consegue:

1. acessar o sistema
2. autenticar-se com credenciais válidas
3. adicionar produto ao carrinho
4. iniciar checkout
5. preencher informações do comprador
6. concluir a compra com sucesso

Esse fluxo atende diretamente ao escopo da prova para automação web.

---

## Estrutura da automação

A automação foi organizada com **Page Objects**, separando responsabilidade por tela:

- `web/pages/login_page.py`
- `web/pages/inventory_page.py`
- `web/pages/cart_page.py`
- `web/pages/checkout_page.py`

### Benefícios dessa estrutura

1. reduz duplicação de seletores e interações
2. melhora legibilidade do teste principal
3. facilita manutenção quando a interface muda
4. deixa a apresentação mais clara em aula

---

## Arquivo principal do cenário

- `web/tests/test_checkout_e2e.py`

Esse arquivo orquestra o fluxo completo usando os Page Objects.

---

## Evidências visuais geradas

O teste salva screenshots durante a execução em:

- `docs/evidencias/`

Arquivos gerados no fluxo atual:

- `01-login.png`
- `02-inventario.png`
- `03-produto-no-carrinho.png`
- `04-carrinho.png`
- `05-checkout-informacoes.png`
- `06-checkout-resumo.png`
- `07-compra-finalizada.png`

### Motivo

Essas capturas ajudam na apresentação e funcionam como evidência concreta do comportamento da suíte.

---

# Fluxo detalhado do teste

## 1. Preparação do cenário

O teste instancia os objetos de página:

- `LoginPage`
- `InventoryPage`
- `CartPage`
- `CheckoutPage`

Também usa o fixture `driver` e as configurações vindas de `settings`.

### O que isso garante
- browser inicializado corretamente
- waits explícitos centralizados
- ambiente consistente entre local e CI

---

## 2. Captura inicial da tela de login

### Ação
Antes do login, o teste salva a evidência:

- `01-login.png`

### Objetivo
Registrar o estado inicial da aplicação antes de qualquer interação.

---

## 3. Login no SauceDemo

### Ação
O teste executa:

- `login_page.login(settings.login_user, settings.login_password)`

### O que é validado
Após o login, a suíte verifica:

- `inventory_page.get_title() == "Products"`

### Por que essa asserção existe
Esse é o sinal funcional de que o usuário autenticado foi levado para a tela de inventário com sucesso.

### Evidência gerada
- `02-inventario.png`

---

## 4. Adição do produto ao carrinho

### Ação
O teste executa:

- `inventory_page.add_backpack_to_cart()`

### O que é validado
A suíte verifica:

- `inventory_page.get_cart_count() == "1"`

### Por que essa asserção existe
Ela confirma que o item foi realmente adicionado ao carrinho e que o contador visual foi atualizado.

### Evidência gerada
- `03-produto-no-carrinho.png`

---

## 5. Abertura do carrinho

### Ação
O teste navega para o carrinho com:

- `inventory_page.open_cart()`

### O que é validado
A suíte verifica:

- `cart_page.has_backpack() is True`

### Por que essa asserção existe
Não basta confiar no contador. Aqui o teste confirma a presença concreta do produto esperado dentro do carrinho.

### Evidência gerada
- `04-carrinho.png`

---

## 6. Início do checkout

### Ação
O teste executa:

- `cart_page.start_checkout()`

Depois aguarda:

- `checkout_page.wait_for_information_step()`

### O que é validado
A validação aqui é implícita na espera bem-sucedida pela etapa de informações.

### Por que essa etapa é importante
Ela garante que o fluxo saiu do carrinho e entrou na primeira fase do checkout.

### Evidência gerada
- `05-checkout-informacoes.png`

---

## 7. Preenchimento das informações do comprador

### Ação
O teste preenche:

- `first_name="QA"`
- `last_name="Automation"`
- `postal_code="89000000"`

Usando:

- `checkout_page.fill_customer_information(...)`

Depois aguarda:

- `checkout_page.wait_for_overview_step()`

### O que é validado
A validação aqui é a transição bem-sucedida para a etapa de resumo do checkout.

### Por que essa etapa existe
Ela prova que o formulário foi aceito e que o usuário avançou corretamente no processo.

### Evidência gerada
- `06-checkout-resumo.png`

---

## 8. Finalização da compra

### Ação
O teste executa:

- `checkout_page.finish_checkout()`

### O que é validado
A suíte verifica:

- `checkout_page.get_success_message() == "Thank you for your order!"`

### Por que essa asserção existe
Ela confirma o encerramento correto do fluxo E2E e a conclusão funcional da compra.

### Evidência gerada
- `07-compra-finalizada.png`

---

# Resumo do cenário coberto

O teste cobre o seguinte encadeamento funcional:

1. login válido
2. entrada na tela de inventário
3. adição de produto ao carrinho
4. conferência do item no carrinho
5. início do checkout
6. preenchimento dos dados obrigatórios
7. visualização do resumo
8. finalização bem-sucedida

---

## Estratégia de validação

A suíte usa uma combinação de:

- asserções funcionais diretas
- waits explícitos para sincronização
- Page Objects para encapsular detalhes da interface
- screenshots como evidência de execução

### Exemplos de validação funcional
- título da tela após login
- contador do carrinho após adição
- presença do produto no carrinho
- mensagem final de sucesso

---

## Dados usados no teste

As credenciais e parâmetros são lidos da configuração do projeto.

### Variáveis relevantes
- `BASE_URL`
- `LOGIN_USER`
- `LOGIN_PASSWORD`
- `BROWSER`
- `CHROME_BINARY`
- `HEADLESS`
- `IMPLICIT_WAIT_SECONDS`
- `EXPLICIT_WAIT_SECONDS`

Essas variáveis podem ser ajustadas por `.env` quando necessário.

---

## Como executar

### Local

```bash
python -m pip install -r requirements.txt
python -m pytest web/tests/test_checkout_e2e.py -q
```

### CI

A pipeline executa o mesmo teste em runner Linux com Chrome configurado:

```bash
python -m pytest web/tests/test_checkout_e2e.py -q
```

---

## Resultado esperado

Quando o fluxo passa corretamente, o teste comprova que:

- o login funciona
- a navegação principal está íntegra
- o carrinho registra a seleção
- o checkout aceita os dados
- a compra é finalizada com mensagem de sucesso

---

## Limitações conhecidas

1. O teste cobre um fluxo E2E central, não múltiplos fluxos alternativos.
2. A execução depende da disponibilidade do SauceDemo e do browser no ambiente.
3. Mudanças de layout, seletor ou texto no site podem exigir ajuste dos Page Objects.

---

## Arquivos relacionados

- `web/tests/test_checkout_e2e.py`
- `web/pages/login_page.py`
- `web/pages/inventory_page.py`
- `web/pages/cart_page.py`
- `web/pages/checkout_page.py`
- `web/conftest.py`
- `web/driver_factory.py`
- `.github/workflows/ci.yml`
- `README.md`
