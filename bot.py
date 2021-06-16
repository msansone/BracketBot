# encoding: utf-8

import bracket
import discord
import os
import subprocess

from discord.ext import commands
from dotenv import load_dotenv

debugMode = False

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

MAX_CHANNEL_NAME_SIZE = 32

bot = commands.Bot(command_prefix='!')

brackets = {}
 

@bot.command(name='addentries')
async def on_addentries(ctx, *args):
    
    bracketName = ctx.channel.name.replace('-', ' ')

    if bracketName in brackets.keys():       
        
        activeBracket = brackets[bracketName]
        
        if activeBracket.votingStarted == False:
   
            activeBracket.addEntries(args)
        
            await ctx.send(f"Added entries {', '.join(args)} to bracket {bracketName}.")
            
        else:
   
           await ctx.send(f"Can't add any more entries. Voting for {bracketName} has already started.")     

    else:
    
        await ctx.send(f"Bracket not found with name {bracketName}. Valid brackets are: {', '.join(brackets.keys())}")

@bot.command(name='bracket')
async def on_bracket(ctx):
    
    bracketName = ctx.channel.name.replace('-', ' ')
    
    await showBracket(ctx, bracketName)
    
    return
    
@bot.command(name='brackets')
async def on_brackets(ctx):
    
    bracketList = ""
    
    for bracketName in brackets.keys():
        
        bracketList += f" {bracketName}" 
    
    await ctx.send(f"Active brackets: {bracketList}.")
    
    return
    
@bot.command(name='createbracket')
async def on_createbracket(ctx, *args):
    
    bracketName = ""
    
    shuffle = True
    
    maxVotes = 0
    
    entries = []
    
    # Find the bracket name parameter
    for arg in args:
    
        if arg.upper().startswith("NAME="):
        
            # Read the name parameter.
            bracketName = arg.partition("=")[2].lower()
        
        elif arg.upper().startswith("SHUFFLE="):
            
            # Read the shuffle parameter.
            value = arg.partition("=")[2]
            
            if value.upper() == "TRUE":
            
                shuffle = True
                
        elif arg.upper().startswith("MAXVOTES="):
            
            # Read the max votes parameter.
            value = arg.partition("=")[2]
            
            try:

                maxVotes = (int)(value)
            
            except:
            
                maxVotes = 0
                       
        elif arg.upper().startswith("ENTRIES="):
        
            # Read the entries.            
            entries = arg.partition("=")[2].split(',')
            
            for i in range(0, len(entries)):
                
                entries[i] = entries[i].strip()

    if bracketName != "" and len(bracketName) <= MAX_CHANNEL_NAME_SIZE:
    
        # Create a channel for the bracket.
        guild = ctx.guild
    
        # Check if this exists already
        existing_channel = discord.utils.get(guild.channels, name=bracketName)
    
        if not existing_channel:
    
            print(f'Creating a new channel: {bracketName}')
        
            # Create a bracket object
            newBracket = bracket.Bracket(bracketName)
            
            newBracket.shuffle = shuffle
            
            newBracket.maxVotes = maxVotes
            
            newBracket.addEntries(entries)
        
            newBracket.save()
            
            brackets[bracketName] = newBracket
                    
            await guild.create_text_channel(bracketName)
            
            entriesToDisplay = ", ".join(entries)
            
            await ctx.send(f"Channel {bracketName} was created with entries: {entriesToDisplay}.")

        else:
    
            await ctx.send(f"A channel with the name {bracketName} already exists.")

    else:
        
        if len(bracketName) > MAX_CHANNEL_NAME_SIZE:
            
            await ctx.send(f"Bracket name can't be longer than {MAX_CHANNEL_NAME_SIZE} characters.")
            
        elif bracketName == "":
        
            await ctx.send(f"No bracket name was found in the parameters.")
            
@bot.command(name='debug')
async def on_debug(ctx, *args):
    
    # Various debug stuff as needed.
    print(type(args))
    
    print(" ".join(args))

    print(brackets.keys())
    
    bracketName = ctx.channel.name.replace('-', ' ')
    
    if bracketName in brackets:
            
        activeBracket = brackets[bracketName]
        
        print(activeBracket)
            
@bot.command(name='dentalplan')
async def on_dentalplan(ctx, *args):
    
    await ctx.send(f"Lisa needs braces.")
    
