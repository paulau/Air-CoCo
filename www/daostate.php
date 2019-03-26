<?php

class ventstate {
	var $service_port, $address, $socket, $result;
	
	
	function __construct() {
		$this->service_port = 40012;
		$this->address = 'localhost';
		
		/* Einen TCP/IP-Socket erzeugen. */
		$this->socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
		if ($this->socket === false) {
			echo "socket_create() fehlgeschlagen: Grund: " . socket_strerror(socket_last_error()) . "\n";
			} 

		//echo "Versuche, zu '$address' auf Port '$service_port' zu verbinden ... <br>";
		$this->result = socket_connect($this->socket, $this->address, $this->service_port);
		}

	function __destruct() {
		//echo "Socket schliessen ...<br>";
		socket_close($this->socket);
		}

	function StateTable()
		{
		$in = "GetData";
		$out = '';
		//echo "HTTP HEAD request senden ...<br>";
		socket_write($this->socket, $in, strlen($in));
			
		//echo "Serverantwort lesen:\n\n<br>";
		echo "
		<table id='statetable' align=center border='1px solid black' cellPadding=0 cellSpacing=0 width=100%>
		<tr bgcolor='#00EE00'>  <th>Datum, Uhrzeit</th> <th>Tin</th> <th>Tout</th> <th>Wind-Regen</th> <th>Luftung</th>   </tr> ";
		
		echo "<tr>";
		while ($out = socket_read($this->socket, 64)) {
			$elements = explode("\t", $out);		
			$lengt_of_el = count($elements);
			$i = 0;
			while ($i < $lengt_of_el)
				{
				echo "<td align=center> <br>" . $elements[$i] . " <br><br></td>";
				$i++;
				}
			}
		echo "</tr></table>";
		}

	}
?>
