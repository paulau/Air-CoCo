<?php

class Parameters {
	
	var $db;
	var $table;
	
	function __construct($dbhost, $sqluser, $sqlpass, $sqldb) {
		
		$this->db = mysqli_connect($dbhost, $sqluser, $sqlpass, $sqldb);
		if(!$this->db)
			{
			exit("Verbindungsfehler: ".mysqli_connect_error());
			}
		}

	function __destruct() {
		mysqli_close($this->db);
		}
	
	function GetParameterForm()
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
		
		$sql = "select * from AirCoCo.Parameters order by Id desc limit 50";
		$result = mysqli_query($this->db, $sql) or die(mysqli_error());
	
		// logically does not belong to dao move to calling php
		// move it into new View class!!!
		// see Model View Controller pattern 
		
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
		// but for user friendly interface, all parameters should be listed 
		// in certain order and devided onto sections. 
		// to do it in settings??.py would be a bit difficult. 
		// no need for now. 
		// therefore we just remake the code manually, stating, what parameters 
		// belong to what sections. See code below commented ona. 
		
		//while($row = mysqli_fetch_array($result)) {
		//	$PName = $row['ParameterName'];
		//	$PValue = $row['ParameterValue'];
		//	//echo $PName . " ". $PValue . "<br>";
		//	
		//	echo '<tr bgcolor=#F8F8F8>
		//	<td valign="top" width="100">';
		//	echo $PName;
		//	echo '</td>
		//	<td>
		//	<input type="text" name="';
		//	echo  $PName .'" value="'.$PValue.'"  id= formfield>';
		//	echo '
		//	</td>
		//	</tr>';
		//	}
	
		// Save "result into php array":
		$this->table = array();	
		while($row = mysqli_fetch_array($result)) {
			$PName = $row['ParameterName'];
			$PValue = $row['ParameterValue'];
			$this->table[$PName] = $PValue;
			}
	
		$this->printSectionName("Parameters of Sensors and relays:");
		
		$this->printParameterLine("sensor_inside_id");
		$this->printParameterLine("sensor_outside_id");
		$this->printParameterLine("pin1");
		$this->printParameterLine("pin2");
		$this->printParameterLine("RelayK1ControlPin");
		$this->printParameterLine("RelayK2ControlPin");
		$this->printParameterLine("RelayK3ControlPin");
			
		$this->printSectionName("Parameters of control:");
		
		$this->printParameterLine("StartTime");
		$this->printParameterLine("EndTime");
		$this->printParameterLine("MinOffTime");
		$this->printParameterLine("TdifferenceOn");
		$this->printParameterLine("TdifferenceOff");
		$this->printParameterLine("OpeningTime");
		$this->printParameterLine("Tmin");
		
		$this->printSectionName("Logging parameters:");
		
		$this->printParameterLine("SaveInterval");
		$this->printParameterLine("LoggingInterval");
		$this->printParameterLine("fileprefix");

		$this->printSectionName("Parameters of central server:");
		
		$this->printParameterLine("ftpserveraddr");
		$this->printParameterLine("FTPfolder");
		$this->printParameterLine("ftpbenutzer");
		$this->printParameterLine("ftppasswort");
		$this->printParameterLine("UploadRate");
		
		
		$this->printSectionName("Other Parameters:");
		
		$this->printParameterLine("internettype");
		$this->printParameterLine("description");
		
		echo '
			</table>    
			<b>Attention! The system will be reboot after pressing the button!</b><br>
			<b>The pages of the control system will be up to 3 min unavailable!</b><br>
			<input type="submit" value="Set Parameter!" id= formbutton>
			</form>';
		}
	
	
	function printParameterLine($name)
	// first argument $name - parametername to be printed
	// second argument - result of sql request - "table of all parameters"
		{
		echo '<tr bgcolor=#F8F8F8>
		<td valign="top" width="100">';
		echo $name;
		echo '</td>
		<td>
		<input type="text" name="';
		echo  $name .'" value="'.$this->table[$name].'"  id= formfield>';
		echo '
		</td>
		</tr>';
		}
	
	function printSectionName($sname)
		{
		echo "</table>";
		echo "<table><tr><td valign='top' width='275' bgcolor=#AAAAAA><b>" . $sname . "</b></td></tr></table>";
		echo "<table>";
		}
	
	
	
	function FindAndReplace($ParamN, $ParamV)
		{
		$sql = "UPDATE " . $sqldb . ".Parameters SET ParameterValue = '". $ParamV . "' WHERE ParameterName='". $ParamN. "';";
		//echo "<br>". $sql; 
		$result = mysqli_query($this->db, $sql) or die(mysqli_error());
		}
	
	
	function SaveParametersToDatabase()
		{
		// This function checks whether Parameter is defined in "POST" of PHP
		// and adds it into SQL request to update Database:
		
		
		if ($_POST <> null) 
			{
			//
			//	
			//if ($_POST['sensor_inside_id']!=null) 
			//	{
			//	//echo 'sensor_inside_id=' . $_POST['sensor_inside_id'];
			//	$this->FindAndReplace('sensor_inside_id', $_POST['sensor_inside_id']);
			//	}
			//if ($_POST['pin1']!=null) 
			//	{
			//	$this->FindAndReplace('pin1', $_POST['pin1']);
			//	}
			
			
			// cycle over all POST variables. 
			foreach($_POST as $key => $value)
				{
				//echo $key . "=". $value ."<br>";
				$this->FindAndReplace($key, $value);
				}
			
			// After update of parameters in database we should restart monitoring control programm
			$this->SendRebootRequest();
			}
		}
	
	function SendRebootRequest() //  to vent server
		{
		$service_port = 40012;
		$address = 'localhost';
		$socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP); // Einen TCP/IP-Socket erzeugen. 
		if ($socket === false) {
			echo "socket_create() fehlgeschlagen: Grund: " . socket_strerror(socket_last_error()) . "\n";
			} 
		$result = socket_connect($socket, $address, $service_port); // Versuche, zu '$address' auf Port '$service_port' zu verbinden 
		if ($result === false) {
			echo "socket_connect() fehlgeschlagen.\nGrund: ($result) " . socket_strerror(socket_last_error($socket)) . "\n";
			} 
		$in = "Reboot";
		socket_write($socket, $in, strlen($in)); // HTTP HEAD request senden 
		socket_close($socket);
		}
	
	}

?>
