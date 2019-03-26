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

include ("statetable.php");
echo "<br>";

echo "<P id='title'>  </P>";
echo "<br>";

echo "<P id='datetime'>  </P><br>";
echo "<P id='tin'>  </P><br>";
echo "<P id='tout'>  </P><br>";

echo "<A onclick='refresh()'>Testlink</A> &nbsp";
echo "<br>";


include("footer.html");

?>
