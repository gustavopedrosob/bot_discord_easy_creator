import asyncio
import logging

import discord
import emoji
from discord import Intents, LoginFailure

from core.config import instance as config
from core.functions import random_choose
from core.messages import messages
from interfaces.main.log_handler import LogHandler
from interpreter.conditions import MessageConditions
from interpreter.variable import Variable

logger = logging.getLogger(__name__)


class Bot:

    def __init__(self):
        self.client = discord.Client(intents=Intents.all())

        @self.client.event
        async def on_ready():
            logger.info("Bot iniciado!")

        @self.client.event
        async def on_message(message: discord.Message):
            logger.info(f'Identificada mensagem "{message.content}".')

            for message_data in messages.content().values():
                await message_and_reply(
                    message=message,
                    conditions=message_data.get("conditions"),
                    expected_message=message_data.get("expected message"),
                    reply=message_data.get("reply"),
                    reaction=message_data.get("reaction"),
                    delete=message_data.get("delete"),
                    pin=message_data.get("pin"),
                    delay=message_data.get("delay"),
                    kick=message_data.get("kick"),
                    ban=message_data.get("ban"),
                    where_reply=message_data.get("where reply"),
                    where_reaction=message_data.get("where reaction"),
                )

        @self.client.event
        async def apply_delay(delay):
            delay = int(delay)
            logger.info(
                f"Aguardando delay de {delay} segundos para a proxima execução!"
            )
            await asyncio.sleep(delay)

        @self.client.event
        async def send_reaction(
            reactions: list[str], message: discord.Message, where: str
        ):
            for reaction in reactions:
                code_reaction = reaction
                reaction = (
                    random_choose(reaction) if isinstance(reaction, list) else reaction
                )
                reaction = emoji.emojize(reaction)
                try:
                    if where == "author":
                        await message.add_reaction(reaction)
                    elif where == "bot" and message.author.bot:
                        await message.add_reaction(reaction)
                    logger.info(
                        f'Adicionando a reação "{code_reaction}" a mensagem "{emoji.demojize(message.content)}" do autor {message.author}.'
                    )
                except discord.HTTPException:
                    print(reaction)

        @self.client.event
        async def send_reply(replies: list[str], message: discord.Message, where: str):
            for reply in replies:
                reply = random_choose(reply) if isinstance(reply, list) else reply
                reply = Variable(message).apply_variable(reply)
                if where == "group":
                    await message.channel.send(reply)
                elif where == "private":
                    dm_channel = await message.author.create_dm()
                    await dm_channel.send(reply)
                logger.info(
                    f'Enviando a resposta "{reply}" à mensagem "{emoji.demojize(message.content)}" do autor {message.author}.'
                )

        @self.client.event
        async def remove_message(message: discord.Message):
            await message.delete()
            logger.info(
                f'Removendo mensagem "{emoji.demojize(message.content)}" do autor {message.author}.'
            )

        @self.client.event
        async def pin_message(message: discord.Message):
            await message.pin()
            logger.info(
                f'Fixando mensagem "{emoji.demojize(message.content)}" do autor {message.author}.'
            )

        @self.client.event
        async def kick_member(member: discord.Member):
            await member.kick()
            logger.info(f'Expulsando jogador "{member.name}".')

        @self.client.event
        async def ban_member(member: discord.Member):
            await member.ban()
            logger.info(f'Banindo jogador "{member.name}".')

        async def message_and_reply(
            message: discord.Message,
            conditions: list[str],
            expected_message: str,
            reply: list[str],
            reaction: list[str],
            delete: bool,
            pin: bool,
            delay: int,
            ban: bool,
            kick: bool,
            where_reply: str = "group",
            where_reaction: str = "author",
        ):

            message_condition = MessageConditions(
                message, expected_message=expected_message
            )

            conditions_to_confirm = []
            if conditions:
                for each_conditions in conditions:
                    conditions_to_confirm.append(
                        message_condition.string_conditions[each_conditions]
                    )
            # é importante adicionar a condição expected message se tiver alguma mensagem esperada porque, senão podem ocorrer erros inesperados.
            if expected_message:
                conditions_to_confirm.append(message.content in expected_message)

            logger.info(f"Verificando condições {conditions_to_confirm}")

            if all(conditions_to_confirm):
                if delay:
                    await apply_delay(delay)
                if reply:
                    await send_reply(reply, message, where_reply)
                if reaction:
                    await send_reaction(reaction, message, where_reaction)
                if delete:
                    await remove_message(message)
                if pin:
                    await pin_message(message)
                if ban:
                    await ban_member(message.author)
                if kick:
                    await kick_member(message.author)

    def run(self):
        try:
            self.client.run(config.get("token"))
        except LoginFailure as exception:
            logger.info(str(exception))


class IntegratedBot(Bot):
    def __init__(self, app):
        self.app = app
        super().__init__()

        log_handler = LogHandler(self.app)
        log_handler.setLevel(logging.INFO)
        logger.addHandler(log_handler)

        @self.client.event
        async def on_ready():
            logger.info("Bot iniciado!")
            self.app.change_init_bot_button()


if __name__ == "__main__":
    bot = Bot()
    bot.run()
