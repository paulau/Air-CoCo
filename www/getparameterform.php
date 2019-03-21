<?php

function GetParameterForm($sqluser,$sqlpass,$sqldb,$dbhost)
	{
	// This function just read all parameters from Database and 
	// prints them as filled html form
	// The problem of this function is that the parameters are 
	// printed in some "strange" order. Not in the order, as they follow
	// in settingsMC.py file. 
	// To solve it, decision is to write a special function 
	// PrintParameterForm() which prints all necessary parameters explicitely
	// in correct order, devided on sections and optionally with some 
	// explanations of each parameter. 
	// it would be difficult to implement it via processing the settingsMC.py
	// and adjusting Database. 
	
	$db = mysqli_connect($dbhost, $sqluser, $sqlpass, $sqldb);
	 
	if(!$db)
	{
	exit("Verbindungsfehler: ".mysqli_connect_error());
	}
	$sql = "select * from AirCoCo.Parameters order by Id desc limit 50";
	$result = mysqli_query($db, $sql) or die(mysqli_error());

echo '
	<!-- enctype="multipart/form-data" -->
	<form 
		name= "formorder"
		action="parameters.php"
		method="post"
		onsubmit="return(validate());"
		>	
	<table>';

	// the following code would just take all parameters from database 
	// and put them as html form
	while($row = mysqli_fetch_array($result)) {
		$PName = $row['ParameterName'];
		$PValue = $row['ParameterValue'];
		//echo $PName . " ". $PValue . "<br>";
		
		echo '<tr bgcolor=#F8F8F8>
		<td valign="top" width="100">';
		echo $PName;
		echo '</td>
		<td>
		<input type="text" name="';
		echo  $PName .'" value="'.$PValue.'"  id= formfield>';
		echo '
		</td>
		</tr>';
		}
		


echo '
	</table>    
  
	<input type="submit" value="Set Parameter!" id= formbutton>
	</form>';


	mysqli_close($db);
	}




