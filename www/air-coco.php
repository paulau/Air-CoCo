<?php

error_reporting(E_ALL);

include('header.html');
include ("dao.php");

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

StateTable();

include("footer.html");

?>
