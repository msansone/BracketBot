Command arguments list:

BracketGeneratorTool.exe [Bracket Name] [RoundNumber] [MatchupNumberInRound] [Round 1 Bracket Entries (pipe delimted list)] ... [Round n Bracket Entries (pipe delimted list)] [winner]


1. Arguments must be encosed in quotes.


2. Numbering

   "Round number" is the column of the current matchup, it is used to highlight the entry currently being voted on.

   "Matchup number in round" is the row number of the current matchup, used with the round number to highlight the entry currently being voted on.

   Here is how the numering works: 

   The following is a bracket with 4 rounds. 

   The round numbers go from the outermost entries inward. 

   The matchup numbers go from top to bottom in the round, wrapping over to the top right side of the bracket, for the same round, when reaching the bottom of the left side.

   Round 0 Matchup 0                                                                                                                                                    Round 0 Matchup 4
                    \________                                                                                                                                  ________/
                    /        \                                                                                                                                /        \
   Round 0 Matchup 0          \                                                                                                                              /          Round 0 Mathcup 4
                               Round 1 Matchup 0                                                                                            Round 1 Matchup 2
                                                \___                                                                                   ____/                 
                                                /   \                                                                                 /    \
                               Round 1 Matchup 0     \                                                                               /      Round 1 Matchup 2
   Round 0 Matchup 1          /                       \                                                                             /                        \          Round 0 Matchup 5
                    \________/                         \                                                                           /                          \________/
                    /                                   \                                                                         /                                    \
   Round 0 Matchup 1                                     Round 2 Matchup 0                                       Round 2 Matchup 1                                      Round 0 Matchup 5
                                                                          \                                     /
                                                                           Round 3 Matchup 0 - Round 3 Matchup 0
                                                                          /                                     \
   Round 0 Matchup 2                                     Round 2 Matchup 0                                       Round 2 Matchup 1                                      Round 0 Matchup 6
                    \________                           /                                                                         \                            ________/
                    /        \                         /                                                                           \                          /        \
   Round 0 Matchup 2          \                       /                                                                             \                        /          Round 0 Matchup 7
                               Round 1 Matchup 1     /                                                                               \      Round 1 Matchup 3
                                                \___/                                                                                 \____/
                                                /                                                                                          \
                               Round 1 Matchup 1                                                                                            Round 1 Matchup 3
   Round 0 Matchup 3          /                                                                                                                              \         Round 0 Matchup 8
                    \________/                                                                                                                                \_______/
                    /                                                                                                                                                 \
   Round 0 Matchup 3                                                                                                                                                   Round 0 Matchup 8


3. Pipe delimited lists:

   The bracket entries pipe delimited list format is as follows:   

   [entry 1 name|entry 1 number of votes|entry 2 name|entry 2 votes|...|entry m name|entry m umber of votes]

4. Example to generates a bracket image for coolest animal:

   "Coolest Animal" 0 6 "dog|1|cow|2|hippo|1|giraffe|2|donkey|1|elephant|2|zebra|1|horse|2|penguin|1|panda|2|marmot|1|hamster|2|owl|1|rabbit|2|iguana|1|elk|2" "cow|1|hippo|2|donkey|1|zebra|2|penguin|1|marmot|2|owl|1|iguana|2" "hippo|1|zebra|2|marmot|1|owl|2" "zebra|1|marmot|2" " marmot"
