# Sim Settings

##### Show current simulation settings. _(Admin command)_
Displays game time, number of players per team, length of half time break, red card bonus modifier, results channel, transfer window status, bet settings, and teams mentions on game start.

    !simset

<br>


#### Bet settings.
##### Enable / Disable betting. _(Admin command)_

    !simset bet toggle <value>

><span style="color:white">value</span>: <span style="color:red">boolean</span> (true | false)<br>

##### Bet time. _(Admin command)_
Set the time allowed for betting - 600 seconds is the max, 180 is default.

    !simset bet <time>

><span style="color:white">time</span>: <span style="color:lightblue">int</span><br>

##### Bet amount. _(Admin command)_
Set the minimum / maximum amount for betting

    !simset bet min <amount>
    !simset bet max <amount>

><span style="color:white">min</span>: <span style="color:lightblue">int</span><br>
><span style="color:white">max</span>: <span style="color:lightblue">int</span><br>


##### Reset bets. _(Admin command)_
Reset current betting status, and refund members that have a pending bet.

    !simset bet reset
