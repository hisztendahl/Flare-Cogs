### Simulation

##### Show current simulation settings. _(Admin command)_
_Displays game time, number of players per team, length of half time break, red card bonus modifier, results channel, transfer window status, bet settings, and teams mentions on game start._

    !simset

<br>

### Bets
##### Enable / Disable betting. _(Admin command)_

    !simset bet toggle <value>

?><span style="color:white">value</span>: <span style="color:red">boolean</span> _(true | false)_<br>

##### Bet time. _(Admin command)_
_Set the time allowed for betting - 600 seconds is the max, 180 is default._

    !simset bet <time>

?><span style="color:white">time</span>: <span style="color:lightblue">int</span><br>

##### Bet amount. _(Admin command)_
_Set the minimum / maximum amount for betting._

    !simset bet min <amount>
    !simset bet max <amount>

?><span style="color:white">min</span>: <span style="color:lightblue">int</span><br>
<span style="color:white">max</span>: <span style="color:lightblue">int</span><br>


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