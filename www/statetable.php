<?php
include ("daoventserver.php");
$s = new ventserver();
$s->GetState(); // json has shown drawbacks! too big! therefore made general! different format
?>