@bot.command(name='matchup')
async def on_matchup(ctx):
    
    # If this command was in a bracket channel, return the current match up.
    bracketName = ctx.channel.name.replace('-', ' ')
    
    if bracketName in brackets:       
        
        activeBracket = brackets[bracketName]

        if activeBracket.votingStarted == True:

            if len(activeBracket.winner) == 0:

                currentMatchup = activeBracket.currentMatchupString()

                await ctx.send(f"{currentMatchup}")
            
            else:
            
                await ctx.send(f"Voting has ended, {activeBracket.winner} is the winner!")
 
        else:
    
            await ctx.send(f"Voting for {bracketName} has not started.")            

    else:
    
        await ctx.send(f"Bracket not found with name {bracketName}. Valid brackets are: {', '.join(brackets.keys())}")


@bot.command(name='maxvotes')
async def on_maxvotes(ctx, maxVotes):
    
    bracketName = ctx.channel.name.replace('-', ' ')

    if bracketName in brackets.keys():       
        
        activeBracket = brackets[bracketName]
        
        try:
        
            activeBracket.maxVotes = int(maxVotes)
            
            activeBracket.save()
            
            await ctx.send(f"Vote threshold has been set to {maxVotes}.")
            
        except:
            
            await ctx.send(f"{maxVotes} is not a valid value.")

    else:
    
        await ctx.send(f"Bracket not found with name {bracketName}. Valid brackets are: {', '.join(brackets.keys())}")


@bot.event
async def on_message(message):

    if message.type == discord.MessageType.pins_add:
            
        await message.delete()

    await bot.process_commands(message)

@bot.command(name='nextmatchup')
async def on_nextmatchup(ctx):
    
    bracketName = ctx.channel.name.replace('-', ' ')
    
    if bracketName in brackets:       
        
        activeBracket = brackets[bracketName]
        
        if activeBracket.votingStarted == True:

            if len(activeBracket.winner) == 0:
            
                matchupResult = activeBracket.finalizeMatchup()
            
                currentMatchup = activeBracket.currentMatchupString()
        
                await showBracket(ctx, bracketName)
        
                await ctx.send(f"{matchupResult}")
            
                await ctx.send(f"{currentMatchup}")
            
            else:
            
                await ctx.send(f"Voting has ended, {activeBracket.winner} is the winner!")
            
        else:
   
           await ctx.send(f"Voting for {bracketName} has not started.")
            
    else:
    
        await ctx.send(f"Bracket not found with name {bracketName}. Valid brackets are: {', '.join(brackets.keys())}")
        
@bot.event
async def on_ready():

    guild = discord.utils.find(lambda g: g.name == GUILD, bot.guilds)
    
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})')
        
    # For each channel, try to load a bracket.
    for channel in guild.text_channels:
    
        bracketName = channel.name.replace('-', ' ')
    
        newBracket = bracket.Bracket(bracketName)
        
        if newBracket.load() == True:
        
            print(f"Bracket {bracketName} found")
            
            brackets[bracketName] = newBracket
        
        else:
        
            print(f"Bracket {bracketName} not found")
            
@bot.command(name='start')
async def on_start(ctx):

    bracketName = ctx.channel.name.replace('-', ' ')

    if bracketName in brackets:       

        activeBracket = brackets[bracketName]

        if activeBracket.votingStarted == False:

            activeBracket.startVoting()
            
            await showBracket(ctx, bracketName)   
            
            await ctx.send(f"Voting for {bracketName} now begins!")    
        else:
   
           await ctx.send(f"Voting for {bracketName} has already started.")

    else:
        
        await ctx.send(f"Bracket not found with name {bracketName}. Valid brackets are: {', '.join(brackets.keys())}")
        
