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
makaut_url = 'https://www.makautexam.net/announcement.html'
makaut_path = 'data.csv'

@bot.command(name="purge")
async def purge(ctx, messages: int):
    if ctx.author.guild_permissions.manage_messages:
        await ctx.channel.purge(limit=messages + 1)
        await ctx.send(f"Deleted {messages} messages.")
    else:
        await ctx.send("You do not have permission to use this command.")

@bot.command(name='coin')
async def flipcoin(ctx):
    result = random.choice(['Heads', 'Tails'])
    await ctx.send(f"The coin landed on: **{result}**")

@bot.command(name='roll')
async def roll(ctx):
    result = random.randint(1, 6)
    await ctx.send(f"The dice rolled: **{result}**")

@bot.command(name='fetch')
async def student_details(ctx, name: str):
    if name == "random":
        student = scraper.get_student_details(str(random.randint(1, 61)))
    else: 
        student = scraper.get_student_details(name)
    if student:
        message = "**Student details found:**\n"
        for key, value in student.items():
            message += f"**{key}**: {value}\n"
        await ctx.send(message)
    else:
        await ctx.send("Student not found.")

@bot.command(name='bday')
async def bday(ctx):
    bday = scraper.get_nearest_birthday()
    message = f"Next Birthday is on **{bday[1]}** of **{bday[0]}** :cake:\n"
    await ctx.send(message)

@bot.command(name="makaut")
async def update_data(ctx):
    new_data = scraper.fetch_data_from_website(makaut_url)
    previous_data = scraper.read_data_from_csv(makaut_path)
    new_links = [link for link in new_data if link not in previous_data]
    new_content = [(link, new_data[link]) for link in new_links]
    scraper.write_data_to_csv(makaut_path, new_data)
    if not new_links:
        await ctx.send("No new links.")
    else:
        message = f"Scraping makaut's website: {makaut_url}\n"
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

@tasks.loop(hours=6)
async def scheduled_task():
    channel = discord.utils.get(bot.get_all_channels(), name='makaut-updates')
    new_data = scraper.fetch_data_from_website(makaut_url)
    previous_data = scraper.read_data_from_csv(makaut_path)
    new_links = [link for link in new_data if link not in previous_data]
    new_content = [(link, new_data[link]) for link in new_links]
    scraper.write_data_to_csv(makaut_path, new_data)
    if new_links:
        message = f"Scraping makaut's website: {makaut_url}\n"
        message += "New links and content:\n"
        for link, content in new_content:
            message += f"Content: **{content}**\n"
        await channel.send(message)

@scheduled_task.before_loop
async def before_scheduled_task():
    await bot.wait_until_ready()

bot.run(os.getenv("BOT_TOKEN"))

