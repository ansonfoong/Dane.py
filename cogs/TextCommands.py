import discord
from utils import *
from discord.ext import commands
import courses
import random
from database.database import *

class TextCommands(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.database = self.client.database
        
    @commands.command()
    async def help(self, ctx):
        await display_help(ctx, self.database)

    @commands.command()
    async def assign(self, ctx):
        await assignRole(self.client, ctx.message)

    ''' Remove a role from a user '''
    @commands.command()
    async def remove(self, ctx):
        await removeRole(self.client, ctx.message)

    @commands.command()
    async def course(self, ctx):
        await queryCourse(ctx, ctx.message)

    '''
    Command: Ban
    admin command to ban users
    '''
    @commands.command()
    async def ban(self, ctx, user_id, reason):
        await assignUserBan(ctx, user_id, reason)
    
    @commands.command()
    async def kick(self, ctx, user_id, reason):
        await kickUser(ctx, int(user_id), reason)
        
    @commands.command()
    async def dice(self, ctx):
        message = ctx.message
        await message.channel.send('Would you like to roll the die? Y/N')
        def check(m):
            return (m.content.lower() == 'y' or m.content.lower() == 'yes') and m.author.id == message.author.id
        
        msg = await self.client.wait_for('message', check=check)
        await message.channel.send('You rolled a ' +str(random.randint(1, 6)))

    @commands.command()
    async def unmute(self, ctx, user_id):
        message = ctx.message
        member_to_unmute = discord.utils.get(message.guild.members, id=int(user_id))
        if member_to_unmute is not None:
            print("Trying to unmute " + member_to_unmute.name)
            muted_role = discord.utils.get(message.guild.roles, name='Muted by Dane')
            if muted_role is not None:
                await member_to_unmute.remove_roles(muted_role, reason="Unmuted by admin.")
            else:
                print("Muted by Dane role was not found.")
        else:
            print("Member not found")

    @commands.command()
    async def mute(self, ctx, user_id, mute_reason):
        message = ctx.message
        member_to_mute = discord.utils.get(ctx.guild.members, id=int(user_id))
        mute_role = discord.utils.find(lambda role: role.name=='Muted by Dane', ctx.guild.roles)

        try:
            if mute_role is not None:
                print("Muting user.")
                await member_to_mute.add_roles(mute_role, reason="Muted by admin")
            else:
                print("Role does not exist.")
        except Exception as err:
            print(err)


def setup(bot):
    bot.add_cog(TextCommands(bot))