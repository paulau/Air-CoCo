<?php
function FindAndReplace($sqluser,$sqlpass,$sqldb,$dbhost, $ParamN, $ParamV)
	{
	$db = mysqli_connect($dbhost, $sqluser, $sqlpass, $sqldb);
	if(!$db)
	{
	exit("Verbindungsfehler: ".mysqli_connect_error());
	}
	$sql = "UPDATE " . $sqldb . ".Parameters SET ParameterValue = '". $ParamV . "' WHERE ParameterName='". $ParamN. "';";
	
	echo "<br>"; 
	echo $sql; 
	$result = mysqli_query($db, $sql) or die(mysqli_error());
	mysqli_close($db);
	}


function SaveParametersToDatabase($sqluser,$sqlpass,$sqldb,$dbhost)
	{
	// This function checks whether Parameter is defined in "POST" of PHP
	// and adds it into SQL request to update Database:
	
	
	if ($_POST <> null) 
		{
		if ($_POST['sensor_inside_id']!=null) 
			{
			//echo 'sensor_inside_id=' . $_POST['sensor_inside_id'];
			FindAndReplace($sqluser,$sqlpass,$sqldb,$dbhost, 'sensor_inside_id', $_POST['sensor_inside_id']);
			}

		if ($_POST['pin1']!=null) 
			{
			FindAndReplace($sqluser,$sqlpass,$sqldb,$dbhost, 'pin1', $_POST['pin1']);
			}


		}
	
	}


?>
