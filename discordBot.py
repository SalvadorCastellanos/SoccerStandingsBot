# This program prints Hello, world!
import discord
import datetime
import re
import numpy as np
import pandas as pd
import requests 
import json
import sys

from urllib.request import urlopen
from bs4 import BeautifulSoup
from dateutil import parser
from dateutil import tz
from discord.ext import commands
from tabulate import tabulate

# create a list of leagues and seasons
leagues = ['eng.1', 'ger.1', 'ita.1', 'esp.1', 'fra.1', 'ned.1','eng.2','usa.1','mex.1','por.1','rus.1','sco.1','bra.1','tur.1'] 
seasons = ['2013','2014', '2015', '2016', '2017', '2018', '2019', '2020']
showleagues = ['EPL', 'Bundesliga', 'SerieA', 'LaLiga', 'Ligue1', 'Eredivisie','EFL','MLS','LigaMX','PrimeiraLiga','RPL','ScottishPremiership','CampeonatoBrasileiro','SuperLig']

bot = commands.Bot(command_prefix = '!', help_command=None)


#Event to show that bot is ready to use.
@bot.event
async def on_ready():
	print('Bot is ready.')

#Simple command for testing.
@bot.command()
async def ping(ctx):
	await ctx.send(f'Pong! Latency: {round(bot.latency * 1000)}ms')


#Command for printing the standings of a league and season.
@bot.command()
async def standings(ctx, league, season):

	#Convert input league into correct format for url
	if league == "EPL":
		league = "eng.1"
	elif league == "Bundesliga":
		league = "ger.1"
	elif league == "SerieA":
		league = "ita.1"
	elif league == "LaLiga":
		league = "esp.1"
	elif league == "Ligue1":
		league = "fra.1"
	elif league == "Eredivisie":
		league = "ned.1"
	elif league == "EFL":
		league = "eng.2"
	elif league == "MLS":
		league = "usa.1"
	elif league == "LigaMX":
		league = "mex.1"
	elif league == "PrimeiraLiga":
		league = "por.1"
	elif league == "RPL":
		league = "rus.1"
	elif league == "ScottishPremiership":
		league = "sco.1"
	elif league == "CampeonatoBrasileiro":
		league = "bra.1"
	elif league == "SuperLig":
		league = "tur.1"
	    
	if league not in leagues :
		await ctx.send("Invalid input, please pick from the list of leagues.")
		await ctx.send(showleagues)
		return
	else:
		#build the url
		base_url = 'https://www.espn.com/soccer/standings/_/league/' + league
		
	if season not in seasons :
	    await ctx.send("Invalid input, please pick from the list of seasons.")
	    await ctx.send(seasons)
	    return
	else:
		if season != seasons[7] :
			base_url = base_url + "/season/" + season

	#Open the url
	page = urlopen(base_url)
	soup = BeautifulSoup(page.read(), 'html.parser')

	#Go to the section in html that stores the standings
	table = soup.find_all("tr", {"class": ["Table__TR Table__TR--sm Table__even", "filled Table__TR Table__TR--sm Table__even"]})
	total = len(table)/2

	#Create an array for the teams in the order they are placed in the standings
	data = []
	teams = {} 
	for x in range(0, int(total)):
		teams[x] = table[x].abbr["title"]

	#Create arrays for the rest of the stats being scraped
	matches = {}
	wins = {}
	draws = {}
	loses = {}
	goalsfor = {}
	goalsagainst = {}
	goaldiff = {}
	points = {}

	#Scrape all the stats by looping through every team
	for x in range(int(total), int(len(table))):
		matchstat = table[x].find('span',{'class':'stat-cell'})
		matches[x-int(total)] = matchstat.text
		winstat = matchstat.find_next('span',{'class':'stat-cell'})
		wins[x-int(total)] = winstat.text
		drawstat = winstat.find_next('span',{'class':'stat-cell'})
		draws[x-int(total)] = drawstat.text
		losestat = drawstat.find_next('span',{'class':'stat-cell'})
		loses[x-int(total)] = losestat.text
		gfstat = losestat.find_next('span',{'class':'stat-cell'})
		goalsfor[x-int(total)] = gfstat.text
		gastat = gfstat.find_next('span',{'class':'stat-cell'})
		goalsagainst[x-int(total)] = gastat.text
		gdstat = gastat.find_next('span',{'class':'stat-cell'})
		goaldiff[x-int(total)] = gdstat.text
		pointstat = gdstat.find_next('span',{'class':'stat-cell'})
		points[x-int(total)] = pointstat.text
		
	for x in range(0, int(total)):
		data.append([teams[x], matches[x], wins[x], draws[x], loses[x], goalsfor[x], goalsagainst[x], goaldiff[x], points[x]])	
	#print(data)
	# create empty data frame in pandas
	full_stat = pd.DataFrame(data, columns = ['Team', 'GP', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'PTS'])

	#print the results
	codeblock = "```"
	await ctx.send(codeblock + tabulate(full_stat, showindex=False, headers=full_stat.columns) + codeblock)
	print(codeblock + tabulate(full_stat, showindex=False, headers=full_stat.columns) + codeblock)
	page.close()

@bot.command()
async def help(ctx):
	await ctx.send(f'Usage: !standings [league] [season]')
	await ctx.send(f'Here are a list of supported leagues:')
	await ctx.send(showleagues)
	await ctx.send(f'Here are a list of supported seasons:')
	await ctx.send(seasons)

with open("token.0", "r", encoding= "utf-8") as f:
	bottoken = f.read()

bot.run(bottoken)