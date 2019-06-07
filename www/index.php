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
		require ("indexcontentRHTCO2.html"); 
// TODO  rename ids ins index files eg statetableRHTCO2 and statetableclassA ...
// check in refresh() of common.js which id is defined and call according function
// document.getElementById('statetableRHTCO2')  - returns array of more than 0
// document.getElementById('statetableclassA')  - returns array of more than 0
// document.getElementById('statetableclassB')  - returns array of more than 0
		
		}
		
	if ($deviceName == "MoniControlA")
		{
		require ("indexcontent.html"); 
		}
	
	}
include("footer.html");

?>
