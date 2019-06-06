<?php
include ("daoventserver.php");
$s = new ventserver();
$cmnd = $_GET['cmd'];
echo $cmnd;
$s->SendCommand($cmnd);
?>

