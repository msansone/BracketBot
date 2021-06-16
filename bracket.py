import json
import math
import os
import random
import sys

class Bracket:

    # Constructor
    def __init__(self, bracketName):
    
        self._entries = []
        
        self.bracketName = bracketName
      
        # A list of rounds. Each round contains bracket slots 
        self.rounds = []
	           
        self.currentRound = 0
	        
        self.currentMatchup = 0
        
        self.votingStarted = False
        
        self.shuffle = False
        
        self.pinnedDiscordMessageId = 0
        
        self.winner = ""
        
        self.maxVotes = 0
        
        return

    # ToString
    def __str__(self):
    
        result = f"Bracket {self.bracketName}\n"
        
        result += f"  currentRound {self.currentRound}\n"
        
        result += f"  currentMatchup {self.currentMatchup}\n"
        
        result += f"  self.votingStarted {self.votingStarted}\n\n"
        
        for i in range(0, len(self.rounds)):
        
            result += "Round {}\n".format(i + 1)
            
            for j in range(0, len(self.rounds[i])):
                
                voteList = ""
                
                for vote in self.rounds[i][j].votes:
                    
                    if len(voteList) > 0 :
                    
                        voteList += ", "
                        
                    voteList += vote
                    
                result += f"Item {j}: \"{self.rounds[i][j]}\" votes: {voteList}\n"
        
            result += "\n"
        
        return result

    def addEntries(self, bracketEntryNames):
        
        bracketEntryNames = list(bracketEntryNames)

        for bracketEntryName in bracketEntryNames:
        
            if len(bracketEntryName) > 0 and not bracketEntryName in self._entries:
            
                self._entries.append(bracketEntryName)
    
        self.save()
        
    def currentMatchupString(self):
        
        if len(self.winner) == 0:
        
            entryOne = self.rounds[self.currentRound][self.currentMatchup]
	        
            entryTwo = self.rounds[self.currentRound][self.currentMatchup + 1]
        
            return f"Current matchup is \"{entryOne.entryName}\" vs \"{entryTwo.entryName}\""
            
        else:
         
            return f"{self.winner} is the winner!"
            

    def currentVotes(self):
        
        entryOne = self.rounds[self.currentRound][self.currentMatchup]
	        
        entryTwo = self.rounds[self.currentRound][self.currentMatchup + 1]
        
        entryOneVoterList = ""
        
        count = 0
        
        for voter in entryOne.votes:
        
            if count > 0:
            
                if count == len(entryOne.votes) - 1:
                
                    entryOneVoterList += ", and "
                
                else:
                
                    entryOneVoterList += ", "
            
            entryOneVoterList += voter
            
            count += 1
            
        if entryOneVoterList == "":
        
            entryOneVoterList = "Nobody"
         
        count = 0
        
        entryTwoVoterList = ""
        
        for voter in entryTwo.votes:
         
            if count > 0:
             
                if count == len(entryTwo.votes) - 1:
                 
                    entryTwoVoterList += ", and "
                 
                else:
                 
                    entryTwoVoterList += ", "
             
            entryTwoVoterList += voter
            
            count += 1
           
        if entryTwoVoterList == "":
        
            entryTwoVoterList = "Nobody"
            
        return f"{entryOneVoterList} voted for \"{entryOne.entryName}\". {entryTwoVoterList} voted for \"{entryTwo.entryName}\""
        
    def finalizeMatchup(self):
        
        matchupResult = ""
        
        entryOne = self.rounds[self.currentRound][self.currentMatchup]
		        
        entryTwo = self.rounds[self.currentRound][self.currentMatchup + 1]
        
        if len(entryOne.votes) > len(entryTwo.votes):
            
            matchupResult = f"{entryOne.entryName} has defeated {entryTwo.entryName} {len(entryOne.votes)} to {len(entryTwo.votes)}"
            
            # Move the winner into the next round, if one exists.
            if self.currentRound + 1 < len(self.rounds):
            
                slotIndexForNextRound = math.floor(self.currentMatchup / 2)
            
                self.rounds[self.currentRound + 1][slotIndexForNextRound].entryName = entryOne.entryName
            
            self.currentMatchup += 2
            
            if self.currentMatchup >= len(self.rounds[self.currentRound]):
            
                self.currentRound += 1
            
                self.currentMatchup = 0

            if  self.currentRound >= len(self.rounds):
            
                # A winner can be decided.
                self.winner = entryOne.entryName
                
            self.save()
             
        elif len(entryOne.votes) < len(entryTwo.votes):
        
            matchupResult = f"{entryTwo.entryName} has defeated {entryOne.entryName} {len(entryTwo.votes)} to {len(entryOne.votes)}"
             
            # Move the winner into the next round, if one exists.
            if self.currentRound + 1 < len(self.rounds):
            
                slotIndexForNextRound = math.floor(self.currentMatchup / 2)
            
                self.rounds[self.currentRound + 1][slotIndexForNextRound].entryName = entryTwo.entryName
            
            self.currentMatchup += 2
            
            if self.currentMatchup >= len(self.rounds[self.currentRound]):
            
                self.currentRound += 1
            
                self.currentMatchup = 0
                
            if  self.currentRound >= len(self.rounds):
            
                # A winner can be decided.
                self.winner = entryTwo.entryName
                            
            self.save()
            
        else:
        
            matchupResult = f"{entryOne.entryName} and {entryTwo.entryName} are currently tied. Can't move to the next matchup until there is a winner."
            
        return matchupResult
        
        
    # The number of bracket slots needs to be a power of 2.
    def findNextPowerOf2(self, n):

        # decrement `n` (to handle the case when `n` itself is a power of 2)
        n = n - 1

        # do till only one bit is left
        while (n & n - 1):

            # unset rightmost bit
            n = n & n - 1
	 
	    # `n` is now a power of two (less than `n`)
	 
        # return next power of 2
        return n << 1
    
    def getJson(self):
    
        jsonObject = "{\n"

        jsonObject += "\"bracketname\" : \"" + str(self.bracketName) + "\",\n"

        jsonObject += "\"currentround\" : " + str(self.currentRound) + ",\n"
        
        jsonObject += "\"currentmatchup\" : " + str(self.currentMatchup) + ",\n"

        jsonObject += "\"pinneddiscordmessageid\" : " + str(self.pinnedDiscordMessageId) + ",\n"

        jsonObject += "\"maxvotes\" : " + str(self.maxVotes) + ",\n"
        

        if self.votingStarted == True:
        
            jsonObject += "\"votingstarted\" : true,\n"
        
        else:
        
            jsonObject += "\"votingstarted\" : false,\n"
        

        if self.shuffle == True:
        
            jsonObject += "\"shuffle\" : true,\n"
        
        else:
        
            jsonObject += "\"shuffle\" : false,\n"
        
        jsonObject += "\"winner\" : \"" + str(self.winner) + "\",\n"
        
        # Build entries list
        entriesJson = ""
        
        for entry in self._entries:

            if len(entriesJson) > 0:
                
                entriesJson += ",\n"    
            
            entriesJson += "\"" + entry + "\""
        
        jsonObject += f"\"entries\" : [{entriesJson}],\n"
        
        # Build rounds lists.
        jsonObject += "\"rounds\" : ["

        roundsJson = ""
        
        for round in self.rounds:
            
            # Build the JSON for the bracket items for this round.                       
            bracketEntriesJson = ""
            
            for bracketEntry in round:
            
                if len(bracketEntriesJson) > 0:
                
                    bracketEntriesJson += ",\n"

                bracketEntriesJson += bracketEntry.getJson()    

            # Append the bracket items into the round
            if len(roundsJson) > 0:
                
                roundsJson += ",\n"
                    
            roundsJson += "[" + bracketEntriesJson + "]"
                        
        jsonObject += roundsJson + "]"

        jsonObject += "\n}"

        return jsonObject        
    
    def isValidVote(self, entryName):
                
        entryOne = self.rounds[self.currentRound][self.currentMatchup].entryName.lower()
    	        
        entryTwo = self.rounds[self.currentRound][self.currentMatchup + 1].entryName.lower()
        
        entryName = entryName.lower()
        
        #print(f"Checking for valid vote between {entryOne} and {entryTwo}")
        
        return (entryName.lower() == entryOne) or (entryName == entryTwo)
    
    def load(self):
    
        filePath = f'brackets\\{self.bracketName}.json'
        
        fileExists = os.path.isfile(filePath)
    
        if fileExists == True:
        
            try:

                with open(filePath) as jsonData:

                    jsonDict = json.load(jsonData)

                    self.populateFromJsonDict(jsonDict)

            except:

                e = sys.exc_info()[0]

                print("Error loading save file: {}".format(e))
                
                return False
        
        else:
        
            return False
            
        return True

    def populateFromJsonDict(self, jsonDict):
        
        self.currentRound = int(jsonDict["currentround"])
        
        self.currentMatchup = int(jsonDict["currentmatchup"])
        
        self.pinnedDiscordMessageId = int(jsonDict["pinneddiscordmessageid"])

        self.votingStarted = jsonDict["votingstarted"]

        self.shuffle = jsonDict["shuffle"]
        
        self.winner = jsonDict["winner"]
        
        self.maxVotes = int(jsonDict["maxvotes"])
        
        # Read the entries.
        self._entries = []
        
        for entry in jsonDict["entries"]:
            
            self._entries.append(entry)

        # Read the rounds.
        self.rounds = []
        
        for round in jsonDict["rounds"]:
            
            newRound = []
            
            for bracketEntry in round:
                
                newBracketEntry = BracketEntry(bracketEntry["entryname"])
                
                newBracketEntry.populateFromJsonDict(bracketEntry)
                
                newRound.append(newBracketEntry)
                        
            self.rounds.append(newRound)
            
    def save(self):
        
        json = self.getJson()
        
        if not os.path.exists("brackets"):

            os.makedirs("brackets")
            
        f = open(f'brackets\\{self.bracketName}.json', 'w+')

        f.write(json)

        f.close()        
    
    def startVoting(self):

        if self.votingStarted == False:
        
            self.votingStarted = True
  
            # Randomize entries
            if self.shuffle == True:
	        
                random.shuffle(self._entries)

            # Initialize the slots for the rounds. 
            # Start with round one and divided by two for each successive round until.
            if len(self._entries) > 0:
        
                slotsForRoundOne = self.findNextPowerOf2(len(self._entries))
            
                # Fill in any empty values.
                count = 0
            
                for i in range(0, slotsForRoundOne - len(self._entries)):
            
                    bracketEntryName = f"None_{count}"
                
                    # If this name already exists in the list, try the next one until a valid value is found.
                    while bracketEntryName in self._entries:

                        count += 1
                    
                        bracketEntryName = f"None_{count}"
                                
                    self._entries.append(bracketEntryName.replace('|', ' '))
                    
                    count += 1

            else:
        
                slotsForRoundOne = 0

            slotsForRound = slotsForRoundOne
            
            while slotsForRound > 1:

                bracketEntriesForRound = []
            
                for i in range(0, slotsForRound):
            
                    # Add an empty bracket entry to be filled in later.
                    bracketEntriesForRound.append(BracketEntry(""))

                self.rounds.append(bracketEntriesForRound)
            
                # Divide by two to get the number of slots for the next round.
                slotsForRound = (int)(slotsForRound/2)
        

            # Assign the bracket entries to slots for the first round.      
            for i in range(0, slotsForRoundOne):

                self.rounds[0][i].entryName = self._entries[i]

            # Save the rounds to disk.
            self.save()
    
    # Cast a vote for an entry in the current matchup.
    def registerVote(self, userId, entryName):
        
        voteChanged = False
        
        entryOne = self.rounds[self.currentRound][self.currentMatchup]
        
        entryTwo = self.rounds[self.currentRound][self.currentMatchup + 1]
        
        if entryOne.entryName.lower() == entryName.lower():
        
            # Check for changed vote.
            if userId in entryTwo.votes:
                
                entryTwo.votes.remove(userId)
                
                voteChanged = True
                
            entryOne.votes.add(userId)
        
        elif entryTwo.entryName.lower() == entryName.lower():
        
            # Check for changed vote.
            if userId in entryOne.votes:
                
                entryOne.votes.remove(userId)
                
                voteChanged = True
                
            entryTwo.votes.add(userId)
        
        self.save()
        
        return voteChanged
        
class BracketEntry:

    def __init__(self, bracketEntryName):
    
        self.entryName = bracketEntryName
        
        self.votes = set()
    
    def __str__(self):
    
        return "{}".format(self.entryName)
        
    def getJson(self):
        
        jsonObject = "{\n"

        jsonObject += "\"entryname\" : \"" + str(self.entryName) + "\",\n"
    
        jsonObject += "\"votes\" : ["
        
        votesJson = ""
        
        for vote in self.votes:
        
            if len(votesJson) > 0:
	                
                votesJson += ",\n"
        
            votesJson += f"\"{vote}\""
        
        jsonObject += votesJson + "]}"
        
        return jsonObject
        
    def populateFromJsonDict(self, jsonDict):
        
        for vote in jsonDict["votes"]:

            self.votes.add(vote)
        
        return
