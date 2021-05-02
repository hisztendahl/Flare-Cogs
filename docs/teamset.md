<!-- ## Teamset -->
##### Set a team's role. _(Admin command)_

    !teamset role <team, role>

?><span style="color:white">team</span>: <span style="color:lightgreen">string</span><br>
<span style="color:white">role</span>: <span style="color:lightgrey">discord.Role</span>

<br>

##### Set a team's stadium. _(Admin command)_

    !teamset stadium <team, stadium>

?><span style="color:white">team</span>: <span style="color:lightgreen">string</span><br>
<span style="color:white">stadium</span>: <span style="color:lightgreen">string</span>

<br>

##### Set a team's logo. _(Admin command)_

    !teamset logo <team, logo>

?><span style="color:white">team</span>: <span style="color:lightgreen">string</span><br>
<span style="color:white">logo</span>: <span style="color:lightgreen">string</span>

!>Url needs to be a .png file.

<br>

##### Set a team's name. _(Admin command)_
_Try keep names to one word if possible._

    !teamset name <teamname, newname>

?><span style="color:white">teamname</span>: <span style="color:lightgreen">string</span><br>
<span style="color:white">newname</span>: <span style="color:lightgreen">string</span>

<br>

##### Set a team's full name. _(Admin command)_

    !teamset fullname <team, fullname>

?><span style="color:white">team</span>: <span style="color:lightgreen">string</span><br>
<span style="color:white">fullname</span>: <span style="color:lightgreen">string</span>

<br>

##### Set a team's captain. _(Admin command)_

    !teamset captain <team, user>

?><span style="color:white">team</span>: <span style="color:lightgreen">string</span><br>
<span style="color:white">user</span>: <span style="color:lightgrey">@discord.Member</span>

<br><br>

#### Kits
##### Set a team's home kit. _(Admin command)_

    !teamset kits home <team, url>

?><span style="color:white">team</span>: <span style="color:lightgreen">string</span><br>
<span style="color:white">url</span>: <span style="color:lightgreen">string</span>

!>Url needs to be a .png file.

<br>

##### Set a team's away kit. _(Admin command)_

    !teamset kits away <team, url>

?><span style="color:white">team</span>: <span style="color:lightgreen">string</span><br>
<span style="color:white">url</span>: <span style="color:lightgreen">string</span>

!>Url needs to be a .png file.

<br>

##### Set a team's third kit. _(Admin command)_
!> This is currently not in use.

    !teamset kits third <team, url>

?><span style="color:white">team</span>: <span style="color:lightgreen">string</span><br>
<span style="color:white">url</span>: <span style="color:lightgreen">string</span>

!>Url needs to be a .png file.

<br>

##### Set a team's bonus. _(Admin command)_

    !teamset bonus <team, value>

?><span style="color:white">team</span>: <span style="color:lightgreen">string</span><br>
<span style="color:white">value</span>: <span style="color:lightblue">int</span>

<br>

##### Delete a team. _(Admin command)_

    !teamset delete <team>

?><span style="color:white">team</span>: <span style="color:lightgreen">string</span>