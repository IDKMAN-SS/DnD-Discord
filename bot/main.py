import os
import discord
from discord.ext import commands
from discord import app_commands
import aiohttp # handles async HTTP requests
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True


roll_url = "http://localhost:8000/roll"

class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()

    async def on_ready(self):
        print(f'We have logged in as {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')

intents = discord.Intents.default()
intents.message_content = True
#client = Client(command_prefix="!", intents=intents)
client = Client()

'''
Example for commands to take in arguments:

@client.tree.command(name="printer", description="I will print what you give me")
async def printer(interaction: discord.Interaction, printer: str):
    await interaction.response.send_message(printer)

'''

# slash command for rolling dice
@client.tree.command(name="roll", description="roll a die")
async def roll(interaction: discord.Interaction, dice: str):
    await interaction.response.defer()  # Acknowledge the interaction

    async with aiohttp.ClientSession() as session:
        async with session.get(roll_url, params={"q": dice}) as resp:
            if resp.status == 200:
                result = await resp.json()
                await interaction.followup.send(f"You rolled `{dice}` and got: {result}")
            else:
                await interaction.followup.send("Error contacting the dice roller API.")

client.run(os.getenv("DISCORD_BOT_TOKEN"))
