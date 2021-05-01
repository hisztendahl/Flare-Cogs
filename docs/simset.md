### General

##### Show current simulation settings. _(Admin command)_
_Displays game time, number of players per team, length of half time break, red card bonus modifier, results channel, transfer window status, bet settings, and teams mentions on game start._

    !simset

<br>

##### Update cache. _(Admin command)_
_Update cached level for every team. This command runs automatically with the !sim command._

    !simset updatecache

<br>

##### Mentions. _(Admin command)_
_Toggle mentions oon game start._

    !simset mentions <toggle>

?><span style="color:white">toggle</span>: <span style="color:red">boolean</span> _(true | false)_

<br>

##### Create roles. _(Admin command)_
_Creates a <span style="color:darkblue">@Sim captain</span> role, assigns it to team captains. Also assign team roles to team members._

    !simset createroles

<br>

##### Update roles for team members. _(Admin command)_

    !simset updateroles

<br>

##### Generate league fixtures. _(Admin command)_

    !simset createfixtures

<br>

##### Generate cup fixtures. _(Admin command)_
_If the number of team is not fitting a round size, byes will be given to teams automatically based on the current league standings. You can also provide a list of teams to give a bye to._

    !simset drawcupround <*teambyes>


?><span style="color:white">teambyes</span>: <span style="color:lightgreen">string[]</span>

<br>

##### [**DEPRECATED**] Add standings stat. _(Admin command)_
!>This should only be used if SimLeague is upgraded from an earlier version which didn't include current metrics such as fouls, or chances.

    !simset addstat <param>


?><span style="color:white">param</span>: <span style="color:pink">enum</span> _(played, wins, losses, points, gd, gf, ga, draws, reds, yellows, fouls, chances)_


<br><br>

### Bets
##### Enable / Disable betting. _(Admin command)_

    !simset bet toggle <value>

?><span style="color:white">value</span>: <span style="color:red">boolean</span> _(true | false)_

<br>

##### Bet time. _(Admin command)_
_Set the time allowed for betting - 600 seconds is the max, 180 is default._

    !simset bet <time>

?><span style="color:white">time</span>: <span style="color:lightblue">int</span>

<br>

##### Bet amount. _(Admin command)_
_Set the minimum / maximum amount for betting._

    !simset bet min <amount>
    !simset bet max <amount>

?><span style="color:white">min</span>: <span style="color:lightblue">int</span><br>
<span style="color:white">max</span>: <span style="color:lightblue">int</span>

<br>

##### Reset bets. _(Admin command)_
_Reset current betting status, and refund members that have a pending bet._

    !simset bet reset

<br><br>

### Game
##### Set the max team players. _(Admin command)_
_Value needs to be between 3 and 7._

    !simset maxplayers <value>

?><span style="color:white">value</span>: <span style="color:lightblue">int</span>

<br>

##### Set the the handicap per red card. _(Admin command)_
_Value needs to be between 1 and 30._

    !simset redcardmodifier <value>

?><span style="color:white">value</span>: <span style="color:lightblue">int</span>

<br>

##### Set game duration. _(Admin command)_
_Set the time each minute takes, in seconds. Value needs to be between 1 and 5._

    !simset gametime <value>

?><span style="color:white">value</span>: <span style="color:salmon">float</span>

<br>

##### Set the time break duration. _(Admin command)_
_Set the time each minute takes, in seconds. Value needs to be between 0 and 20._

    !simset halftimebreak <value>

?><span style="color:white">value</span>: <span style="color:salmon">float</span>


<br><br>

### Probabilities
!> Careful when changing probabilities, this has the potential to break the simulation.
<!-- * [Visit the probability helper for more detail.](probability_calculator.md) -->


##### View probabilities. _(Admin command)_

    !simset probability

<br>
##### Goal probability. _(Admin command)_
_Value needs to be between 1 and 100. Default = 96._

    !simset probability goals <value>

?><span style="color:white">value</span>: <span style="color:lightblue">int</span>

<br>

##### Own goal probability. _(Admin command)_
_Value needs to be between 1 and 400. Default = 399._

    !simset probability owngoals <value>

?><span style="color:white">value</span>: <span style="color:lightblue">int</span>

<br>

##### Yellow card probability. _(Admin command)_
_Value needs to be between 1 and 100. Default = 98._

    !simset probability yellow <value>

?><span style="color:white">value</span>: <span style="color:lightblue">int</span>

<br>

##### Red card probability. _(Admin command)_
_Value needs to be between 1 and 400. Default = 398._

    !simset probability red <value>

?><span style="color:white">value</span>: <span style="color:lightblue">int</span>

<br>

