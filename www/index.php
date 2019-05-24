<?php

error_reporting(E_ALL);

include ("sqlsettings.php"); // import settings of sql database
require ("authclass.php"); // import authorisation class
include('header.html');

$a = new Authorisation($dbhost,$sqluser,$sqlpass,$sqldb);
$a->checkAccess(); // makes nothing if already done

// print content if authorised
if ($a->Authorised) {
	echo "
	<center>
	<b>Air-CoCo :)</b>
	</center>
	<br>
	
	Steuerung und Monitoring Systeme für Gebäudeabkühlung durch Nachtsluftung! 
	<br>
	<br>
	<br>
	
	<table id='statetable' align=center border='1px solid black' cellPadding=0 cellSpacing=0 width=100%>
	<tr bgcolor='#00EE00'>  <th>Datum, Uhrzeit</th> <th>Tin</th> <th>Tout</th> <th>Wind-Regen</th> <th>Luftung</th> </tr> 
	<tr><td id='datetime'></td><td id='tin'></td><td  id='tout'></td><td id='WindRainState' align='center'></td><td id='FanState' align='center'></td></tr></table>
	
	<br><br><br>
	
	Die volgende Knopfe sind noch nicht funktionstüchtig. 
	Die sind da als Vorschlag zu implementieren. <br>
	<form>
	<table>
		<tr><td>Fenster (Auf-Zu): </td> <td> <button type='button' id='Fenster'>Auf-Zu</button> </td> </tr>
		<tr><td>Regime (Auto-Manuell): </td> <td> <button type='button' id='AutoManuell' width=200px>Automatic-Manuell</button>   </td> </tr>
		<tr><td>Lufter: </td> <td> <button type='button' id='Luftung'>An-Aus</button>  </td> </tr>
	</table>
	</form>
	
	<center><img src='datapics/2019_03_09-2019_04_10.png'></center>
	<br>

	
	<!--'WindowOpenMotorState':1,'WindowCloseMotorState':1 
	<A onclick='refresh()'>Testlink</A> &nbsp -->
	<br>
	
	<P id='title'>  </P>
	<br>";
	}




include("footer.html");

?>
