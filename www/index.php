<?php

error_reporting(E_ALL);

include ("sqlsettings.php"); // import settings of sql database
require ("authclass.php"); // import authorisation class
include('header.html');
include ("daoventserver.php");

$a = new Authorisation($dbhost,$sqluser,$sqlpass,$sqldb);
$a->checkAccess(); // makes nothing if already done



// print content if authorised
if ($a->Authorised) {
	$s = new ventserver();
	$deviceName = $s->GetDeviceName();
	
	if ($deviceName == "MoniControlC")
		{
		require ("indexcontentC.html"); 
		}
		
	if ($deviceName == "MoniControlA")
		{
		require ("indexcontentA.html"); 
		}
	
	}
include("footer.html");

?>
