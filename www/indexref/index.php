<?php	


$link = 'http://'.$_SERVER['HTTP_HOST'] . $_SERVER['REQUEST_URI'].'air-coco/';
echo ($link);
header('Location: '.$link); // redirect to previous page.

?>
