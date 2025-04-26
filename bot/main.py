import asyncio
import json
from logging import exception
import os
import discord
from discord.ext import commands
from discord import AllowedMentions, app_commands, channel
import aiohttp # handles async HTTP requests
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

roll_url = "http://localhost:8000/roll"
schedule_url = "http://localhost:8000/reminder"
customweapon_url = "http://localhost:8000/customweapon"
lookup_url = "http://localhost:8000/search"
reminders_due = "http://localhost:8000/reminders_due"
mark_sent = "http://localhost:8000/mark_sent"
character_url = "http://localhost:8000/api/character"
attack_url = "http://localhost:8000/api/attack"

class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self) -> None:
        await super().setup_hook()
        await self.tree.sync()
        self.loop.create_task(self.check_reminders())
       #setups the reminders loop
    async def check_reminders(self):
        await self.wait_until_ready()
        while not self.is_closed():
            try:
                await self.fetch_and_send_reminders()
            except Exception as e:
                print(f"Reminder loop error: {e}")
            await asyncio.sleep(60)

    async def fetch_and_send_reminders(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(reminders_due) as resp:
                if resp.status == 200:
                    reminders = await resp.json()
                    for reminder in reminders:
                        channel = self.get_channel(int(reminder["channel_id"]))
                        if channel:
                            if isinstance(channel, discord.TextChannel):
                                print(f"Sending reminder to {channel.id}")
                                await channel.send(f"@everyone {reminder["message"]}",allowed_mentions=AllowedMentions(everyone=True))
                                async with aiohttp.ClientSession() as session:
                                    await session.post(mark_sent, json={"id": reminder["id"]})
                                await asyncio.sleep(1)
                            else:
                                print(f"Error cannot send message to channel")
    async def on_ready(self):
        print(f'We have logged in as {self.user}')

client = Client()

# slash command for rolling dice
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

# slash command for creating a custom weapon
@client.tree.command(name="customweapon", description="Create a custom weapon.")
@app_commands.describe(name="Weapon name", damage="weapon damage", range="weapon range")
async def customweapon(interaction: discord.Interaction, name: str, damage: str, range: str):
    await interaction.response.defer()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(customweapon_url, params={"name": name, "damage": damage, "range": range}) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    await interaction.followup.send((data[0]))
                else:
                    error_message = await resp.text()
                    await interaction.followup.send(f"Failed to create weapon. Server said: {error_message}")
    except Exception as e:
        await interaction.followup.send(f"an error occurred: {e}")


# slash command for scheduler
@client.tree.command(name="reminder", description="set a reminder with a date and time")
@app_commands.describe(date="Date in YYYY-MM-DD", time="Time in HH:MM (24hr)", message="Reminder message")
async def reminder(interaction: discord.Interaction, date: str, time: str, message: str):
    await interaction.response.defer()

    channel_id = str(interaction.channel_id)

    params = {
        "date": date,
        "time": time,
        "message": message,
        "channel_id": channel_id
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(schedule_url, params=params) as resp:
            if resp.status == 200:
                result = await resp.json()
                await interaction.followup.send(f"{result}")
            else:
                await interaction.followup.send("Failed to schedule")

# slash command for lookup
@client.tree.command(name="lookup", description="search a specific type of entity")
@app_commands.describe(name="the name of the entity", ltype="enter monster or weapons")
async def lookup(interaction: discord.Interaction, name: str, ltype: str):
    await interaction.response.defer()

    async with aiohttp.ClientSession() as session:
        async with session.get(lookup_url, params={"name": name, "ltype": ltype}) as resp:
            if resp.status == 200:
                result = await resp.json()
                await interaction.followup.send(f"{name} is found in the {ltype} data table")
            else:
                await interaction.followup.send("Failed to search entity.")

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
            "name":name, "player_id": str(interaction.user.id), "hp": hp, "ac": ac, "level": level, "race": race, "char_class": char_class
        }) as resp:
            if resp.status == 200:
                await interaction.followup.send(f"Character `{name}` updated!")
            else:
                error_message = await resp.text()
                await interaction.followup.send(f"Failed to update character. Server said: {error_message}")

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
                error_message = await resp.text()
                await interaction.followup.send(f"Failed to attack. Server said: {error_message}")


client.run(os.getenv("DISCORD_BOT_TOKEN"))
