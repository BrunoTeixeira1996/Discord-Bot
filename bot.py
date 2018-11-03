'''
Title : Discord Bot
Author : Bruno Teixeira
Year : 2018
'''
import discord
from discord.ext import commands
import asyncio
import time
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style

plt.style.use('dark_background')

token = 'token'
client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
	global pokeralho_guild
	print(f'Login in as {client.user}')

@client.event 
async def on_ready():
	await client.change_presence(activity=discord.Game(name='Doing The Math'))
	print(f'We have logged in as {client.user}')

@client.command(pass_context=True)
async def autor(ctx):
	channel = ctx.message.channel
	embed = discord.Embed(title='My name is Tiburcio', description = 'Im a bot', colour=discord.Colour.orange())
	embed.set_image(url='https://cdn.discordapp.com/avatars/500793832384757771/1084a7b38007d727410dc39c08106d89.png')
	await ctx.send(embed=embed)

def member_report(guild):
	online = 0
	idle = 0
	offline = 0
	for i in guild.members:
		if str(i.status) == 'online':
			online +=1
		if str(i.status) == 'offline':
			offline +=1
		else:
			idle +=1
	return online, idle, offline

async def background_task():
	await client.wait_until_ready()
	global pokeralho_guild
	pokeralho_guild = client.get_guild(401767363072229387)

	while not client.is_closed():
		try:
			online, idle, offline = member_report(pokeralho_guild)
			with open('data.csv','a') as file:
				file.write(f'{int(time.time())},{online},{idle},{offline}\n')
				df = pd.read_csv("data.csv", names=['time', 'online', 'idle', 'offline'])
				df['date'] = pd.to_datetime(df['time'],unit='s')
				df['total'] = df['online'] + df['offline'] + df['idle']
				df.drop("time", 1,  inplace=True)
				df.set_index("date", inplace=True)
				plt.clf()
				df['online'].plot()
				plt.legend()
				plt.savefig("online.png")
			await asyncio.sleep(15)
		except Exception as e:
			print(str(e))
			await asyncio.sleep(15)


@client.event
async def on_message(message):
	global pokeralho_guild
	print(f'{message.channel}: {message.author}: {message.content}')

	if 'member_count()' == message.content.lower():
		await message.channel.send(f'```py\n{pokeralho_guild.member_count} ```')

	elif 'member_report()' == message.content.lower():
		online, idle, offline = member_report(pokeralho_guild)
		await message.channel.send(f'```Online: {online} \nIdle: {idle} \nOffline: {offline} ```')

@client.event
async def on_message(message):
	pokeralho_guild = client.get_guild(401767363072229387)
	if "member_count()" == message.content.lower():
		await message.channel.send(f'```There are {pokeralho_guild.member_count} members in this server```')
	elif message.content.startswith('cool()'):
		thumbs = message.channel
		await thumbs.send(':thumbsup:')
	elif "logout()" == message.content.lower():
		await client.close()
	elif "member_report()" == message.content.lower():
		online, iddle, offline = member_report(pokeralho_guild)
		await message.channel.send(f'```Online: {online}.\nIddle:{iddle}.\nOffline: {offline}. ```')
		file = discord.File('online.png', filename='grafico.png')
		await message.channel.send(file=file)
	await client.process_commands(message)


client.loop.create_task(background_task())
client.run(token)
