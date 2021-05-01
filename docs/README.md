# Core

### General
#### Notify
##### Set wheter to receive notifications of matches and results.

    !notify <toggle>
    
?><span style="color:white">toggle</span>: <span style="color:red">boolean</span>

<br>

#### Register
##### Register a team. _(Try to keep team names to one word if possible)_

    !register <teamname, members, logo, *, role>


?><span style="color:white">teamname</span>: <span style="color:lightgreen">string</span><br>
<span style="color:white">members</span>: <span style="color:lightgrey">@discord.Member</span><br> 
<span style="color:white">logo</span>: <span style="color:lightgreen">string</span><br>
<span style="color:white">role</span>: <span style="color:lightgrey">@discord.Role</span>

<br>

## Teams
##### List current teams.

    !teams <updatecache, mobilefriendly>

?><span style="color:white">updatecache</span>?: <span style="color:red">boolean</span> (false)<br> 
<span style="color:white">mobilefriendly</span>?: <span style="color:red">boolean</span> (true)

<br>

##### List a team.

    !team <team>

?><span style="color:white">team</span>: <span style="color:lightgreen">string</span>

<br>

## Fixtures
##### Show all fixtures.
_Shows all fixtures, or first 25. Use page to see following fixtures._

    !fixtures <page>

?><span style="color:white">page</span>: <span style="color:lightblue">int</span> (1)

<br>

##### Show individual fixture.

    !fixture <week>

?><span style="color:white">week</span>: <span style="color:lightblue">int</span>



#### Standings
##### Current sim standings.

    !standings <verbose>

?><span style="color:white">verbose</span>: <span style="color:red">boolean</span> (false) -  Display goals for / against

#### Standings subcommands

##### Teams with the most goals / shots / fouls...

    !standings <stat>
    
    
?><span style="color:white">stat</span>: <span style="color:pink">enum</span> 

Possible values:

- <span style="color:pink">goals</span>: Teams with the most goals scored.
- <span style="color:pink">shots</span>: Teams with the most shots.
- <span style="color:pink">fouls</span>: Teams with the most fouls.
- <span style="color:pink">yellows</span>: Teams with the most yellow cards.
- <span style="color:pink">reds</span>: Teams with the most red cards.
- <span style="color:pink">defence</span>: Teams with the least goals conceded.
- <span style="color:pink">conversioon</span>: Teams with the best conversion rate.


## Simulation

##### Simulate a game between two teams.

    !sim <team1, team2>

?> <span style="color:white">team1</span>: <span style="color:lightgreen">string</span><br>
<span style="color:white">team2</span>: <span style="color:lightgreen">string</span>

Admin command, 1 max concurrency, 30 sec cooldown


##### Simulate a cup game between two teams.

    !simcup <team1, team2>

?> <span style="color:white">team1</span>: <span style="color:lightgreen">string</span><br>
<span style="color:white">team2</span>: <span style="color:lightgreen">string</span>


Admin command, 1 max concurrency, 30 sec cooldown.

No level, 50/50 game


##### Simulate a friendly game between two teams.

    !simfriendly <team1, team2>

?><span style="color:white">team1</span>: <span style="color:lightgreen">string</span><br>
<span style="color:white">team2</span>: <span style="color:lightgreen">string</span>


Admin command, 1 max concurrency, 30 sec cooldown.

No level, 50/50 game

<br>

## Bet
#### Bet on a team or a draw.

    !bet <amount, team>

?><span style="color:white">amount</span>: <span style="color:lightblue">int</span><br>
<span style="color:white">team</span>: <span style="color:lightgreen">string</span>