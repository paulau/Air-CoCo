// Functions to update the page automatically

function init() // This is the function the browser first runs when it's loaded.
	{
	//smartphon 360x640
	//screen.width<screen.height

	var slidehidden = document.getElementById('slidehiddenid');
	var slidetop = document.getElementById('slidetopid');
	if (screen.width<800) 
		{
		slidetop.src="slide1_w640.jpg";
		slidehidden.src="slide2_w640.jpg";
		}


	refreshSlide();
	var int = self.setInterval(function () {
		refreshSlide()
		}, 5000);   // Set the refresh() function to run every 1 seconds.	

	refreshrhtco2() // Then runs the refresh function for the first time.
	var int = self.setInterval(function () {
		refreshrhtco2()
		}, 1000);   // Set the refresh() function to run every 1 seconds.   
	}

function refreshSlide() {
	var slidetop = document.getElementById('slidetopid');
	if (slidetop.style.opacity==1.0)
		{
		//alert("hallo");	
		slidetop.style.opacity=0.0;
		} else {
		slidetop.style.opacity=1.0;
		}
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
			if (stateObj.WindRainState==0) {
				document.getElementById('WindRainState').innerHTML = "Gute Wetter";
				document.getElementById("WindRainState").style.color = "#ff0000"; 
				} 
			if (stateObj.WindRainState==1) {
				document.getElementById('WindRainState').innerHTML = "Schlechte Wetter";
				document.getElementById("WindRainState").style.color = "#000000"; 
				}
				
			if (stateObj.FanState==0) {
				document.getElementById('FanState').innerHTML = "Aus";
				document.getElementById("FanState").style.color = "#ff0000"; 
				} 
			if (stateObj.FanState==1) {
				document.getElementById('FanState').innerHTML = "An";
				document.getElementById("FanState").style.color = "#000000"; 
				}
			
			 stateObj.FanState;
			}
		}
	req.send();
	}


function ActivateImage(fname) {
	var folder = "datapics/";
	var res = folder.concat(fname);
	document.images['exposed'].src = res;
	}


function sendcmd(cmd) {
	var req = new XMLHttpRequest();  
	var myurl = 'sendcmdtoventserver.php?cmd='.concat(cmd.toString());
	req.open("GET", myurl, true); // Grabs whatever you've written in this file	
	req.send();
	}

function refreshrhtco2() {
	var currentdate = new Date(); 
	var datetime = "Last Sync: " + currentdate.getDate() + "/"
                + (currentdate.getMonth()+1)  + "/" 
                + currentdate.getFullYear() + " @ "  
                + currentdate.getHours() + ":"  
                + currentdate.getMinutes() + ":" 
                + currentdate.getSeconds();
	
	document.getElementById('title').innerHTML = datetime;
	
	if (screen.width<800) 
		{
		document.getElementById('MainTable').width='100%';
		document.getElementById('MainTableTD').width='100%';
		document.getElementById('LeftMargin').width='20';
		document.getElementById('RightMargin').width='20';
		}


	
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
			document.getElementById('h').innerHTML = stateObj.h;
			document.getElementById('t').innerHTML = stateObj.t;
			document.getElementById('co2').innerHTML = stateObj.co2;
			
			if (stateObj.FanState==0) {
				document.getElementById('FanState').innerHTML = "Aus";
				document.getElementById("FanState").style.color = "#ff0000"; 
				} 
			if (stateObj.FanState==1) {
				document.getElementById('FanState').innerHTML = "An";
				document.getElementById("FanState").style.color = "#000000"; 
				}
			
			 stateObj.FanState;
			}
		}
	req.send();
	}
