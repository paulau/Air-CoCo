<?php

error_reporting(E_ALL);

include('header.html');


echo "
<center>
<b>Air-CoCo :)</b>
</center>
<br>

Steuerung und Monitoring Systeme für Gebäudeabkühlung durch Nachtsluftung! 
<br>
<br>
<br>
";

echo "
<table id='statetable' align=center border='1px solid black' cellPadding=0 cellSpacing=0 width=100%>
<tr bgcolor='#00EE00'>  <th>Datum, Uhrzeit</th> <th>Tin</th> <th>Tout</th> <th>Wind-Regen</th> <th>Luftung</th> </tr> 
<tr><td id='datetime'></td><td id='tin'></td><td  id='tout'></td><td id='WindRainState'></td><td id='FanState'></td></tr></table>";

//"WindowOpenMotorState":1,
//"WindowCloseMotorState":1


echo "<br>";

echo "<P id='title'>  </P>";
echo "<br>";

//echo "<A onclick='refresh()'>Testlink</A> &nbsp";


include("footer.html");

?>
