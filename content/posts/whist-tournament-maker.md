{
   "date": "2024-07-15T17:41:56-04:00",
   "draft": false,
   "title": "Whist Tournaments for Euchre",
   "tags" : [
         "technical",
         "algorithms",
         "frontend"
      ]
}

My dad has a friend that holds an annual Euchre tournament each year on St. Paddy's Day. It's a pretty big deal, anywhere from 20-30 people will show up to see who takes home a non-trivial cash prize. The format is unique and very similar to a round-robin style tournament, but with a twist. Each round the teams are randomly chosen via each person pulling a piece of paper out of a hat. The system is simple, but there are some problems such as players playing each other multiple times or having the same partner multiple times, which is why I was approached to write a program to improve the process.

I was only given one constraint, and that was: make it such that each person has every other person as a partner exactly once. I am happy to say that I was able to produce a product to solve this problem. Below I am going to detail my journey of building this app as well as what I learned from my mistakes and successes.

## False Starts
In the past I have extensively researched a project before starting. Unfortunately, this time around, an abundance of overconfidence led me to start an implementation for this project without doing so not once, but twice, before finally coming to my senses. This section encapsulates both of these failures for posterity as a reminder to my future self to measure twice and cut once.

### No. 1 - Backtracking
Upon starting this project I had recently done some backtracking exercises on Leetcode, and thought I had a solution right away. I would generate all of the possible team combinations via backtracking, then pair those team combinations together to create the tables for each round. 

I figured I could do this with any arbitrary number of players and just have 1-3 players sit out each round with a bye.

To begin I created several data structures:

* **Table**, which holds two Teams
* **Team**, which holds two Players
* **Round**, which holds an array of Tables
* **Tourney**, which represents the tournament and holds all of the Rounds

Using those data structures, I attempted to implement a backtracking solution that would recurse over each round, table, and team, and attempt to fill each until there were no more combinations. The idea was that if the program reached a point where it could no longer fill a table, it would backtrack and try new combinations until something fit. 

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
This time around I decided to decrease the scope of the problem. In the first false start I attempted to come up with a solution that would work for any amount of players on a team and any amount of teams in a table. I scrapped this and decided to fix the number of players per team and number of teams per table at 2, which are the values required for a game of Euchre.

The next idea I tried was a usage matrix. I created an array of sets for each other players. Each player had a set representing who they had been partnered with. I then iterated over an array of all the player IDs, sorted by the number of games they had played, and attempted to partner each player until the usage matrix was full.

The solution looked something like this:

{{< highlight pseudocode >}}
while we can partner players from the usage matrix
   sort player IDs by games played
   while all tables in a round not full
      for player in player IDs
         for partner in players IDs
            if player has not been partnered AND player has not been used 
            this round AND partner has not been used this round
               add team to table
               add partner to player used partners
               add player to partner used partners
{{< / highlight >}}

That's a lot of nested loops. 

This also did not work. The number of rounds should be equal to or greater than the number of players, because each player needs to partner with every other player exactly once. This algorithm stopped well short of the correct number of rounds, and it appeared to be caused by the usage matrix entering a state where it could no longer assign tables, even though combinations remained. An example being: If player 1 and player 2 is a remaining combination, along with player 1 and player 3, we can't make a table out of this because both combinations contain player 1.

I tried a few tweaks to fix this such as adjusting where the iterative loops started, but this method began to feel fruitless. After a while working on this approach I finally came to my senses and did what I should have done before writing the first line of code.

## Stepping back and doing some research

A deep dive into the interwebs led me to a mathematics stack exchange post where someone posited a question about this very same tournament format, albeit for a different game. One of the answers led by to my two new heroes, Richard A. Venezia and Durango Bill.

It turns out that this type of tournament design exists! And there is literature on it. In the blog of Richard A. Venezia, I found a short discussion where someone requested this style of a tournament for beach volleyball. Richard tried to come up with a solution on his own, which worked out semi-well, but also reached out to a friend, and this friend introduced Richard, the original question-asker, and now myself, to the tournament style that is called Whist.

