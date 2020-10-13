#!/usr/bin/python3
# bot.py
import os
import discord
import logging
import platform
import subprocess
from discord.ext import commands
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import pydig, re, json, requests

# LOGGING CONFIGURATION

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('/var/log/supervisor/discord-bot.log')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Functions

# DNS FUNCTIONS

def get_ip(domain_name, dns_type):
    result = pydig.query(domain_name,dns_type)
    return(result[0])

# PING FUNCTIONS

def ping_command(host):
    param = '-n' if platform.system().lower()=='windows' else '-c'
    command = ['ping', param, '1', host]
    return subprocess.call(command) == 0

def ping_func(ip):
   regex = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
   if regex.match(ip):
       ping_result = ping_command(ip)
       if ping_result:
           return('OK')
       else:
           return('KO')
   else:
       return('The IP given ({}) is not correct, you should pass an IP.'.format(ip))

# HTTP STATUS

def http_status(value):
    status_request = requests.get(value)
    return('Status : {}'.format(status_request.status_code))

# HYPIXEL STATS
def get_hystats(name):
    url = 'https://sky.lea.moe/stats/{}'.format(name)
    html_request = requests.get(url)
    soup = BeautifulSoup(html_request.content,'html.parser')
    stats = soup.find('meta', property='og:description')

    if('A beautiful site' in stats['content']):
        stats['content'] = 'User not found.'

    return(stats['content'])

# bot definition
bot = commands.Bot(command_prefix='!atom ')

# commands
@bot.command()
async def dns(ctx, arg1, arg2):
    result = get_ip(arg1, arg2)
    await ctx.send(result)

@bot.command()
async def ping(ctx, arg):
    result = ping_func(arg)
    await ctx.send(result)

@bot.command()
async def http(ctx, arg):
    result = http_status(arg)
    await ctx.send(result)

@bot.command()
async def prout(ctx):
    await ctx.send('prout :poop:')

@bot.command()
async def hystats(ctx, arg):
    result = get_hystats(arg)
    await ctx.send(result)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(TOKEN)

