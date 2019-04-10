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
			} else {
			$this->createUsersTable();
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

			if (!$this->Authorised) {
				include("login.html");
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
	}

?>
