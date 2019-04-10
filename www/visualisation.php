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
	<center><img src='datapics/kk002_2019_03_20_00_00.png' width=600></center>
	<br>
	";
	}
	
include("footer.html");
?>