##### Penalty probability. _(Admin command)_
_Value needs to be between 1 and 250. Default = 249._

    !simset probability penalty <value>

?><span style="color:white">value</span>: <span style="color:lightblue">int</span>

<br>

##### Penalty block probability. _(Admin command)_
_Value needs to be between 1 and 100. Default = 75._

    !simset probability penaltyblock <value>

?><span style="color:white">value</span>: <span style="color:lightblue">int</span>

<br>

##### Corner probability. _(Admin command)_
_Value needs to be between 1 and 100. Default = 98._

    !simset probability corner <value>

?><span style="color:white">value</span>: <span style="color:lightblue">int</span>

<br>

##### Corner block probability. _(Admin command)_
_Value needs to be between 1 and 100. Default = 20._

    !simset probability corneryblock <value>

?><span style="color:white">value</span>: <span style="color:lightblue">int</span>

<br>

##### Freekick probability. _(Admin command)_
_Value needs to be between 1 and 100. Default = 98._

    !simset probability freekick <value>

?><span style="color:white">value</span>: <span style="color:lightblue">int</span>

<br>

##### Freekick block probability. _(Admin command)_
_Value needs to be between 1 and 100. Default = 15._

    !simset probability freekickblock <value>

?><span style="color:white">value</span>: <span style="color:lightblue">int</span>

<br>

##### VAR probability. _(Admin command)_
_Value needs to be between 1 and 100. Default = 50._

    !simset probability var <value>

?><span style="color:white">value</span>: <span style="color:lightblue">int</span>

<br>

##### VAR success probability. _(Admin command)_
_Value needs to be between 1 and 100. Default = 50._

    !simset probability varsuccess <value>

?><span style="color:white">value</span>: <span style="color:lightblue">int</span>

<br>

##### Commentary probability. _(Admin command)_
_Value needs to be between 1 and 100. Default = 85._

    !simset probability commentchance <value>

?><span style="color:white">value</span>: <span style="color:lightblue">int</span>

<br>


### Channels
##### Add a channel for automatic result posting. _(Admin command)_

    !simset resultchannel <channel>

?><span style="color:white">channel</span>: <span style="color:lightgrey">@discord.TextChannel</span>

!> Note: You can post results in multiple channels.

<br>

##### Show or clear all result channels. _(Admin command)_

    !simset resultchannels <option>

?><span style="color:white">option</span>: <span style="color:pink">enum</span> _(clear | show)_


##### Add a channel for automatic transfer posting. _(Admin command)_

    !simset transferchannel <channel>

?><span style="color:white">channel</span>: <span style="color:lightgrey">@discord.TextChannel</span>

!> Note: You can post results in multiple channels.

<br>

##### Show or clear all transfer channels. _(Admin command)_

    !simset transferchannels <option>

?><span style="color:white">option</span>: <span style="color:pink">enum</span> _(clear | show)_

<br><br>

### Transfers
##### Open or close the transfer window. _(Admin command)_

    !simset window <status>

?><span style="color:white">status</span>: <span style="color:pink">enum</span> _(open | close)_

<br>

##### Open or close the contract extension window. _(Admin command)_

    !simset lockwindow <status>

?><span style="color:white">status</span>: <span style="color:pink">enum</span> _(open | close)_

<br><br>

### Clear
##### Clear all teams, stats etc. _(Admin command)_

    !simset clear all

!>Warning: This will clear everything.

<br>

##### Clear stats. _(Admin command)_
_Clears standings, player stats, and team stats (league only)._

    !simset clear stats

<br>

##### Clear player notes. _(Admin command)_

    !simset clear notes

<br>

##### Clear cup stats. _(Admin command)_
_Clears standings, player stats, and team stats (cup only)._

    !simset clear cupstats

<br>

##### Clear cup results and stats. _(Admin command)_

    !simset clear cup

<br>

##### Clear transfers. _(Admin command)_
_Clears transfers from the current window._

    !simset clear transfers

<br>

##### Clear standings and player stats. _(Admin command)_
_Resets contract extensions. Using team param will only reset for that team._

    !simset clear lock <team>

?><span style="color:white">team</span>_(opt.)_: <span style="color:lightgreen">string</span>

<br>

##### Clear palmares. _(Admin command)_

    !simset clear palmares

!> Warning: This will remove palmares entries for all users.

<br>

##### Clear TOTS. _(Admin command)_
_Reset players, kit, and logo for TOTS._

    !simset clear tots

<br>

##### Clear team(s) form. _(Admin command)_
_Clear streak results for a team or all of them._

    !simset clearform <team>

?><span style="color:white">team</span>_(opt.)_: <span style="color:lightgreen">string</span>

<br>