# Palmares

##### Generate palmares for a season _(Admin command)_

    !genseasonpalmares <season>

><span style="color:white">url</span>: <span style="color:lightblue">int</span>

_Warning: Be careful of what season you are adding new palmares to._

<br>

##### Add palmares for a player _(Admin command)_
This is used to add individual entries for a player.

    !addpalmares <user, season, stat, value, rank>

><span style="color:white">user</span>: <span style="color:lightgrey">discord.Member</span><br>
><span style="color:white">season</span>: <span style="color:lightblue">int</span><br>
><span style="color:white">stat</span>: <span style="color:pink">enum</span> (goals, assists, ga, reds, yellows, motms, finish, cupfinish, communityshield)<br>
><span style="color:white">value</span>: <span style="color:lightblue">int</span><br>
><span style="color:white">rank</span>: <span style="color:lightblue">int</span>


_Example_

`!addpalmares @Bot Suricate 3 goals 20 2`

=> Bot Suricate was the 2nd top scorer with 20 goals in season 3.

_Note: For finish and cupfinish, the value needs to be the team name._

<br>


##### View palmares for a player

    !palmares <user>

><span style="color:white">user</span>: <span style="color:lightgrey">discord.Member</span><br>
