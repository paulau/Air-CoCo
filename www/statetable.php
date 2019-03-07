<?php	


function StateTable()
	{
	$service_port = 40012;
	$address = 'localhost';
	
	/* Einen TCP/IP-Socket erzeugen. */
	$socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
	if ($socket === false) {
		echo "socket_create() fehlgeschlagen: Grund: " . socket_strerror(socket_last_error()) . "\n";
		} else {
			//echo "<br> OK.\n";
		}
	
	//echo "Versuche, zu '$address' auf Port '$service_port' zu verbinden ... <br>";
	$result = socket_connect($socket, $address, $service_port);
	/*
	if ($result === false) {
		echo "socket_connect() fehlgeschlagen.\nGrund: ($result) " . socket_strerror(socket_last_error($socket)) . "\n";
	} else {
		echo "OK.\n<br>";
	}
	*/
	
	$in = "GetData";
	$out = '';
	
	//echo "HTTP HEAD request senden ...<br>";
	socket_write($socket, $in, strlen($in));
	//echo "OK.\n";
	
	//echo "Serverantwort lesen:\n\n<br>";
	echo "
	<table align=center border='1px solid black' cellPadding=0 cellSpacing=0 width=100%>
	<tr bgcolor='#00EE00'>  <th>Datum, Uhrzeit</th> <th>Tin</th> <th>Tout</th> <th>Wind-Regen</th> <th>Luftung</th>   </tr> ";
	
	echo "<tr>";
	while ($out = socket_read($socket, 64)) {
		#echo $out;
		$elements = explode("\t", $out);
		
		$lengt_of_el = count($elements);
		$i = 0;
		//echo $lengt_of_el;
		while ($i < $lengt_of_el)
			{	
			echo "<td align=center> <br>" . $elements[$i] . " <br><br></td>";
			
			//if (($i % 2) == 1) {
			//	echo("<tr bgcolor='EEEEEE' onmouseover='setcolorA(this,0);ActivateImage(" . $Id  . ");' onmouseout='setcolorA(this,1)' onclick='addttobasketA(this)'><td name='goodname'>" . $MessageDate . "</td><td valign='Top' id='pricecolumn' name='goodprice'>" . $ShortMessage . "</td></tr>" );
			//	} else {
			//	echo("<tr bgcolor='FFFFFF' onmouseover='setcolorA(this,0);ActivateImage(" . $Id . ");' onmouseout='setcolorA(this,2)' onclick='addttobasketA(this)'><td name='goodname'>" . $MessageDate . "</td><td valign='Top' id='pricecolumn' name='goodprice'>" . $ShortMessage . "</td></tr>" );	
			//	}
			
			$i++;	
			}
		
	}
	echo "</tr>";
	
	echo "</table>";
	
	echo "<br>";
	
	//echo "Socket schliessen ...<br>";
	socket_close($socket);
	//echo "OK.\n\n<br>";


	}

?>
