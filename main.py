import os
import random
from dotenv import load_dotenv
import discord
import requests
from discord.ext import commands, tasks
import scraper

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Dont't Edit Above this
URL = os.getenv("SITE")
data_path = os.getenv("DATA")
bot.owner_id = os.getenv("USER_ID")
# Don't Edit Below this

DATA = "data.csv"

if not os.path.exists(DATA):
    with open(DATA, 'w') as file:
        pass

@bot.event
async def on_ready():
    print(f"Sylvian's presence is strong. Summoner's ID: {bot.owner_id}")

@bot.command(name='shut')
async def shutdown_bot(ctx):
    if str(ctx.author.id) == str(bot.owner_id):
        await ctx.send("I am always there...")
        await bot.close()
    else:
        await ctx.send("You did not summon me...")

@bot.command(name="purge")
async def purge(ctx, messages: int):
    if ctx.author.guild_permissions.manage_messages:
        await ctx.channel.purge(limit=messages + 1)
    else:
        await ctx.send("You do not seem to have the privilege...")

@bot.command(name='coin')
async def flipcoin(ctx):
    result = random.choice(['Heads', 'Tails'])
    if result == 'Tails':
        gif = f"https://tenor.com/view/fear-and-hunger-coin-toss-coin-tails-gif-3319076472075751918"
    else:
        gif = f"https://tenor.com/view/fear-and-hunger-coin-toss-coin-toss-heads-gif-2501105449971185509"
    await ctx.send(result)
    await ctx.send(gif)
    

@bot.command(name='roll')
async def roll(ctx):
    result = random.randint(1, 6)
    await ctx.send(f"The dice rolled: **{result}**")

@bot.command(name='fetch')
async def student_details(ctx, name: str):
    if name == "random":
        student = scraper.get_student_details(str(random.randint(1, 61)), data_path)
    else: 
        student = scraper.get_student_details(name, data_path)
    if student:
        message = "**Student details found:**\n"
        for key, value in student.items():
            message += f"**{key}**: {value}\n"
        await ctx.send(message)
    else:
        await ctx.send("Student not found.")


@bot.command(name='list')
async def list_details(ctx, parameter: str, roll_numbers_str: str):
    results = scraper.get_students_details(roll_numbers_str, parameter, data_path)
    message = ""
    for roll_number, detail in results.items():
        if detail:
            message += f"**{roll_number}**: {detail}\n"
        else:
            message += f"**{roll_number}**: Not found or no {parameter}\n"
    await ctx.send(message)


@bot.command(name='bday')
async def bday(ctx, skip: int = 0):
    bday = scraper.get_nearest_birthday(data_path, skip)
    message = f"Next Birthday is on **{bday[1]}** of **{bday[0]}** :cake:\n"
    await ctx.send(message)

@bot.command(name="makaut")
async def update_data(ctx):
    new_data = scraper.fetch_data_from_website(URL)
    previous_data = scraper.read_data_from_csv(DATA)
    new_links = [link for link in new_data if link not in previous_data]
    new_content = [(link, new_data[link]) for link in new_links]
    scraper.write_data_to_csv(DATA, new_data)
    if not new_links:
        await ctx.send("No new links.")
    else:
        message = f"Scraping makaut's website: {URL}\n"
        message += "New links and content:\n"
        for link, content in new_content:
            message += f"Content: **{content}**\n"
        await ctx.send(message)

@bot.command(name='quote')
async def quote(ctx):
    response = requests.get('https://api.quotable.io/random')
    if response.status_code == 200:
        data = response.json()
        quote = data['content']
        await ctx.send(f"Quote: {quote}")
    else:
        await ctx.send("Failed to fetch a quote.")


@bot.command(name='anon')
async def send_anonymous_message(ctx, *, message):
    await ctx.message.delete()
    await ctx.send(f"Someone said: {message}")

bot.run(os.getenv("BOT_TOKEN"))
