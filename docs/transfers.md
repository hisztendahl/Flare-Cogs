### List
_Show transfers for a team, or all teams._

    !transfer list <team>

?><span style="color:white">team</span> (opt.): <span style="color:lightgreen">string</span>

<br><br>

### Captains
##### Extend contract. _(@Sim Captain command)_
_Lock a player from your team to make him intransferable._

    !transfer lock <team, player>

?><span style="color:white">team</span>: <span style="color:lightgreen">string</span><br>
<span style="color:white">player</span>: <span style="color:lightgrey">discord.Member</span><br>

<br>

##### Transfer swap. _(@Sim Captain command)_
_Swap a player from your team with a player from another team._

    !transfer swap <team1, player1, team2, player2>

?><span style="color:white">team1</span>: <span style="color:lightgreen">string</span><br>
<span style="color:white">player1</span>: <span style="color:lightgrey">discord.Member</span><br>
<span style="color:white">team2</span>: <span style="color:lightgreen">string</span><br>
<span style="color:white">player2</span>: <span style="color:lightgrey">discord.Member</span>

<br>

##### Sign a free agent. _(@Sim Captain command)_
_Release a player from your team and sign a free agent._

    !transfer sign <team, player1, player2>

?><span style="color:white">team</span>: <span style="color:lightgreen">string</span><br>
<span style="color:white">player1</span>: <span style="color:lightgrey">discord.Member</span><br>
<span style="color:white">player2</span>: <span style="color:lightgrey">discord.Member</span>

<br>

##### Pass. _(@Sim Captain command)_
_End your turn without making any transfer._

    !transfer pass

<br>

##### Turn. _(@Sim Captain command)_
_Shows the team currently eligible to make transfers._

    !transfer turn

<br><br>

### Admin

##### Skip transfer turn. _(Admin command)_
_End transfer window for a given team._

    !admintransfer skip <team>
    
?><span style="color:white">team</span>: <span style="color:lightgreen">string</span>

<br>
    
##### Extend contracts. _(Admin command)_
_Lock **all players** from a team to make them intransferable._

    !admintransfer lock <team>

?><span style="color:white">team</span>: <span style="color:lightgreen">string</span>

<br>

##### Transfer swap. _(Admin command)_
_Swap a player from any team with a player from another team._

    !admintransfer swap <team1, player1, team2, player2>

?><span style="color:white">team1</span>: <span style="color:lightgreen">string</span><br>
<span style="color:white">player1</span>: <span style="color:lightgrey">discord.Member</span><br>
<span style="color:white">team2</span>: <span style="color:lightgreen">string</span><br>
<span style="color:white">player2</span>: <span style="color:lightgrey">discord.Member</span>

<br>

##### Transfer swap by id, _(Admin command)_
_Swap a player from any team with a player from another team. Same as above, but with user id._

    !admintransfer swapid <team1, player1id, team2, playerid2>

?><span style="color:white">team1</span>: <span style="color:lightgreen">string</span><br>
<span style="color:white">player1id</span>: <span style="color:lightgreen">string</span><br>
<span style="color:white">team2</span>: <span style="color:lightgreen">string</span><br>
<span style="color:white">player2id</span>: <span style="color:lightgreen">string</span>

<br>

##### Sign a free agent. _(Admin command)_
_Release a player from any team and sign a free agent._

    !admintransfer sign <team, player1, player2>

?><span style="color:white">team</span>: <span style="color:lightgreen">string</span><br>
<span style="color:white">player1</span>: <span style="color:lightgrey">discord.Member</span><br>
<span style="color:white">player2</span>: <span style="color:lightgrey">discord.Member</span>

<br>

##### Sign a free agent by id. _(Admin command)_
_Release a player from any team and sign a free agent. Same as above, but with user id._

    !admintransfer signid <team, player1id, player2id>

?><span style="color:white">team</span>: <span style="color:lightgreen">string</span><br>
<span style="color:white">player1id</span>: <span style="color:lightgreen">string</span><br>
<span style="color:white">player2id</span>: <span style="color:lightgreen">string</span>

<br>

##### Simple signing. _(Admin command)_
_Sign a free agent for a team, without releasing one of their players._

    !admintransfer simplesign <team, player1id, lock>

?><span style="color:white">team</span>: <span style="color:lightgreen">string</span><br>
<span style="color:white">player1id</span>: <span style="color:lightgreen">string</span><br>
<span style="color:white">lock</span> _(opt.)_:<span style="color:red">boolean</span>

!> _lock_ defaults to **False**. If set to **True**, the player will be intransferrable for the current window.

<br>

##### Releas a player. _(Admin command)_
_Release a player agent for any team._

    !admintransfer release <team, player1id>

?><span style="color:white">team</span>: <span style="color:lightgreen">string</span><br>
<span style="color:white">player1id</span>: <span style="color:lightgreen">string</span>

<br>

##### Reset player status. _(Admin command)_
_Remove player from transferred list._

    !admintransfer reset <player>

<span style="color:white">player</span>: <span style="color:lightgrey">discord.Member</span>

<br>
