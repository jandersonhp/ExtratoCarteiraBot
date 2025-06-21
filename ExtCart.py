from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from datetime import datetime
import os
import json

#Carregar TOKEN do arquivo .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Nome do arquivo onde vamos salvar os dados
ARQUIVO_DADOS = 'carteiras.json'

# Estrutura para guardar os dados em memória
carteiras = {}

# Função para carregar os dados do JSON ao iniciar o bot
def carregar_dados():
    global carteiras
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as file:
            carteiras = json.load(file)
    else:
        carteiras = {}

# Função para salvar os dados no JSON
def salvar_dados():
    with open(ARQUIVO_DADOS, 'w', encoding='utf-8') as file:
        json.dump(carteiras, file, ensure_ascii=False, indent=4)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Olá! Eu sou seu bot de carteira financeira. 💰\n\n"
        "📌 Comandos disponíveis:\n"
        "/saldo <valor> → Adicionar saldo\n"
        "/recebeu <valor> <descrição> → Registrar um ganho\n"
        "/gastou <valor> <descrição> → Registrar um gasto\n"
        "/extrato → Ver o extrato e saldo atual\n"
        "/limpar → Limpar todas as movimentações\n"
        "/exportar → Exportar extrato em .txt"
    )

async def saldo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if user_id not in carteiras:
        carteiras[user_id] = []

    try:
        valor = float(context.args[0])
        data_hora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        carteiras[user_id].append(['Saldo Adicionado', valor, 'Saldo Adicionado', data_hora])
        salvar_dados()
        await update.message.reply_text(f"✅ Saldo adicionado de R$ {valor:.2f} definido em {data_hora}")
    except (IndexError, ValueError):
        await update.message.reply_text("❌ Uso correto: /saldo <valor>")

async def recebeu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if user_id not in carteiras:
        carteiras[user_id] = []

    try:
        valor = float(context.args[0])
        descricao = ' '.join(context.args[1:]) if len(context.args) > 1 else 'Sem descrição'
        data_hora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        carteiras[user_id].append(['Entrada', valor, descricao, data_hora])
        salvar_dados()
        await update.message.reply_text(f"✅ Registrado: +R$ {valor:.2f} ({descricao}) em {data_hora}")
    except (IndexError, ValueError):
        await update.message.reply_text("❌ Uso correto: /recebeu <valor> <descrição>")

async def gastou(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if user_id not in carteiras:
        carteiras[user_id] = []

    try:
        valor = float(context.args[0])
        descricao = ' '.join(context.args[1:]) if len(context.args) > 1 else 'Sem descrição'
        data_hora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        carteiras[user_id].append(['Saída', valor, descricao, data_hora])
        salvar_dados()
        await update.message.reply_text(f"✅ Registrado: -R$ {valor:.2f} ({descricao}) em {data_hora}")
    except (IndexError, ValueError):
        await update.message.reply_text("❌ Uso correto: /gastou <valor> <descrição>")

async def extrato(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if user_id not in carteiras or not carteiras[user_id]:
        await update.message.reply_text("📭 Você ainda não registrou nenhuma movimentação.")
        return

    saldo = 0
    linhas = []
    for tipo, valor, descricao, data_hora in carteiras[user_id]:
        if tipo == 'Entrada' or tipo == 'Saldo Adicionado':
            saldo += valor
            sinal = '+'
        else:
            saldo -= valor
            sinal = '-'
        linhas.append(f"{sinal} R$ {valor:.2f} — {descricao} ({data_hora})")

    resumo = "\n".join(linhas)
    resumo += f"\n\n💰 Saldo atual: R$ {saldo:.2f}"
    resumo += "\n\n📢 Não esqueça de exportar seu extrato com /exportar para não perder seus registros!"
    await update.message.reply_text(resumo)

async def limpar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if user_id in carteiras:
        carteiras[user_id] = []
        salvar_dados()
        await update.message.reply_text("✅ Seu extrato foi limpo com sucesso.")
    else:
        await update.message.reply_text("📭 Você ainda não tem nenhuma movimentação registrada.")

async def exportar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if user_id not in carteiras or not carteiras[user_id]:
        await update.message.reply_text("📭 Você ainda não tem movimentações para exportar.")
        return

    saldo = 0
    linhas = []
    for tipo, valor, descricao, data_hora in carteiras[user_id]:
        if tipo == 'Entrada' or tipo == 'Saldo Adicionado':
            saldo += valor
            sinal = '+'
        else:
            saldo -= valor
            sinal = '-'
        linhas.append(f"{sinal} R$ {valor:.2f} — {descricao} ({data_hora})")

    resumo = "\n".join(linhas)
    resumo += f"\n\nSaldo final: R$ {saldo:.2f}"

    filename = f"extrato_{user_id}.txt"
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(resumo)

    await update.message.reply_document(document=open(filename, 'rb'))
    os.remove(filename)

if __name__ == '__main__':
    carregar_dados()
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("saldo", saldo))
    app.add_handler(CommandHandler("recebeu", recebeu))
    app.add_handler(CommandHandler("gastou", gastou))
    app.add_handler(CommandHandler("extrato", extrato))
    app.add_handler(CommandHandler("limpar", limpar))
    app.add_handler(CommandHandler("exportar", exportar))

    print("🤖 Bot rodando...")
    app.run_polling()
