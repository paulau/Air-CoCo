<?php	

include('header.html');
include ("statetable.php");

echo "
<center>
<b>Visualisierung</b>
</center>
<br>
Temperatur und Luftungszustand in graphische Darstellung:
<br>
<br>
<br>
";

StateTable();

include("footer.html");


?>
