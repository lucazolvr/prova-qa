# Testes Web E2E — SauceDemo

## Visão geral

| Item | Detalhe |
|------|---------|
| **Aplicação** | SauceDemo |
| **URL** | `https://www.saucedemo.com/` |
| **Stack** | Python 3.12 + Selenium + pytest |
| **Teste principal** | `web/tests/test_checkout_e2e.py` |
| **Execução** | `python -m pytest web/tests/test_checkout_e2e.py -q` |
| **CI** | GitHub Actions — job `web-tests` |

---

## Fluxo coberto

O teste percorre o fluxo de compra completo do SauceDemo:

```
┌─────────┐    ┌────────────┐    ┌──────────────┐    ┌──────────┐
│  Login   │───>│ Inventário │───>│ Add ao cart   │───>│ Carrinho │
└─────────┘    └────────────┘    └──────────────┘    └──────────┘
                                                          │
     ┌────────────────┐    ┌─────────────┐    ┌───────────┘
     │ Compra concluída│<───│   Resumo    │<───│ Checkout  │
     └────────────────┘    └─────────────┘    └───────────┘
```

---

## Arquitetura — Page Objects

A automação encapsula cada tela em um Page Object:

| Page Object | Arquivo | Responsabilidade |
|-------------|---------|------------------|
| `LoginPage` | `web/pages/login_page.py` | Preencher credenciais e submeter login |
| `InventoryPage` | `web/pages/inventory_page.py` | Verificar título, adicionar produto, acessar carrinho |
| `CartPage` | `web/pages/cart_page.py` | Verificar itens no carrinho, iniciar checkout |
| `CheckoutPage` | `web/pages/checkout_page.py` | Preencher dados, revisar, finalizar compra |

Cada Page Object recebe o `driver` e o `explicit_wait_seconds`, centralizando waits explícitos para estabilidade em CI.

---

## Etapas do teste

### 1. Tela de login

| | |
|-|-|
| **Ação** | Captura a tela inicial antes de qualquer interação |
| **Evidência** | `01-login.png` |

### 2. Login

| | |
|-|-|
| **Ação** | `login_page.login(user, password)` |
| **Asserção** | `inventory_page.get_title() == "Products"` |
| **O que valida** | Autenticação bem-sucedida e navegação para inventário |
| **Evidência** | `02-inventario.png` |

### 3. Adicionar produto ao carrinho

| | |
|-|-|
| **Ação** | `inventory_page.add_backpack_to_cart()` |
| **Asserção** | `inventory_page.get_cart_count() == "1"` |
| **O que valida** | Item registrado no carrinho e contador visual atualizado |
| **Evidência** | `03-produto-no-carrinho.png` |

### 4. Abrir carrinho

| | |
|-|-|
| **Ação** | `inventory_page.open_cart()` |
| **Asserção** | `cart_page.has_backpack() is True` |
| **O que valida** | Presença concreta do produto esperado dentro do carrinho |
| **Evidência** | `04-carrinho.png` |

### 5. Iniciar checkout

| | |
|-|-|
| **Ação** | `cart_page.start_checkout()` |
| **Validação** | `checkout_page.wait_for_information_step()` (wait explícito) |
| **O que valida** | Transição do carrinho para a primeira etapa do checkout |
| **Evidência** | `05-checkout-informacoes.png` |

### 6. Preencher dados do comprador

| | |
|-|-|
| **Ação** | `checkout_page.fill_customer_information("QA", "Automation", "89000000")` |
| **Validação** | `checkout_page.wait_for_overview_step()` (wait explícito) |
| **O que valida** | Formulário aceito e avanço para a etapa de resumo |
| **Evidência** | `06-checkout-resumo.png` |

### 7. Finalizar compra

| | |
|-|-|
| **Ação** | `checkout_page.finish_checkout()` |
| **Asserção** | `checkout_page.get_success_message() == "Thank you for your order!"` |
| **O que valida** | Encerramento correto do fluxo E2E com mensagem de sucesso |
| **Evidência** | `07-compra-finalizada.png` |

---

## Evidências visuais

O teste gera 7 screenshots automaticamente em `docs/evidencias/`, um para cada etapa do fluxo:

| # | Arquivo | Etapa |
|---|---------|-------|
| 1 | `01-login.png` | Tela de login (estado inicial) |
| 2 | `02-inventario.png` | Inventário após login |
| 3 | `03-produto-no-carrinho.png` | Produto adicionado (badge atualizado) |
| 4 | `04-carrinho.png` | Carrinho com item |
| 5 | `05-checkout-informacoes.png` | Formulário de dados do comprador |
| 6 | `06-checkout-resumo.png` | Resumo do pedido |
| 7 | `07-compra-finalizada.png` | Mensagem de compra concluída |

---

## Configuração

As credenciais e parâmetros são lidos de variáveis de ambiente via `web/config/settings.py`:

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `BASE_URL` | `https://www.saucedemo.com/` | URL da aplicação |
| `LOGIN_USER` | `standard_user` | Usuário de teste |
| `LOGIN_PASSWORD` | `secret_sauce` | Senha de teste |
| `BROWSER` | `chrome` | Navegador |
| `CHROME_BINARY` | *(vazio)* | Caminho do Chrome (se não padrão) |
| `HEADLESS` | `true` | Executar sem interface gráfica |
| `IMPLICIT_WAIT_SECONDS` | `0` | Wait implícito do Selenium |
| `EXPLICIT_WAIT_SECONDS` | `10` | Wait explícito (30s no CI) |

Arquivo de exemplo: `.env.example`

---

## Execução

```bash
# Local
python -m pip install -r requirements.txt
python -m pytest web/tests/test_checkout_e2e.py -q

# CI (GitHub Actions)
# Roda com HEADLESS=true, EXPLICIT_WAIT_SECONDS=30
python -m pytest web/tests/test_checkout_e2e.py -q
```

Em caso de falha no CI, screenshots e logs de debug são publicados como artefatos do workflow.

---

## Limitações conhecidas

- O teste cobre o fluxo E2E principal (happy path), não fluxos alternativos ou negativos
- A execução depende da disponibilidade do SauceDemo e do Chrome no ambiente
- Alterações de layout, seletores ou texto no site podem exigir ajuste nos Page Objects

---

## Arquivos relacionados

| Arquivo | Papel |
|---------|-------|
| `web/tests/test_checkout_e2e.py` | Cenário E2E principal |
| `web/pages/login_page.py` | Page Object — Login |
| `web/pages/inventory_page.py` | Page Object — Inventário |
| `web/pages/cart_page.py` | Page Object — Carrinho |
| `web/pages/checkout_page.py` | Page Object — Checkout |
| `web/conftest.py` | Fixtures do pytest (driver, settings) |
| `web/driver_factory.py` | Instanciação do WebDriver |
| `web/config/settings.py` | Leitura de .env e configurações |
| `.github/workflows/ci.yml` | Pipeline CI |
