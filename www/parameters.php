<?php	

include('header.html');
include ("daoparameters.php");
include ("sqlsettings.php"); // import settings of sql database
require ("authclass.php"); // import authorisation class



//StateTable();

$a = new Authorisation($dbhost,$sqluser,$sqlpass,$sqldb);
$a->checkAccess(); // makes nothing if already done

// print content if authorised
if ($a->Authorised) {
	echo "
	<center>
	<b>Parameter</b>
	</center>
	<br>
	Sie können hier die Steuerung-Monitoring Parameter einstellen:
	<br>
	<br>
	";
	
	$p = new Parameters($dbhost,$sqluser,$sqlpass,$sqldb);
	$p->SaveParametersToDatabase();
	$p->GetParameterForm();	
	}


include("footer.html");


?>
