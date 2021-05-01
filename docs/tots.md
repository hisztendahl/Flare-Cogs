# TOTS

### Settings
##### Set kit _(Admin command)_

    !tots kit <url>

?><span style="color:white">url</span>: <span style="color:lightgreen">string</span>

!>Url needs to be a .png file.

<br>

##### Set logo _(Admin command)_

    !tots logo <url>

?><span style="color:white">url</span>: <span style="color:lightgreen">string</span>

!>Url needs to be a .png file.

<br>

##### Generate rankings _(Admin command)_

Ranks alls players according to their season performance. This ranking is what determines who gets POTS/TOTS.

    !tots getranking

**Points attribution:**
- *League*
    - Note: 10pts
    - Goal: 5pts
    - Assist: 3pts
    - Yellow card: -1pt
    - Red card: -3pts
    - MOTM: 5pts

- *Cup*
    - Goal: 2.5pts
    - Assist: 1.5pts
    - Yellow card: -0.5pt
    - Red card: -1.5pts
    - MOTM: 2.5pts

<br>

##### View TOTS

    !tots view


##### View POTS Ranking

    !tots ranking <page>

?><span style="color:white">page</span>: <span style="color:lightblue">int</span>

<br>
<br>


### Infographics
##### Champions _(Admin command)_
Generate Trophy winner image

    !tots champion <trophy, season>

?><span style="color:white">trophy</span>: <span style="color:pink">enum</span> (league | cup)<br>
<span style="color:white">season</span>: <span style="color:lightblue">int</span>

<br>

##### Walkout _(Admin command)_
Team of the season walkout.

    !tots walkout

!>Warning: This is tailored for 4 teams members, so you could have visual issues if team size is different.

<br>

##### Team Stats _(Admin command)_
Team stats recap for the season.
Shows top 3 best performing teams for wins, goals scored, shots, conversion rate, goals conceded, fairplay (least cards) and fouls.

    !tots teamstats

<br>


##### Individual Stats _(Admin command)_
Player stats recap for the season.
Shows top 3 best performing players for notes, goals scored, assists, goal contributions, MOTMs, fairplay (least cards).

    !tots playerstats

<br>

##### Player of the season _(Admin command)_
Shows POTS with their stats recap.

    !tots pots

<br>