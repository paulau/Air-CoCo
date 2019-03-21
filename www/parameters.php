<?php	

include('header.html');
//include ("statetable.php");
include ("getparameterform.php");
include ("savetodatabase.php");
include ("sqlsettings.php"); // import settings of sql database

//mysqli_connect


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
SaveParametersToDatabase($sqluser,$sqlpass,$sqldb,$dbhost);
//GetParameterForm($sqluser,$sqlpass,$sqldb,$dbhost); // older verrsion 
PrintParameterForm();


include("footer.html");


?>