@bot.command(name='vote')
async def on_vote(ctx,  *args):
    
    entryName = " ".join(args)
    
    # If this command was in a bracket channel, vote for an item in the current matchup, if it is valid    
    bracketName = ctx.channel.name.replace('-', ' ')
    
    if bracketName in brackets:       
        
        activeBracket = brackets[bracketName]
        
        if activeBracket.votingStarted == True:
        
            if len(activeBracket.winner) == 0:

                isValidVote = activeBracket.isValidVote(entryName)
                
                entryOne = activeBracket.rounds[activeBracket.currentRound][activeBracket.currentMatchup]
        
                entryTwo = activeBracket.rounds[activeBracket.currentRound][activeBracket.currentMatchup + 1]
                                
                # If it's not a valid vote, check for shorthand
                if isValidVote == False:
                
                    if entryName.upper() == "A":
                        
                        entryName = entryOne.entryName
                        
                        isValidVote = True
                        
                    elif entryName.upper() == "B":
                        
                        entryName = entryTwo.entryName
                        
                        isValidVote = True
                
                if isValidVote == True:
        
                    voteChanged = activeBracket.registerVote(ctx.author.name, entryName)
            
                    if voteChanged == False:
                        
                        await showBracket(ctx, bracketName)
                
                        await ctx.send(f"{ctx.author.name} voted for {entryName}")
                        
                    else:
                        
                        await showBracket(ctx, bracketName)
                
                        await ctx.send(f"{ctx.author.name} changed their vote to {entryName}")
             
                    # If the max votes is set to something more than 0, move to the next matchup
                    # automatically if that number of votes has been reached.
                    if activeBracket.maxVotes > 0:
        
                        entryOne = activeBracket.rounds[activeBracket.currentRound][activeBracket.currentMatchup]
        
                        entryTwo = activeBracket.rounds[activeBracket.currentRound][activeBracket.currentMatchup + 1]
        
                        if len(entryOne.votes) + len(entryTwo.votes) >= activeBracket.maxVotes:
                        
                            await on_nextmatchup(ctx)

                else:
        
                    await ctx.send(f"{entryName} is not a valid vote.")        
                
                    currentMatchup = activeBracket.currentMatchupString()
        
                    await ctx.send(f"{currentMatchup}")

            else:
            
                await ctx.send(f"Voting has ended, {activeBracket.winner} is the winner!")
                
        else:
        
            await ctx.send(f"Voting has not yet begun for {bracketName}.")
    
    else:
    
        await ctx.send(f"Bracket not found with name {bracketName}. Valid brackets are: {', '.join(brackets.keys())}")
        
@bot.command(name='votes')
async def on_votes(ctx):
    
    # If this command was in a bracket channel, return the current match up.
    bracketName = ctx.channel.name.replace('-', ' ')
    
    if bracketName in brackets:       
        
        activeBracket = brackets[bracketName]

        if activeBracket.votingStarted == True:
        
            if len(activeBracket.winner) == 0:
                    
                currentVotes = activeBracket.currentVotes()
        
                await ctx.send(f"{currentVotes}")
 
            else:
            
                await ctx.send(f"Voting has ended, {activeBracket.winner} is the winner!")
                
        else:
        
            await ctx.send(f"Voting has not yet begun for {bracketName}.")
       
    else:
    
        await ctx.send(f"Bracket not found with name {bracketName}. Valid brackets are: {', '.join(brackets.keys())}")
        
async def showBracket(ctx, bracketName):

    if bracketName in brackets:       
        
        activeBracket = brackets[bracketName]

        # Generate the bracket image.        
        command = f"BracketImageGeneratorTool.exe \"{bracketName}\" "
        
        command += f"{activeBracket.currentRound} {(int)(activeBracket.currentMatchup/2)} "
        
        for i in range(0, len(activeBracket.rounds)):
        
            entriesForRound = ""
        
            for bracketEntry in activeBracket.rounds[i]:
        
                if len(entriesForRound) > 0:
            
                    entriesForRound += "|"

                entriesForRound += f"{bracketEntry.entryName}|{len(bracketEntry.votes)}"
        
            command += f"\"{entriesForRound}\" "
        
        command += f"\"{activeBracket.winner}\" "
        
        if debugMode == True:
        
            print(command)
        
        return_code = subprocess.call(command, shell=True)
        
        bracketImageFilename = bracketName.replace(' ', '_')
        
        if activeBracket.pinnedDiscordMessageId != 0:
        
            try:

                msgToDelete = await ctx.channel.fetch_message(activeBracket.pinnedDiscordMessageId)

                await msgToDelete.delete()
            
            except:
            
                print("Couldn't delete image")
        
        msg = await ctx.channel.send(file=discord.File(f"brackets\\{bracketImageFilename}.png"))
            
        activeBracket.pinnedDiscordMessageId = msg.id
        
        await msg.pin()
    
        activeBracket.save()

bot.run(TOKEN)