Whist tournaments, which I believe are based on the old English card game of the same name, can be generated exactly like round robin tournaments! With a simple [cyclic round-robin algorithm](https://en.wikipedia.org/wiki/Round-robin_tournament#Scheduling_algorithm) of fixing the position of one person and incrementing the other positions each round with a modulo equal to the total number of players minus one. The special sauce that makes it a Whist style tournament is what Richard calls the 'starting blocks,' which is the position that each person starts in. It turns out that if you pick these starting blocks correctly, when you generate the tournament, you get N rounds for N people where each person pairs with each other person exactly once and players each other person exactly twice. The perfect solution to my problem!

Richard has an excellent page on his site where you can generate all rounds of the tournament for many different styles, for 0 to 100 players. Unfortunately, when I tried to get the Whist tournaments for more than 16 players, the PHP kept redirecting me to the regular round robin rounds, which was a problem. In the forum discussion, his friend only offered the first 16 starting blocks, which are present in [Combinatoric Design and Tournaments by Ian Anderson](https://books.google.com/books/about/Combinatorial_Designs_and_Tournaments.html?id=fra5mHKGk_kC).

Enter Durango Bill.

Durango Bill's website is linked directly from Richard A. Venezia's site and contains a wealth of information on combinatorics. The page that was most relevant to me was 'Durango Bill's Bridge Probabilities and Combinatorics.' Many years ago, Durango Bill did the thankless work of writing a computer program and sinking the CPU hours required into generating every possible 'starting block' permutation, and then parsing out the correct permutation(s) that would generate a Whist style tournament for N = 16 to 100. For context, once you hit 28 players, the number of starting blocks is around 23 trillion and, according to Durango Bill's blog, took two weeks to parse.

For my purposes, the algorithm that I had struggled to implement thus far was now a matter of extracting the starting blocks from the blog post, and writing a simple cyclic algorithm to generate the rounds.

Side Note: An interesting thing I have found in my years of web searching are that if you know the name of some very niche concept, it is very easy to find a wealth of information on it, but if you don't know the exact name, and just try to describe the concept to the search engine (or ChatGPT), the answers are mostly garbage. I wonder if there is a way to fix this?

## Implementation
With the hard part of figuring out the underlying tournament generation algorithm over, it was now time to actually build the app.

I decided to use Angular because I am a huge fan of Golang and wanted to try out Google's web framework. 

The Angular app has no routes and only two components besides the main *app* component. 

The first component is called the *players* component and its function is to allow the user to add the names of all participating players. This component displays a simple input box and a list of players, with the most recent player appearing at the top of the list. Players can be dismissed using the "x" next to their names. The color of the number indicating how many players have been added changes color depending on the validity of the value. The number of players must be divisible by 4. Each player is assigned a unique ID, with the first player added receiving the ID of 1, the second player added receiving an ID of 2, and so on. At the bottom there is a large "Start Tournament" button.

The second component is called the *tourney* component. When the "Start Tournament" button in the *players* component is pressed, this component will select the correct starting blocks based on the number of players. The component generates each round by taking the starting block and making a copy of it. Each player in the copy besides the player with the highest ID will then be incremented by 1 with a modulo of one less than the number of players (`(id + 1) % num_players`). The copy is then added to the list of rounds. Once there are as many rounds as there are players, the tournament has been generated. The component then displays each table for each round as four player names with a dividing symbol separating them to indicate teams. Selecting the "End Tournament" button at the bottom of the template will return the user to the *players* component.

The last thing I had to do was write a Go program to parse out all of the starting rounds on Durango Bill's website into JSON. The program continually loops and reads in an input.txt file which it expects to be in the starting round format defined by Durango Bill. It extracts the number of tables, then for each table the two teams, then for each team the two players. It stores all of that information in structs before marshaling the structs to JSON and concatenating them to the rest of the starting rounds. After running the parser I added the starting rounds for players 4 - 16 by hand from Richard A. Venezia's site.

Finally I deployed the finished product to github pages and texted my dad that his friend's new toy was ready to be played with. 

You can check out the app yourself at: https://ross.grattafiori.dev/wtm

The source code is present at: https://github.com/rossgrat/wtm

## Closing Thoughts
### What I Learned
* I learned some basic Angular fundamentals such as components, templates, and how these objects interact.
* I learned that Angular is probably best for larger projects, and might be overkill for my little app.
* I (re)learned that it is always best to do research and planning before starting an implementation
* I learned about the Whist style tournament and what is necessary to create one
* I learned that I need to review and practice Big O notation

Thanks for reading!

### What's Next?
The next project I think I am going to tackle is an idea for a laundry sharing web app that I had about a month ago. TLDR; my apartment has fixed laundry days, but sometimes I need to clean stuff on days that are not my laundry day. Solution: build an app where my neighbors can share their laundry time with each other.

These are some of the things I am hoping to learn and practice with this next project:
* Reverse Proxy via Caddy
* Websockets
* Progressive Web Apps
* Web Push Notifications
* Session Management in Angular
* Some lightweight DB like SQLite or LevelDB

### References
* [Durango Bill's Starting Rounds](https://www.durangobill.com/BridgeCyclicSolutions.html)
* [Richard A. Venezia's Round Robin Page](https://www.devenezia.com/downloads/round-robin/rounds.php?it=12&v=w1)

