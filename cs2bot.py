import discord
from discord.ext import commands, tasks
import mysql.connector

TOKEN = 'MTExNTQzNjI0MjkzNTQ4ODU4NA.GTCRdw.xO5gg5gbVRL7CyRjfBMFjJfZ51WWkWhdvnvr7g'

config = {
    'user': 'coyotecs2',
    'password': '#uniaoBrasil22#',
    'host': '107.190.131.154',
    'database': 'coyotecs2',
    'autocommit': True
}

async def atualizar_top15():
    channel = bot.get_channel(376928206411792407)

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM k4ranks ORDER BY points DESC LIMIT 15')
    resultados = cursor.fetchall()
    mensagem = "```\n"
    mensagem += "Top 15 da classificação:\n\n"
    for index, resultado in enumerate(resultados, start=1):
        nome_jogador = resultado[1]
        classificacao = resultado[3]
        pontuacao = resultado[4]
        mensagem += f"{index}: {nome_jogador} - {classificacao} ({pontuacao} pontos)\n"
    mensagem += "```"
    await channel.send(mensagem)
    conn.close()

@tasks.loop(hours=48)
async def atualizar_top15_loop():
    await atualizar_top15()

async def atualizar_top_mvp():
    channel = bot.get_channel(982623639851634779)

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute('SELECT name, mvp FROM k4stats ORDER BY mvp DESC LIMIT 15')
    mvps = cursor.fetchall()

    print(f"Resultados da consulta: {mvps}")

    if mvps:
        mensagem = "```\nRank de melhores jogadores por partida:\n\n"
        melhor_mvp = mvps[0]
        for index, mvp in enumerate(mvps, start=1):
            nome_mvp = mvp[0]
            partidas_mvp = mvp[1]
            if mvp == melhor_mvp:
                mensagem += f"{index} - {nome_mvp} é o melhor jogador, com {partidas_mvp} MVPs.\n"
            else:
                mensagem += f"{index} - {nome_mvp} tem {partidas_mvp} MVPs.\n"
        mensagem += "```"
    else:
        mensagem = "Nenhum MVP encontrado no servidor CS."

    await channel.send(mensagem)
    conn.close()

@tasks.loop(hours=48)
async def atualizar_top_mvp_loop():
    await atualizar_top_mvp()

# Definindo os intents necessários
intents = intents = discord.Intents.all()
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('BOT CS NEWS está pronto!')
    await atualizar_top15_loop.start()
    await atualizar_top_mvp_loop.start()

@bot.command()
async def top15(ctx):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM k4ranks ORDER BY points DESC LIMIT 15')
    resultados = cursor.fetchall()
    mensagem = "```\n"
    mensagem += "Top 15 da classificação:\n\n"
    for index, resultado in enumerate(resultados, start=1):
        nome_jogador = resultado[1]
        classificacao = resultado[3]
        pontuacao = resultado[4]
        mensagem += f"{index}: {nome_jogador} - {classificacao} ({pontuacao} pontos)\n"
    mensagem += "```"
    await ctx.send(mensagem)
    conn.close()

@bot.command()
async def topmvp(ctx):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute('SELECT name, mvp FROM k4stats ORDER BY mvp DESC LIMIT 15')
    mvps = cursor.fetchall()
    mensagem = "```\nRank de melhores jogadores por partida:\n\n"
    melhor_mvp = mvps[0]
    for index, mvp in enumerate(mvps, start=1):
        nome_mvp = mvp[0]
        partidas_mvp = mvp[1]
        if mvp == melhor_mvp:
            mensagem += f"{index} - {nome_mvp} é o melhor jogador, com {partidas_mvp} MVPs.\n"
        else:
            mensagem += f"{index} - {nome_mvp} tem {partidas_mvp} MVPs.\n"
    mensagem += "```"
    await ctx.send(mensagem)
    conn.close()

@bot.command()
async def comandos(ctx):
    mensagem = "```\nComandos do servidor:\n\n"
    mensagem += "!top15 - Mostra os top 15 jogadores do servidor.\n"
    mensagem += "!topmvp - Mostra os melhores jogadores por partida do servidor.\n"
    mensagem += "```"
    await ctx.send(mensagem)

bot.run(TOKEN)