# bot.py
import logging
import os
import re
import sys

import discord
import emoji
from dotenv import load_dotenv
from tinydb import Query, TinyDB, where

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

BOT_PREFIX = "!sylwek"

EMOJI_REGEX_PATTERN = r"<:[\w_]*:(\d*)>"
EMOJI_REGEX = re.compile(EMOJI_REGEX_PATTERN)

stdout_handler = logging.StreamHandler(sys.stdout)
# file_handler = logging.FileHandler(filename='/srv/bot.log')

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(stdout_handler)


# LOGGER.addHandler(file_handler)


class SylwekClient(discord.Client):
    """
    Discord client implementation
    """

    def __init__(self, user_db, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.commands = {
            "życzenia": self._handle_command_wish,
            "zyczenia": self._handle_command_wish,
            "rzyczenia": self._handle_command_wish,
            "pomocy": self._handle_command_help,
            "emoji": self._handle_command_emoji,
            "nazywajmnie": self._handle_command_callme,
            "fajerwerki": self._handle_command_fireworks,
        }
        self.user_db = user_db

    async def on_ready(self):
        LOGGER.info(f"{self.user} has connected to Discord!")

    async def on_message(self, message):
        if message.author == self.user:
            return

        LOGGER.debug(
            "got new not-self message: '%s' from '%s'",
            message.content,
            message.author.name,
        )

        components = message.content.split()

        if message.guild is None:
            return await self._handle_command(message, components)
        else:
            if components[0] == BOT_PREFIX:
                return await self._handle_command(message, components[1:])
            elif self.user in message.mentions:
                return await self._handle_command(message, components[1:])

    async def _handle_command(self, message, components):

        if len(components) < 1:
            return await self._handle_command_help(message, [])

        command_name = components[0]
        params = components[1:]
        LOGGER.info(f"got command: {command_name}, {params}")

        if command_name not in self.commands:
            return await self._handle_command_help(message, [])

        command = self.commands[command_name]
        return await command(message, params)

    async def _handle_command_wish(self, message, params):
        user_id = message.author.id
        found = self.user_db.search(where("user_id") == user_id)
        alias = message.author.name
        if len(found) > 0:
            alias = found[0]["alias"]
        await message.channel.send(f"Hello {alias}!")

    async def _handle_command_emoji(self, message, params):
        if len(params) == 0:
            return
        em = params[0]
        emoji_match = EMOJI_REGEX.match(em)

        if emoji_match:
            emoji_id = int(emoji_match.group(1))
            discord_emoji = self.get_emoji(emoji_id)
            LOGGER.info(discord_emoji.url)
            await message.channel.send(f"emoji URL: {discord_emoji.url}")
        msg = f"emoji: {em} {emoji.demojize(em)}"
        LOGGER.info(msg)
        await message.channel.send(msg)

    async def _handle_command_fireworks(self, message, params):
        return

    async def _handle_command_callme(self, message, params):
        user = Query()
        alias = " ".join(params)
        self.user_db.upsert(
            {"user_id": message.author.id, "alias": alias},
            user.user_id == message.author.id,
        )
        await message.channel.send(f"Siema {alias} aka {message.author.name}!")

    async def _handle_command_help(self, message, params):
        text = """
:blue_circle: `emoji` - `!sylwek emoji <emoji>` - dodaj emotke <emoji> i bedzie fajnie
:blue_circle: `pomocy` - `!sylwek pomocy` - zobacz pomoc jak z tego korzystać typie
:blue_circle: `życzenia`, `zyczenia`, `rzyczenia` - `!sylwek życzenia <Moje życzenia>` - złóż życzenia <Moje życzenia>
:blue_circle: `nazywajmnie` - `!sylwek nazywajmnie <imie>` - ustaw sobie imię na <imię> mordo
:blue_circle: `fajerwerki` - `!sylwek fajerwerki <efekt> [kolor]` - dodaj fajerwerki typu <efekt> z kolorem <kolor>, dostępne efekty ziomuś to:
        :red_circle:  `normalny` - no normalne fajerwerki takie najbardziej typowe
"""
        await message.channel.send(text)


def run_discord_client():
    """
    Run discord client event loop
    """
    LOGGER.info("Starting client")
    db_path = "./data/users.db"
    user_db = TinyDB(db_path)
    client = SylwekClient(user_db)
    client.run(TOKEN)
