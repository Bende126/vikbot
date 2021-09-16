import discord
from discord.enums import try_enum
from discord.ext import commands, tasks
import requests
from discord_slash import client, cog_ext, SlashContext
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import json
from datetime import datetime

password_provided = "asd"  
password = password_provided.encode()  
salt = b'\x81t\xd4C+\x92\x82O\xd0\x18du\xb6}\xcd\x7f'  

login_options = [
    {
    "name":"username",
    "description":"Felhasználóneved",
    "required": True,
    "type":3
    },

    {
        "name":"passwd",
        "description":"Jelszavad",
        "required": True,
        "type": 3
    }
    ]

class jhside(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('jhside is ready')

    @commands.command()
    async def testcog_jhside(self, ctx):
        await ctx.send("Cog is ready")

    @cog_ext.cog_slash(name="Login", description = "Beléptet a doodleba", guild_ids = [308599429122883586], options = login_options)
    async def login_slash(self, ctx: SlashContext, username = "a", passwd = "b"):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )

        key = base64.urlsafe_b64encode(kdf.derive(password))  

        tempuserdict = {username:passwd}
        toencryptuser = json.dumps(tempuserdict).encode()
        f = Fernet(key)
        encrypteduser = f.encrypt(toencryptuser)
        tosaveuser = {}

        with open("doodle/accounts.json", "r") as fp:
            tosaveuser = json.loads(fp.read())

        tosaveuser[str(ctx.author.id)] = encrypteduser.decode()

        with open("doodle/accounts.json", "w") as fp:
            json.dump(tosaveuser, fp)
        
        await ctx.send(content=f"Logging in as {username} with password: {passwd}", hidden=True)
        with requests.Session() as s:
            res = s.post("https://doodle.com/api/v2.0/users/oauth/token", json={ "email": username, "password": passwd} ).json()
            print(res)
            if list(res.keys())[0] == "errorType":
                await ctx.send("Hibás felhasználónév/jelszó. Használd újra a /login parancsot.", hidden=True)
                return
        
            accessToken = res["accessToken"]
            tosaveacces = {}
            toencryptacces = accessToken.encode()
            encryptedacces = f.encrypt(toencryptacces)

            with open("doodle/acceskeys.json", "r") as fp:
                tosaveacces = json.loads(fp.read())
            
            tosaveacces[str(ctx.author.id)] = encryptedacces.decode()

            with open("doodle/acceskeys.json", "w") as fp:
                json.dump(tosaveacces, fp)
                
        await ctx.send(content="Fileba mentve :thumbsup:", hidden=True)

    @cog_ext.cog_slash(name="mypolls", description = "Listázza az általad csinált doodlekat", guild_ids=[308599429122883586], options=None)
    async def mypolls_slash(self, ctx: SlashContext):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password)) 
        f = Fernet(key)

        with open("doodle/acceskeys.json", "r") as fp:
            tempdict = json.loads(fp.read())

        for x in tempdict:
            if int(x) == int(ctx.author.id):
                todecrypt = tempdict[x].encode()
                acceskey = f.decrypt(todecrypt).decode()
                
        print(acceskey)
        
        with requests.Session() as s:
            s.get("https://doodle.com/api/v2.0/users/me/cookie-from-access-token", headers={ 'Access-Token': acceskey } )
            s.cookies.set("token", acceskey, domain="doodle.com")
            myPolls = s.get("https://doodle.com/np/users/me/dashboard/myPolls", params={ 'locale': 'en_EN', 'fullList': 'true', 'token': acceskey} ).json()
                        #otherPolls = s.get("https://doodle.com/np/users/me/dashboard/otherPolls", params={ 'locale': 'en_EN', 'fullList': 'true', 'token': accessToken } ).json()
                        #print(myPolls)
                        #print(otherPolls)
        if(len(myPolls) ==0):
            await ctx.send(content="Még nincs saját pollod", hidden=True)
            return
        print(myPolls)
        embed = discord.Embed(
        title = "Általad készített dudlik",
        colour = discord.Colour.blue(),
        timestamp = datetime.utcnow())
        embed.set_thumbnail(url= "https://w7.pngwing.com/pngs/56/568/png-transparent-doodle-app-store-computer-icons-android-mindmap-text-logo-android.png")
        for poll in myPolls["myPolls"]["myPolls"]:
            membernumber = poll["participantsCount"]
            pollid = poll["id"]
            lastactivity = poll["lastActivity"]
            embed.add_field(name=poll["title"], value=(f"Résztvevők: {membernumber}\n ID: {pollid}\n Útolsó aktivitás: {lastactivity}"), inline=False)
            await ctx.send(embed=embed, hidden=True)
                        #return
            #await ctx.send(content="Még nem jelentkeztél be, ezt megteheted a /login parancscsal", hidden=True)       

def setup(client):
    client.add_cog(jhside(client))

