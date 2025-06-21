<p align="center">
  <img src="https://raw.githubusercontent.com/jandersonhp/ExtratoCarteiraBot/refs/heads/main/assets/banner.png" alt="Carteira Bot" width="700"/>
</p>

# 🤖 Extrato Carteira Bot - Telegram

Este é um bot de Telegram simples para gerenciamento financeiro pessoal (tipo uma carteira digital básica).  
Ele permite ao usuário registrar ganhos, gastos e visualizar o extrato com saldo atualizado.

Bot Configurado no Telegram: [@ExtCart_Bot](https://t.me/extcart_bot)

---

## ✅ Funcionalidades

- Adicionar saldo inicial
- Registrar entradas de dinheiro
- Registrar saídas (gastos)
- Consultar o extrato com saldo atual
- Limpar todas as movimentações
- Exportar o extrato como arquivo `.txt`
- Dados persistentes (salvos localmente em JSON)

---

## 🚀 Como criar seu próprio bot no Telegram

1. Abra o Telegram e procure pelo **BotFather**

2. Envie o comando:

```
/newbot
```

3. Siga as instruções para escolher um nome e um username para o bot.

4. O BotFather vai te fornecer um **Token de API**, algo como:

```
123456789:ABCDefGhIJKlmNOPqrSTUvWXyz
```

**⚠️ Importante:**  
Nunca compartilhe seu token publicamente.

---

## 💻 Como rodar o bot localmente

### 1. Clone o projeto:

```bash
git clone https://github.com/jandersonhp/ExtratoCarteiraBot.git
cd ExtratoCarteiraBot
```

---

### 2. Instale as dependências:

```bash
pip install -r requirements.txt
```

> Se ainda não tiver um arquivo `requirements.txt`, crie um com:

```
python-telegram-bot==20.0
python-dotenv
```

---

### 3. Crie um arquivo `.env` com o token do seu bot:

Na raiz do projeto, crie um arquivo chamado `.env` com este conteúdo:

```
BOT_TOKEN=SEU_TOKEN_AQUI
```

(Substitua `SEU_TOKEN_AQUI` pelo token que o BotFather te deu.)

---

### 4. Rode o bot:

```bash
python ExtCart.py
```

(Ou o nome do arquivo Python que você está usando.)

---

## ✅ Comandos disponíveis

| Comando          | Função                                    |
|------------------|-------------------------------------------|
| /start           | Exibe mensagem de boas-vindas e ajuda     |
| /saldo <valor>   | Adiciona um saldo inicial                 |
| /recebeu <v> <d> | Registra uma entrada de dinheiro          |
| /gastou <v> <d>  | Registra um gasto                         |
| /extrato         | Mostra todas as movimentações e saldo     |
| /limpar          | Limpa todas as movimentações              |
| /exportar        | Exporta o extrato em formato `.txt`       |


---

## 📃 Licença

Este projeto está licenciado sob a licença MIT.
