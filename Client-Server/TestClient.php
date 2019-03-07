<?php
error_reporting(E_ALL);

echo "<h2>TCP/IP-Verbindung</h2>\n";


$service_port = 40012;
$address = 'localhost';

/* Einen TCP/IP-Socket erzeugen. */
$socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
if ($socket === false) {
    echo "socket_create() fehlgeschlagen: Grund: " . socket_strerror(socket_last_error()) . "\n";
	} else {
		echo "OK.\n";
	}

echo "Versuche, zu '$address' auf Port '$service_port' zu verbinden ... <br>";
$result = socket_connect($socket, $address, $service_port);
if ($result === false) {
    echo "socket_connect() fehlgeschlagen.\nGrund: ($result) " . socket_strerror(socket_last_error($socket)) . "\n";
} else {
    echo "OK.\n";
}

$in = "GetData";
$out = '';

echo "HTTP HEAD request senden ...<br>";
socket_write($socket, $in, strlen($in));
echo "OK.\n";

echo "Serverantwort lesen:\n\n<br>";
while ($out = socket_read($socket, 64)) {
    echo $out;
}

echo "<br>";

echo "Socket schliessen ...<br>";
socket_close($socket);
echo "OK.\n\n";
?>
