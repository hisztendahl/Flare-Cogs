# Stats

## Player Stats
##### Add statistics for a user. _(Admin command)_
_Add goals, own goals, assists, goal contributions, yellow/red cards, motms, penalties for a user. This is only for league stats._

    !addstats <user, stat, value>

?><span style="color:white">user</span>: <span style="color:lightgrey">discord.Member</span><br>
<span style="color:white">stat</span>: <span style="color:pink">enum</span> _(goals | owngoals | assists | ga | yellows | reds | motm | penscored | penmissed)_<br>
<span style="color:white">value</span>: <span style="color:lightblue">int</span>

<br>

##### Clear statistics for a user. _(Admin command)_
Removes goals, own goals, assists, yellow/red cards, motms, penalties for a user. This is only for league stats.

    !clearstats <user>

?><span style="color:white">user</span>: <span style="color:lightgrey">discord.Member</span>

<br>

##### View league statistics

    !leaguestats <user>

?><span style="color:white">user _(opt.)_</span>: <span style="color:lightgrey">discord.Member</span>

!> If invoked without a user, it will display a summary with top performers for each category. Otherwise, it will display a summary for the invoked user.

<br>

##### Players with the best average note.

    !leaguestats notes <page>

?><span style="color:white">page _(opt.)_</span>: <span style="color:lightblue">int</span>

<br>

##### Players with the most combined goals and assists.

    !leaguestats ga <page>

?><span style="color:white">page _(opt.)_</span>: <span style="color:lightblue">int</span>

<br>

##### Players with the most goals.

    !leaguestats goals <page>

?><span style="color:white">page _(opt.)_</span>: <span style="color:lightblue">int</span>

<br>

##### Players with the most assists.

    !leaguestats assists <page>

?><span style="color:white">page _(opt.)_</span>: <span style="color:lightblue">int</span>

<br>

##### Players with the most own goals.

    !leaguestats owngoals <page>

?><span style="color:white">page _(opt.)_</span>: <span style="color:lightblue">int</span>

<br>

##### Players with the most yellow cards.

    !leaguestats yellows <page>

?><span style="color:white">page _(opt.)_</span>: <span style="color:lightblue">int</span>

<br>

##### Players with the most red cards.

    !leaguestats reds <page>

?><span style="color:white">page _(opt.)_</span>: <span style="color:lightblue">int</span>

<br>

##### Players with the most MOTMs.

    !leaguestats motm <page>

?><span style="color:white">page _(opt.)_</span>: <span style="color:lightblue">int</span>

<br>

##### Teams with the most cleansheets.

    !leaguestats cleansheets <page>

?><span style="color:white">page _(opt.)_</span>: <span style="color:lightblue">int</span>

<br>

##### Penalties scored and missed statistics.

    !leaguestats penalties <page>

?><span style="color:white">page _(opt.)_</span>: <span style="color:lightblue">int</span>

<br>
<br>

## Team Stats
##### Add statistics for a team. _(Admin command)_

    !addteamstats <team, stat, value>

?><span style="color:white">team</span>: <span style="color:lightgreen">string</span><br>
<span style="color:white">stat</span>: <span style="color:pink">enum</span> (played, wins, losses, points, gd, gf, ga, draws, reds, yellows, fouls, chances)<br>
<span style="color:white">value</span>: <span style="color:lightblue">int</span>

<br>

##### View statistics for a team.

    !teamstats <team, comptype = league>

?><span style="color:white">team</span>: <span style="color:lightgreen">string</span><br>
<span style="color:white">comptype _(opt.)_</span>: <span style="color:pink">enum</span> (league | cup | all)<br>

<br>

## Notes
##### View notes.

    !viewnotes <user>

?><span style="color:white">user</span>: <span style="color:lightgrey">discord.Member</span>

<br>

##### Add note(s) for a user. _(Admin command)_

    !addnotes <user, *notes>

?><span style="color:white">user</span>: <span style="color:lightgrey">discord.Member</span><br>
<span style="color:white">notes</span>: <span style="color:lightgreen">string | string[]</span>

!> Note: You can add multiple values at once.<br>
Example: _!addnotes @Bot Suricate 10 8.5 7 4.25_

<br>

##### Remove note for a user. _(Admin command)_
Remove a note at a given index for a user.

    !removenote <user, index>

?><span style="color:white">user</span>: <span style="color:lightgrey">discord.Member</span><br>
<span style="color:white">index</span>: <span style="color:lightblue">int</span>

!>Example: _!removenote @Bot Suricate 4_ will remove Suricate's 5th note (index starts at 0)

<br>

##### Remove all notes for a user. _(Admin command)_

    !clearnotes <user>

?><span style="color:white">user</span>: <span style="color:lightgrey">discord.Member</span><br>

<br>