<?php	

include('header.html');
include ("dao.php");
include ("sqlsettings.php"); // import settings of sql database


echo "
<center>
<b>Parameter</b>
</center>
<br>
Sie können hier die Steuerung-Monitoring Parameter einstellen:
<br>
<br>
";

//StateTable();

$p = new parameters($dbhost,$sqluser,$sqlpass,$sqldb);

$p->SaveParametersToDatabase();
$p->GetParameterForm();


include("footer.html");


?>
