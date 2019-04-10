<?php
include ("sqlsettings.php"); // import settings of sql database
require ("auth.php"); // import settings of sql database
/*
 * The registration takes place only once, at first start of webapplication.
 */

function register() {
	//echo ("halo");
	$pdo = new PDO('mysql:host=localhost;dbname=AirCoCo', 'runner', 'runner123');
	$error = false;
	$login = $_POST['login'];
	$passwort = $_POST['passwort'];
	$passwort2 = $_POST['passwort2'];
	
	//if(!filter_var($email, FILTER_VALIDATE_EMAIL)) {
	//	echo 'Bitte eine gültige E-Mail-Adresse eingeben<br>';
	//	$error = true;
	//	}
	if(strlen($passwort) == 0) {
		echo 'Bitte ein Passwort angeben<br>';
		$error = true;
		}
	if($passwort != $passwort2) {
		echo 'Die Passwörter müssen übereinstimmen<br>';
		$error = true;
		}
	
	//Überprüfe, dass das Login noch nicht registriert wurde
	if(!$error) { 
		$statement = $pdo->prepare("SELECT * FROM users WHERE login = :login");
		$result = $statement->execute(array('login' => $login));
		$user = $statement->fetch();
		
		if($user !== false) {
				echo 'Diese Login ist bereits vergeben<br>';
				$error = true;
			}    
		}
	
	//Keine Fehler, wir können den Nutzer registrieren
	if(!$error) {    
		$passwort_hash = password_hash($passwort, PASSWORD_DEFAULT);
		
		$statement = $pdo->prepare("INSERT INTO users (login, passwort) VALUES (:login, :passwort)");
		$result = $statement->execute(array('login' => $login, 'passwort' => $passwort_hash));
		
		if($result) {
			include("parameters.php");
			} else {
			echo 'Beim Abspeichern ist leider ein Fehler aufgetreten<br>';
			}
		} 

	} 
	
	
# main code: 
$a = new Authorisation($dbhost,$sqluser,$sqlpass,$sqldb);
if (!$a->Registered && isset($_GET['register']))
	{
	register();
	}

?>
