import os
import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

roll_url = "http://localhost:8000/roll"
schedule_url = "http://localhost:8000/reminder"
customweapon_url = "http://localhost:8000/customweapon"
lookup_url = "http://localhost:8000/search"
character_url = "http://localhost:8000/api/character"
attack_url = "http://localhost:8000/api/attack"

GUILD_ID = 1359588987391578342

class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def startup(self) -> None:
        await self.wait_until_ready()
        guild = discord.Object(id=GUILD_ID)
        await self.tree.sync(guild=guild)

    async def setup_hook(self) -> None:
        await super().setup_hook()
        self.loop.create_task(self.startup())

    async def on_ready(self):
        print(f'We have logged in as {self.user}')

client = Client()

@client.tree.command(name="roll", description="roll a die")
async def roll(interaction: discord.Interaction, dice: str):
    await interaction.response.defer()
    async with aiohttp.ClientSession() as session:
        async with session.get(roll_url, params={"dice": dice}) as resp:
            if resp.status == 200:
                result = await resp.json()
                await interaction.followup.send(f"You rolled `{dice}` and got: {result}")
            else:
                await interaction.followup.send("Error contacting the dice roller API.")

@client.tree.command(name="customweapon", description="Create a custom weapon.")
@app_commands.describe(name="Weapon name", damage="weapon damage", range="weapon range")
async def customweapon(interaction: discord.Interaction, name: str, damage: int, range: int):
    await interaction.response.defer()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(customweapon_url, params={"name": name, "damage": damage, "range": range}) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    await interaction.followup.send(f"Success! {data['name']} created successfully.")
                else:
                    error_message = await resp.text()
                    await interaction.followup.send(f"Failed to create weapon. Server said: {error_message}")
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {e}")

@client.tree.command(name="reminder", description="Set a reminder with a date and time")
@app_commands.describe(date="YYYY-MM-DD", time="HH:MM", message="Reminder message")
async def reminder(interaction: discord.Interaction, date: str, time: str, message: str):
    await interaction.response.defer()
    channel_id = str(interaction.channel_id)
    async with aiohttp.ClientSession() as session:
        async with session.post(schedule_url, json={"date": date, "time": time, "message": message, "channel_id": channel_id}) as resp:
            if resp.status == 200:
                result = await resp.json()
                await interaction.followup.send(f"{result}")
            else:
                await interaction.followup.send("Failed to schedule")

@client.tree.command(name="lookup", description="Search a specific type of entity")
@app_commands.describe(name="Entity name", ltype="monster or weapon")
async def lookup(interaction: discord.Interaction, name: str, ltype: str):
    await interaction.response.defer()
    async with aiohttp.ClientSession() as session:
        async with session.get(lookup_url, params={"name": name, "ltype": ltype}) as resp:
            if resp.status == 200:
                result = await resp.json()
                await interaction.followup.send(f"{name} found in {ltype} table")
            else:
                error_text = await resp.text()
                await interaction.followup.send(f"Failed to search entity. {error_text}")

@client.tree.command(name="create_character", description="Create a new character")
@app_commands.describe(name="Character name", hp="HP", ac="AC", level="Level", race="Race", char_class="Class")
async def create_character(interaction: discord.Interaction, name: str, hp: int, ac: int, level: int, race: str, char_class: str):
    await interaction.response.defer()
    async with aiohttp.ClientSession() as session:
        async with session.post(character_url, json={
            "name": name,
            "hp": hp,
            "ac": ac,
            "level": level,
            "race": race,
            "char_class": char_class,
            "player_id": str(interaction.user.id)
        }) as resp:
            if resp.status == 200:
                await interaction.followup.send(f"Character `{name}` created!")
            else:
                error_message = await resp.text()
                await interaction.followup.send(f"Failed to create character. {error_message}")

@client.tree.command(name="view_character", description="View a character by name")
@app_commands.describe(name="Character's name")
async def view_character(interaction: discord.Interaction, name: str):
    await interaction.response.defer()
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{character_url}/{name}") as resp:
            if resp.status == 200:
                character = await resp.json()
                await interaction.followup.send(f"Character details: `{character}`")
            else:
                await interaction.followup.send("Character not found.")

@client.tree.command(name="update_character", description="Update a character")
@app_commands.describe(name="Character's name", hp="HP", ac="AC", level="Level", race="Race", char_class="Class")
async def update_character(interaction: discord.Interaction, name: str, hp: int, ac: int, level: int, race: str, char_class: str):
    await interaction.response.defer()
    async with aiohttp.ClientSession() as session:
        async with session.put(f"{character_url}/{name}", json={
            "hp": hp, "ac": ac, "level": level, "race": race, "char_class": char_class
        }) as resp:
            if resp.status == 200:
                await interaction.followup.send(f"Character `{name}` updated!")
            else:
                await interaction.followup.send("Failed to update character.")

@client.tree.command(name="delete_character", description="Delete a character")
@app_commands.describe(name="Character's name")
async def delete_character(interaction: discord.Interaction, name: str):
    await interaction.response.defer()
    async with aiohttp.ClientSession() as session:
        async with session.delete(f"{character_url}/{name}") as resp:
            if resp.status == 200:
                await interaction.followup.send(f"Character `{name}` deleted!")
            else:
                await interaction.followup.send("Failed to delete character.")

@client.tree.command(name="attack", description="Attack another character")
@app_commands.describe(target_name="Target name", damage_dice="Damage dice (e.g. 1d6)")
async def attack(interaction: discord.Interaction, target_name: str, damage_dice: str):
    await interaction.response.defer()
    attacker_name = interaction.user.name
    async with aiohttp.ClientSession() as session:
        async with session.post(attack_url, json={
            "attacker_name": attacker_name,
            "target_name": target_name,
            "damage_dice": damage_dice
        }) as resp:
            if resp.status == 200:
                result = await resp.json()
                await interaction.followup.send(result["message"])
                if "Dead" in result["message"]:
                    target_user = discord.utils.get(interaction.guild.members, name=target_name)
                    if target_user:
                        try:
                            await target_user.send(f"Your character `{target_name}` has been killed in combat!")
                        except discord.Forbidden:
                            await interaction.followup.send(f"Could not DM {target_name}.")
            else:
                await interaction.followup.send("Attack failed.")

client.run(os.getenv("DISCORD_BOT_TOKEN"))
