<?php
include ("sqlsettings.php"); // import settings of sql database
require ("authclass.php"); // import authorisation class
/*
 * The registration takes place only once, at first start of webapplication.
 * Implementation is based on 
 * https://www.php-einfach.de/experte/php-codebeispiele/loginscript/
 */

$login = $_POST['login'];
$passwort = $_POST['passwort'];
$passwort2 = $_POST['passwort2'];
$referer = $_SERVER['HTTP_REFERER'];

$a = new Authorisation($dbhost,$sqluser,$sqlpass,$sqldb);
if(isset($_GET['register'])) {
	if (!$a->Registered && isset($_GET['register']))
		{
		$a->register($login, $passwort, $passwort2, $referer);
		}
	}

session_start();

if(isset($_GET['login'])) {
	$a->login($login, $passwort, $referer);
	}
if(isset($_GET['logout'])) {
	$a->logout($referer);
	}

?>
