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
	
	<br> <a href='datapics/' target=_blank> Archiv, tägliche Darstellung. </a> <br><br>
	
	Visualisierung kann bis zu 10 Sekunden dauern. <br><br>
	
	Temperatur und Luftungszustand in graphische Darstellung:
	<br>
	<br>
	<center><img src='datapics/current.png' name='exposed' width=600>
	<br>
	Aktuelle Tag. Also  - heute
	</center>
	<br>
	";

	// *****************************************************************
	// the following code sends the command to the ventillationserver
	// to flush data to make them immediately available for visualisation
	// and to visualise them. Vent server makes it accordingly
	
	$service_port = 40012;
	$address = 'localhost';
	/* Einen TCP/IP-Socket erzeugen. */
	$socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
	if ($socket === false) {
		echo "socket_create() fehlgeschlagen: Grund: " . socket_strerror(socket_last_error()) . "\n";
		} 

	//echo "Versuche, zu '$address' auf Port '$service_port' zu verbinden ... <br>";
	$result = socket_connect($socket, $address, $service_port);
	$in = "Flush";
	//echo "HTTP HEAD request senden ...<br>";
	socket_write($socket, $in, strlen($in));
	socket_close($socket);
	
	

	// *****************************************************************
	// The code below prints the archiv of all visualisation files:
	
	$path    = './datapics';
	$files = scandir($path);
	$total = count($files); 
	$images = array(); 
	
	
	
	/*
	echo ("<table width=100%><tr><td>");
	for($x = 0; $x <= $total; $x++)
		{
		if (strpos($files[$x], 'png') !== false) {
			echo("<a onclick=ActivateImage('". $files[$x] . "')>  ". $files[$x] . "  </a> <br>");
			}
		}

	echo(" </td><td align='center' valign='center'> <b>Um die Daten von bestimmte Tag zu sehen, <br> klicken Sie auf entsprechende Tag </b> </td></tr></table>");
	*/
	
	}
	

include("footer.html");
?>
