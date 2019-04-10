<?php	
include ("sqlsettings.php"); // import settings of sql database
require ("authclass.php"); // import authorisation class
include('header.html');

$a = new Authorisation($dbhost,$sqluser,$sqlpass,$sqldb);
$a->checkAccess(); // makes nothing if already done

// print content if authorised
if ($a->Authorised) {

	echo "
	<center>
	<b>Visualisierung</b>
	</center>
	<br>
	Temperatur und Luftungszustand in graphische Darstellung:
	<br>
	<br>
	<center><img src='datapics/kk002_2019_03_20_00_00.png' name='exposed' width=600></center>
	<br>
	";

	$path    = './datapics';
	$files = scandir($path);
	$total = count($files); 
	$images = array(); 
	
	echo ("<table width=100%><tr><td>");
	
	
	for($x = 0; $x <= $total; $x++)
		{
		if (strpos($files[$x], 'png') !== false) {
			echo("<a onclick=ActivateImage('". $files[$x] . "')>  ". $files[$x] . "  </a> <br>");
			}
		}

	echo(" </td><td align='center' valign='center'> <b>Um die Daten von bestimmte Tag zu sehen, <br> klicken Sie auf entsprechende Tag </b> </td></tr></table>");
	}
	

include("footer.html");
?>
