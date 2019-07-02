<?php

class ventserver {
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

	function GetState() // json has shown drawbacks! too big! therefore made general! different format
		{
		$in = "GetData";
		$out = '';
		//echo "HTTP HEAD request senden ...<br>";
		socket_write($this->socket, $in, strlen($in));
		//echo "Serverantwort lesen:\n\n<br>";
		$out = socket_read($this->socket, 64);
		echo $out;
		}

	function SendCommand($cmnd) // switch to automatic regime
		{		
		socket_write($this->socket, $cmnd, strlen($cmnd));
		}

	// each device has different sets of parameters and state variables.
	// it should be described in different pages of WEB GUI. 
	// To decide, which interface should be chosen, the 
	// monicontrol class of each model should return its own name,
	// via GetDeviceName function via according server request
	function GetDeviceName() // switch to automatic regime
		{		
		$in = "GetDeviceName";
		$out = '';
		//echo "HTTP HEAD request senden ...<br>";
		socket_write($this->socket, $in, strlen($in));
		//echo "Serverantwort lesen:\n\n<br>";
		$out = socket_read($this->socket, 64);
		return $out;
		}


	}
?>