function PrintParameterForm()
	{
		
		MUST GET NOW VALUES FROMDB
		
echo '
	<!-- enctype="multipart/form-data" -->
	<form 
		name= "formorder"
		action="parameters.php"
		method="post"
		onsubmit="return(validate());"
		>	
	<table>
		<tr bgcolor=#BBBBBB><td>
		<b>Parameters of Sensors and relays:</b>
		</td><td></td></tr>

		<tr bgcolor=#F8F8F8>
		<td valign="top" width="100">sensor_inside_id</td>
		<td>
		<input type="text" name="sensor_inside_id" value="28-02099177d15c"  id= formfield>
		</td>
		</tr>

		<tr bgcolor=#F8F8F8>
		<td valign="top" width="100">sensor_outside_id</td>
		<td>
		<input type="text" name="sensor_outside_id" value="28-020d9177a279"  id= formfield>
		</td>
		</tr>

		<tr bgcolor=#F8F8F8>
		<td valign="top" width="100">pin1</td>
		<td>
		<input type="text" name="pin1" value="19"  id= formfield>
		</td>
		</tr>
		
		<tr bgcolor=#F8F8F8>
		<td valign="top" width="100">pin2</td>
		<td>
		<input type="text" name="pin2" value="26"  id= formfield>
		</td>
		</tr>

		<tr bgcolor=#F8F8F8>
		<td valign="top" width="100">RelayK1ControlPin</td>
		<td>
		<input type="text" name="RelayK1ControlPin" value="16"  id= formfield>
		</td>
		</tr>
		<tr bgcolor=#F8F8F8>
		<td valign="top" width="100">RelayK2ControlPin</td>
		<td>
		<input type="text" name="RelayK2ControlPin" value="20"  id= formfield>
		</td>
		</tr>
		<tr bgcolor=#F8F8F8>
		<td valign="top" width="100">RelayK3ControlPin</td>
		<td>
		<input type="text" name="RelayK3ControlPin" value="21"  id= formfield>
		</td>
		</tr>
		
		
		
		
		<tr bgcolor=#BBBBBB><td>
		<b>Parameters of control:</b>
		</td><td></td></tr>

		<tr bgcolor=#F8F8F8>
		<td valign="top" width="100">StartTime</td>
		<td>
		<input type="text" name="StartTime" value="0"  id= formfield>
		</td>
		</tr>

		<tr bgcolor=#F8F8F8>
		<td valign="top" width="100">EndTime</td>
		<td>
		<input type="text" name="EndTime" value="12"  id= formfield>
		</td>
		</tr>
		
		<tr bgcolor=#F8F8F8>
		<td valign="top" width="100">MinOffTime</td>
		<td>
		<input type="text" name="MinOffTime" value="1"  id= formfield>
		</td>
		</tr>
		
		<tr bgcolor=#F8F8F8>
		<td valign="top" width="100">TdifferenceOn</td>
		<td>
		<input type="text" name="TdifferenceOn" value="3.0"  id= formfield>
		</td>
		</tr>

		<tr bgcolor=#F8F8F8>
		<td valign="top" width="100">TdifferenceOff</td>
		<td>
		<input type="text" name="TdifferenceOff" value="1.0"  id= formfield>
		</td>
		</tr>

		
		<tr bgcolor=#F8F8F8>
		<td valign="top" width="100">OpeningTime</td>
		<td>
		<input type="text" name="OpeningTime" value="5"  id= formfield>
		</td>
		</tr>

		<tr bgcolor=#F8F8F8>
		<td valign="top" width="100">Tmin</td>
		<td>
		<input type="text" name="Tmin" value="14"  id= formfield>
		</td>
		</tr>



		<tr bgcolor=#BBBBBB><td>
		<b>Logging parameters:</b>
		</td><td></td></tr>
		
		<tr bgcolor=#F8F8F8>
		<td valign="top" width="100">SaveInterval</td>
		<td>
		<input type="text" name="SaveInterval" value="%H"  id= formfield>
		</td>
		</tr>
		
		<tr bgcolor=#F8F8F8>
		<td valign="top" width="100">LoggingInterval</td>
		<td>
		<input type="text" name="LoggingInterval" value="10"  id= formfield>
		</td>
		</tr>
		
		<tr bgcolor=#F8F8F8>
		<td valign="top" width="100">fileprefix</td>
		<td>
		<input type="text" name="fileprefix" value="kk002_"  id= formfield>
		</td>
		</tr>

		
		<tr bgcolor=#BBBBBB><td>
		<b>Parameters of central server:</b>
		</td><td></td></tr>		
		
		<tr bgcolor=#F8F8F8>
		<td valign="top" width="100">ftpserveraddr</td>
		<td>
		<input type="text" name="ftpserveraddr" value="139.13.179.37"  id= formfield>
		</td>
		</tr>
		
		<tr bgcolor=#F8F8F8>
		<td valign="top" width="100">FTPfolder</td>
		<td>
		<input type="text" name="FTPfolder" value="monicontrol"  id= formfield>
		</td>
		</tr>
		
		<tr bgcolor=#F8F8F8>
		<td valign="top" width="100">ftpbenutzer</td>
		<td>
		<input type="text" name="ftpbenutzer" value="kornkraft"  id= formfield>
		</td>
		</tr>

		<tr bgcolor=#F8F8F8>
		<td valign="top" width="100">ftppasswort</td>
		<td>
		<input type="text" name="ftppasswort" value="xxx"  id= formfield>
		</td>
		</tr>
		
		<tr bgcolor=#F8F8F8>
		<td valign="top" width="100">UploadRate</td>
		<td>
		<input type="text" name="UploadRate" value="3600"  id= formfield>
		</td>
		</tr>
		




		<tr bgcolor=#BBBBBB><td>
		<b>Other Parameters:</b> 
		</td><td></td></tr>
		
		<tr bgcolor=#F8F8F8>
		<td valign="top" width="100">internettype</td>
		<td>
		<input type="text" name="internettype" value="1"  id= formfield>
		</td>
		</tr>

		<tr bgcolor=#F8F8F8>
		<td valign="top" width="100">description</td>
		<td>
		<input type="text" name="description" value="Controlled ventillation system for Korn Kraft"  id= formfield>
		</td>
		</tr>



	</table>    
  
	<input type="submit" value="Set Parameter!" id= formbutton>
	</form>     <br>

';

	}

?>
