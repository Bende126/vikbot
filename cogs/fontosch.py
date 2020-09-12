import discord
from discord.ext import commands, tasks
import sqlite3
from sqlite3 import Error

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

connection = create_connection("reactions.db")

class reactions(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('reactionroles are ready')
        create_channels_table = """
                CREATE TABLE IF NOT EXISTS channels (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  message INTEGER,
                  channel INTEGER,
                  count INTEGER,
                  newmessage INTEGER
                );
                """
        execute_query(connection, create_channels_table)
        create_channels = f"""
                        INSERT INTO
                            channels (message, channel, count, newmessage)
                        VALUES
                            (753696878616641648, 308599429122883586, 1, 754254146168684555)
                        """
        execute_query(connection, create_channels)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        member = await self.client.fetch_user(payload.user_id)
        csanel = self.client.get_channel(payload.channel_id)
        msg = await csanel.fetch_message(payload.message_id)

        newschannel = self.client.get_channel(745883081310732379)

        if str(payload.emoji) == '❗':
            select_channels = """
            SELECT
                message
            FROM
                channels
            """
            channels = execute_read_query(connection, select_channels)
            for x in channels:
                res = int(''.join(map(str, x)))
                if msg.id == int(res):
                    print('yeey') #itt hozzáadok ha létezik
                    select_count = """
                                SELECT
                                    count
                                FROM
                                    channels
                                """
                    count = execute_read_query(connection, select_count)
                    for x in count:
                        res = int(''.join(map(str, x)))
                        newcount = int(res)+1
                    update_count = f"""
                    UPDATE
                        channels
                    SET
                        count = {newcount}
                    WHERE
                        message = {msg.id}
                    """
                    execute_query(connection, update_count)
                    return
                else:
                    print('naez') #itt létrehozom és posztolom
                    newmessage_id = newschannel.last_message_id
                    create_channels = f"""
                                        INSERT INTO
                                            channels (message, channel, count, newmessage)
                                        VALUES
                                            ({msg.id}, {csanel.id}, 1, {newmessage_id})
                                        """
                    execute_query(connection, create_channels)
                    await newschannel.send(f"{member.mention} szerint ez fontos infó```{msg.content}```Az eredeti üzenet megtekinthető itt:\n{msg.jump_url}")
                    return

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        
        member = await self.client.fetch_user(payload.user_id)
        csanel = self.client.get_channel(payload.channel_id)
        msg = await csanel.fetch_message(payload.message_id)

        newschannel = self.client.get_channel(745883081310732379)

        if str(payload.emoji) == '❗':
            select_channels = """
            SELECT
                message
            FROM
                channels
            """
            channels = execute_read_query(connection, select_channels)
            for x in channels:
                res = int(''.join(map(str, x)))
                if msg.id == int(res):
                    print('yeey')
                    select_count = """
                                SELECT
                                    count
                                FROM
                                    channels
                                """
                    count = execute_read_query(connection, select_count)
                    for x in count:
                        res = int(''.join(map(str, x)))
                        newcount = int(res)-1
                        update_count = f"""
                        UPDATE
                            channels
                        SET
                            count = {newcount}
                        WHERE
                            message = {msg.id}
                        """
                        execute_query(connection, update_count)
                        if newcount == 0:
                            select_message = """
                                        SELECT
                                            newmessage
                                        FROM
                                            channels
                                        WHERE
                                            count = 0
                                        """
                            newmessage_id = execute_read_query(connection, select_message)
                            res = int(float(''.join(map(str, newmessage_id))))#hogyafaszomba rakom át ezt integerbe
                            print(res)
                            message = await newschannel.fetch_message(res)
                            await message.delete(delay= None)
                            await newschannel.send(f"Nem fontosként megjelölt. Az eredeti üzenet továbbra is megtekinthető itt:\n{msg.jump_url}")
                            return
                        return

    @commands.command()
    async def print(self, ctx):
        select_channels = """
        SELECT
            message,
            count
        FROM
            channels
        """
        channels = execute_read_query(connection, select_channels)
        for x in channels:
            print(x)
            res = int(''.join(map(str, x)))
            print(str(res))

    @commands.command()
    async def reacc(self, ctx):
        msg = await ctx.fetch_message(753696878616641648)
        await msg.add_reaction('❗')

def setup(client):
    client.add_cog(reactions(client))

