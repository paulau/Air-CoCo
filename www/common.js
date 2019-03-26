// Functions to update the page automatically

function init() // This is the function the browser first runs when it's loaded.
	{
	refresh() // Then runs the refresh function for the first time.
	var int = self.setInterval(function () {
		refresh()
		}, 1000);   // Set the refresh() function to run every 1 seconds.   
	}


function refresh() {
	var currentdate = new Date(); 
	var datetime = "Last Sync: " + currentdate.getDate() + "/"
                + (currentdate.getMonth()+1)  + "/" 
                + currentdate.getFullYear() + " @ "  
                + currentdate.getHours() + ":"  
                + currentdate.getMinutes() + ":" 
                + currentdate.getSeconds();
	
	document.getElementById('title').innerHTML = datetime;
	
	var req = new XMLHttpRequest();  //  console.log("Grabbing Value");
	//req.open("GET", 'jsontest.php', true); // Grabs whatever you've written in this file	
	req.open("GET", 'statetable.php', true); // Grabs whatever you've written in this file	
	req.onreadystatechange = function () {
		// this function will be performed apparently, when request is ready
		if (req.readyState == 4) {
			//alert(req.responseText);			
			var stateObj = JSON.parse(req.responseText);
			//alert(stateObj.datetime);			
			document.getElementById('datetime').innerHTML = stateObj.datetime;
			document.getElementById('tin').innerHTML = stateObj.tin;
			document.getElementById('tout').innerHTML = stateObj.tout;
			document.getElementById('WindRainState').innerHTML = stateObj.WindRainState;
			document.getElementById('FanState').innerHTML = stateObj.FanState;
			}
		}
	req.send();
	}
