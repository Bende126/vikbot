from contextlib import nullcontext
import discord
from discord.ext import commands
from discord.ext.commands import cog
from discord.utils import get
from discord_slash import client, cog_ext, SlashContext
import uuid
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import json
import asyncio
import urllib.request, json 


password_provided = "asdw"  
password = password_provided.encode()  
salt = b'\x81t\xd4C+\x92\x82O\xd0\x18du\xb6}\xcd\x7f'

auth_options = [
    {
        "name":"token",
        "description":"Ezzel a tokennel csatlakozol a szerverhez",
        "required": True,
        "type":3
    },
    {
        "name":"displayname",
        "description":"Ez a név lesz látható mások számára a szerveren",
        "required": True,
        "type":3
    }
]

def decode(msg):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
        )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    f = Fernet(key)

    decoded = f.decrypt(msg)
    return decoded

def encode(msg):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
        )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    f = Fernet(key)

    encoded = f.encrypt(msg.encode())
    print(encoded)
    return encoded

async def socketserver():
    server = await asyncio.start_server(
        handle_echo, '45.32.155.246', 2222)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

def save_token(tempdict):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
        )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    f = Fernet(key)

    loadedtoken = load_token()
    #saveddict = {**tempdict, **loadedtoken}
    saveddict = loadedtoken.copy()
    saveddict.update(tempdict)
    print(saveddict)

    toencrypt = json.dumps(saveddict).encode()
    encrypted = f.encrypt(toencrypt).decode()

    with open("mc/accounts.json", "w") as fp:
        json.dump(encrypted, fp)

    print("saved token")

def load_token():
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
        )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    f = Fernet(key)
    with open("mc/accounts.json", "r") as fp:
        loadeddict = json.loads(fp.read())
    if not loadeddict:
        return loadeddict

    todecrypt = json.dumps(loadeddict).encode()
    returndict = f.decrypt(todecrypt).decode()

    print(json.loads(returndict))
    #print(f"\n{key}\n")
    return json.loads(returndict)

async def handle_echo(reader, writer):
    size = await reader.read(4)
    data = await reader.read(int.from_bytes(size, "big"))
    print(int.from_bytes(size, "big"))
    print(data)
    message = decode(msg=data)
    addr = writer.get_extra_info('peername')
    print(f"Connection from {addr}")
    tempdict = load_token()
    recdict = json.loads(message)

    #print(f"Received {message!r} from {addr!r}")
    for token in list(tempdict.keys()):
        if tempdict[token]["token"] == recdict["token"]:
            sentdict = encode(msg=(json.dumps(tempdict[token])))
            bytenum = len(sentdict)
            writer.write(bytenum.to_bytes(4, "big"))
            writer.write(sentdict)
            print("küldve")
            await writer.drain()
            writer.close()
            await writer.wait_closed()
            return
            
    mydict = {"token": None}
    sentdict = encode(json.dumps(mydict))
    bytenum = len(sentdict)
    writer.write(bytenum.to_bytes(4, "big"))
    writer.write(sentdict)
    await writer.drain()
    print("küldve üres")
    writer.close()
    await writer.wait_closed()

    #print(f"Send: {message!r}")
    #writer.write(data)
    #await writer.drain()

    #print("Close the connection")
    #writer.close()

class mcauth(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('mcauth is ready')

    @commands.command()
    async def testcog_mcauth(self, ctx):
        await ctx.send("Cog is ready")

    @cog_ext.cog_slash(name="token", description="Megmutatja a regisztrált tokent", options=None)
    async def token_slash(self, ctx: SlashContext):
        await ctx.defer(hidden=True)
        tmpdict = load_token()
        token = tmpdict[str(ctx.author.id)]["token"]
        dpname = tmpdict[str(ctx.author.id)]["displayname"]
        await ctx.send(content=f"Token: {token} | Displayname: {dpname}", hidden=True)
        print("showed token")

    @cog_ext.cog_slash(name="mcauth", description="Nem eredetis játékosok ezzel tudnak karaktert regisztrálni", options=auth_options)
    async def mcauth_slash(self, ctx: SlashContext, token, displayname):
        await ctx.defer(hidden=True)
        tmpdict = load_token()
        accountdict = {}

        accountdict["id"] = str(uuid.uuid5(uuid.NAMESPACE_DNS, token))
        accountdict["token"] = token
        accountdict["displayname"] = displayname

        if str(ctx.author.id) in list(tmpdict.keys()):
            accountdict["id"] = tmpdict[str(ctx.author.id)]["id"]

        for id in tmpdict:
            if tmpdict[id]["token"] == token or tmpdict[id]["displayname"] == token or tmpdict[id]["token"] == displayname or tmpdict[id]["displayname"] == displayname:
                await ctx.send(content="A `token` és `displayname` nem egyezhet két offline játékos között", hidden=True)
                return

        with urllib.request.urlopen(f"https://api.mojang.com/users/profiles/minecraft/{displayname}") as url1:
            getname = url1.read().decode()

        with urllib.request.urlopen(f"https://api.mojang.com/users/profiles/minecraft/{token}") as url2:
            gettoken = url2.read().decode()

        if gettoken == "" and getname == "" and token!= displayname :
                tmpdict[str(ctx.author.id)] = accountdict
                save_token(tempdict=tmpdict)
                await ctx.send(content="Saved account", hidden=True)
                print("saved new user")
        else:
            await ctx.send(content="Nem használhatsz online accountot `token`-ként és `displayname`-ként. A `token` és `displayname` nem egyezhet. :triumph:", hidden=True)

    @commands.command()
    async def start_server(self, ctx):
        #asyncio.run(socketserver())
        await ctx.send(content="server started")
        await socketserver()
        print("server started")

def setup(client):
    client.add_cog(mcauth(client))

