import asyncio
import random
import emoji

class Interpreter:
    async def message_and_reply(self, *conditions, expected_message, any_message, reply:str,reaction=None, multi_reply:list=None):
        
        all_condiction_is_true = conditions.count(True) == len(conditions)
        all_condiction_is_false = conditions.count(False) == len(conditions)
        
        reply = reply[random.randint(0, (len(reply)-1))] if type(reply) == list else reply
        if reaction:
            reaction = emoji.emojize(reaction[random.randint(0, (len(reaction)-1))]) if type(reaction) == list else emoji.emojize(reaction)
        # reaction = reaction[random.randint(0, (len(reaction)-1))] if type(reaction) == list else reaction
        message_condiction = any_message.content == expected_message if type(expected_message) == str else any_message.content in expected_message

        canal = any_message.channel

        if multi_reply:
            for reply in multi_reply:
                reply = reply[random.randint(0,(len(reply)-1))] if type(reply) == list else reply
                if all_condiction_is_true and message_condiction:
                    await canal.send(reply)
                    if reaction:
                        await any_message.add_reaction(reaction)
        
        else:
            if all_condiction_is_true and message_condiction:
                await canal.send(reply)
                if reaction:
                    await any_message.add_reaction(reaction)

