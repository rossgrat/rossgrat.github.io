{
   "date": "2024-06-03T19:52:20-04:00",
   "draft": false,
   "title": "Whist Tournaments for Euchre",
   "tags" : [
         "combinatorics",
         "angular",
         "golang"
      ]
}

My dad has a friend that holds an annual Euchre tournament each year on St. Patties day. It's a pretty big deal, anywhere from 20-30 people will show up to see who takes home a hefty cash prize. The format is unique and very similar to a round-robin style tournament, but with a twist. Each round the teams are randomly chose via each person pulling a piece of paper out of a hat. The system is simple, but there are some problems such as players playing each other multiple times or having the same partner multiple times, which is why I was approached to write a program to improve the process.

I was only given one constraint, and that was: make it such that each person has every other person as a partner exactly once. I am happy to say that I was able to produce a product to solve this problem. Below I am going to detail my journey of building this app as well as what I learned from my mistakes and successes.

## False Starts
### No. 1 - Backtracking
After having done some leetcode exercies on backtracking, specifically on how to generate combinations while backtracking, I thought that I knew the solution right away. I would generate all of the possible team combinations, then pair those team combinations together to create the tables for each round. 

I figured I could do this with any arbitrary number of players and just have 1-3 players sit out each round with a bye.

To begin I created several data structures:
* **Tourney**, which represents the tournament and holds all the rounds
* **Round**, which holds an array of Tables
* **Table**, which holds two Teams
* **Team**, which holds two Players

Really basic stuff. Using those data structures, I attempted to implement a backtracking solution that would recurse over each round, table, and team, and attempt to fill each until there were no more combinations. The idea was that if the program reached a point where it could no longer fill a table, it would backtrack and try new combinations until something fit. 

The initial solution looked something like this:

{{< highlight pseudocode >}}
generate all combinations for N players choose 
backtrack(combinations, used_players_for_round, used_combinations)
   if used_combinations equals combinations length
      all done
   for all unused combinations
      if the players in the combination are not in used_players for round 
         AND there is not one player on both teams
         add the team to a table
         add combination to used_combinations
         add players on the team to used_players_for_round
         backtrack(combinations, used_players_for_round, used_combinations)
         remove team from table
         remove combination from used_combinations
         remove players from used_players_for_round
{{< / highlight >}}

This did not work. 

My skill at deriving Big O complexities leaves much to be desired and I do not remember much about the master theorem besides its name (or if it is even applicable in this situation), but if I was going to take a stab at guessing, I would guess code is O(N^N) or worse. Basically this solution ran forever even at what I considered to be the very small inputs such as 16 players.

Back to the drawing board.

### No. 2 - Usage Matrix
At this point I really should have stepped back and done some research to see if there was any existing literature or algorithms on what appeared to be an increasingly unique problem. Doing so would have likely saved me hours of headache and wheel spinning. I did not do this, partially because for I went on vacation for a period where I sat on a beach for several days straight without any internet access, and partially because I thought it would be really cool to come up with a custom algorithm by myself. The result was sitting in the sun with a notepad and paper and trying to rough out a new algorithm, when I probably sould have been reading books on Combinatoric Desing.

The first thing I decided to do this time around was to decrease the scope of the problem. In the first false start I attempted to come up with a solution that would work for any amount of players on a team and any amount of teams in a table. I scrapped this and decided to fix the number of players per team at 2, and the number of teams per table also at 2. This would work fine for a Euchre tournament.

=== TODO === 
The next idea I tried was a usage matrix. I created an array of sets for each other players. Each player had a set representing who they had been partnered with.

The solution looked something like this:

{{< highlight pseudocode >}}

{{< / highlight >}}

The problem persists. What to do next?

## Stepping back and doing some research
=== TODO === 
After two false starts I realized that maybe this problem wasn't as simple as I thought. I did a few various deep dives and 

A dive down the math stack exchange rabbit hole lead me to my knio

### Whist Tournaments, Durango Bill and Richard A. Venezia


## Implementation
Having finally figured out how to generate the rounds, I started building the web app. 

This first thing I did was write a Go program to parse out all of the starting rounds on Durango Bill's website into JSON. The program continually loops and reads in an input.txt file which it expects to be in the starting round format defined by Durango Bill. It extracts the number of tables, then for each table the two teams, then for each team the two players. It stores all of that information in structs before marshaling the structs to JSON and concatenating them to the reset of the starting rounds. After running the parser I added the starting rounds for players 4 - 16 by hand from Richard A. Venezia's site.

=== TODO === 

The second thing I did was to build the app itself. I used Angular mostly because I am a huge fan of Golang and figured if Google could build a language that good, then maybe their web framework was equally as good. The Angular app has no routes and only two components, one to add all of the players and one to show the rounds for each player. It's really exactly like Richard A. Venezias tables but with the added feature of displaying the names you entered. 

Finallyh I deployed the finished product to github pages and texted my dad that his friend's new toy was ready to be played with.

You can check out the app yourself at: https://ross.grattafiori.dev/wtm

The source code is present at: https://github.com/rossgrat/wtm


## Closing Thoughts
### What I Learned
* Basic Angular fundamentals such as components and templates
* Do some research on your topic instead of diving right in (duh.)

### Future Actions
* Big O Notation, I need to get better at this and practice often, especially for difficult problems, so I know when to hold em' and when to fold em'

### What's Next?
The next project I think I am going to tackle is an idea for a laundry sharing web app that I had about a month ago. TLDR; my apartment has fixed laundry days, but sometimes I need to clean stuff on days that are not my laundry day. Solution: build an app where my neighbors can share their laundry time with each other.

These are some of the things I am hoping to learn and practice with this next project:
* Reverse Proxy via Caddy
* Websockets
* Progressive Web Apps
* Web Push Notifications
* Session Management in Angular
* Somne lightwight DB like SQLite or LevelDB

### References
* [Durango Bill's Starting Rounds](https://www.durangobill.com/BridgeCyclicSolutions.html)
* [Richard A. Venezia's Round Robin Page](https://www.devenezia.com/downloads/round-robin/rounds.php?it=12&v=w1)

