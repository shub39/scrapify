import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import scraper

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
tree = bot.tree
url = 'https://www.makautexam.net/announcement.html'
csv_file_path = 'data.csv'

@tree.command(name="sylvian", description="Summon Sylvian!")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Sylvian severed ties with humanity long ago, yet her presence continues to permeate the world. In Fear & Hunger, an unique encounter known as Traces of Sylvian serves as a manifestation of her lingering essence.")

@bot.event
async def on_ready():
    print("Sylvian's presence is strong.")
    await tree.sync()

@bot.command(name="purge")
async def purge(ctx, amount: int):
    if ctx.author.guild_permissions.manage_messages:
        await ctx.channel.purge(limit=amount + 1)  
        await ctx.send(f"Deleted {amount} messages.")
    else:
        await ctx.send("You do not have permission to use this command.")

@bot.command(name="makaut")
async def update_data(ctx):
    new_data = scraper.fetch_data_from_website(url)
    previous_data = scraper.read_data_from_csv(csv_file_path)
    new_links = [link for link in new_data if link not in previous_data]
    new_content = [(link, new_data[link]) for link in new_links]
    scraper.write_data_to_csv(csv_file_path, new_data)
    if not new_links:
        await ctx.send("No new links.")
    else:
        message = f"Scraping makaut's website: {makaut}\n"
        message += "New links and content:\n"
        for link, content in new_content:
            message += f"Content: **{content}**\n"
        await ctx.send(message)


bot_token = os.getenv("BOT_TOKEN")

bot.run(bot_token)
