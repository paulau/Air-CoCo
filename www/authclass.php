<?php

/*
 * The registration takes place only once, at first start of webapplication.
 * The user gets form to enter username and password for registration only once.
 * 
 * On each new start of the web application, the only first registered 
 * user has rights to watch and change certain areas of the wabapplication.
 * 
 * */


class Authorisation  {
	var $DatabaseName; 
	var $UsersTable;
	var $Authorised;
	var $Registered;
	
	function __construct($dbhost, $sqluser, $sqlpass, $sqldb) {
		
		$this->Authorised = false;
		$this->Registered = false;
		
		$this->DatabaseName = $sqldb;
		$this->db = mysqli_connect($dbhost, $sqluser, $sqlpass, $sqldb);
		if(!$this->db)
			{
			exit("Database should be already created and the user - initialised. Verbindungsfehler: ".mysqli_connect_error());
			}
		$this->Registered = $this->isRegistered();
		if ($this->Registered) {
			$this->Authorised = $this->isLoggedIn();
			}
		}

	function __destruct() {
		mysqli_close($this->db);
		}
	
	function isRegistered()
		{
		// check, whether the Database and table already exists.
		$sql = "select * from ".$this->DatabaseName.".users order by Id desc limit 50";
		$result = mysqli_query($this->db, $sql); // or die(mysqli_error());
		// Save "result into php array":
		$this->UsersTable = array();
		while($row = mysqli_fetch_array($result)) {
			$UName = $row['user'];
			$PassValue = $row['pass'];
			$this->UsersTable[$UName] = $PassValue;
			}
		$UsersAmount = count($this->UsersTable);
		//echo ($UsersAmount);
		$check = ($UsersAmount > 0);
		return $check;
		}

	function checkAccess()
		{
		//echo ("is registered = false");
		if (!$this->Registered) {
			include("register.html");
			} else {
			
			session_start();
			if(!isset($_SESSION['login'])) {
				include("login.html");
				//die('Bitte zuerst <a href="login.php">einloggen</a>');
				$this->Authorised = false;
				} else {
				$this->Authorised = true;
				}
			}
		}

	function isLoggedIn(){
		return $true;
		}
	
	function createUsersTable() {
		$sql =" DROP TABLE 'users'";
		$result = mysqli_query($this->db, $sql);
		$sql =" CREATE TABLE ". $this->DatabaseName .".users (id int PRIMARY KEY AUTO_INCREMENT, login varchar(255), passwort varchar(255));";
		//echo ($sql . "<br>");
		$result = mysqli_query($this->db, $sql); // or die(mysqli_error());
		}
		
	function register($login, $passwort, $passwort2, $referer) {
		$error = false;
		
		
		
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
		//if(!$error) { 
		//	  $sql = "SELECT * FROM ".$this->DatabaseName.".users WHERE login = ".$login;
		//	  $result = mysqli_query($this->db, $sql); // or die(mysqli_error());			
		//	  $this->UsersTable = array();
		//	  while($row = mysqli_fetch_array($result)) {
		//	  	$UName = $row['login'];
		//	  	$PassValue = $row['passwort'];
		//	  	$this->UsersTable[$UName] = $PassValue;
		//	  	}
		//	  $UsersAmount = count($this->UsersTable);
		//	  
		//	  if($UsersAmount>0) {
		//	  	echo 'Diese Login ist bereits vergeben<br>';
		//	  	$error = true;
		//	  	}    
		//	}

		//Keine Fehler, wir können den Nutzer registrieren
		if(!$error) {
			$this->createUsersTable();
			
			$passwort_hash = password_hash($passwort, PASSWORD_DEFAULT);
			$sql = "INSERT INTO ".$this->DatabaseName. ".users (login, passwort) VALUES ('".$login ."','" . $passwort_hash."');";
			$result = mysqli_query($this->db, $sql); // or die(mysqli_error());
			
			if($result) {
				header('Location: '.$referer); // redirect to previous page.
				} else {
				echo 'Beim Abspeichern ist leider ein Fehler aufgetreten<br>';
				}
			}
		}
		
	function login($login, $passwort, $referer)
		{
		$sql = "SELECT * FROM ".$this->DatabaseName.".users WHERE login = '".$login."';";
		//echo ($sql . "<br>");
		$result = mysqli_query($this->db, $sql); // or die(mysqli_error());

		// the only one record is needed (since users are unique):
		$row = mysqli_fetch_array($result);
		$UName = $row['login'];
		$PassValue = $row['passwort'];

		//Überprüfung des Passworts	
		if ( (strlen($UName) >0) && password_verify($passwort, $PassValue)) {
			$_SESSION['login'] = $UName;
			echo("Successful login<br>");

			//die('Login erfolgreich. Weiter zu <a href="geheim.php">internen Bereich</a>');
			} 
		//else {
		//	$errorMessage = "Login oder Passwort war ungültig<br>";
		//if(isset($errorMessage)) {
		//    echo $errorMessage;
		//}
		//}
		// in any case forward to calling page:
		header('Location: '.$referer); // redirect to previous page.

		}
	
	function logout($referer)
		{
		session_start();
		session_destroy();
		header('Location: '.$referer); // redirect to previous page.
		}

	}

?>
