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

	refresh() // Then runs the refresh function for the first time.
	var int = self.setInterval(function () {
		refresh()
		}, 2000);   // Set the refresh() function to run every 1 seconds.   


	var tbl = document.getElementsByClassName('statetable'); // oder:
	if (screen.width<screen.height) 
		{
		tbl.style.width = "100%";
		} else {
		tbl.style.width = "50%";
		}


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
  var objA = document.getElementById('statetableclassA');
  if (objA != null)	{
	refreshA();
	} else {
	var objC = document.getElementById('statetableclassC');
	if (objC != null) {
		refreshC();
		}
	}
}

function bit_test(num, bit){
    return ((num>>bit) % 2 != 0)
}

function refreshA() {
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
			//var stateObj = JSON.parse(req.responseText);
			//
			//document.getElementById('datetime').innerHTML = stateObj.datetime;
			//document.getElementById('tin').innerHTML = stateObj.tin;
			//document.getElementById('tout').innerHTML = stateObj.tout;
			//if (stateObj.WindRainState==0) {
			//	document.getElementById('WindRainState').innerHTML = "Schlechte Wetter";
			//	document.getElementById("WindRainState").style.color = "#ff0000"; 
			//	} 
			//if (stateObj.WindRainState==1) {
			//	document.getElementById('WindRainState').innerHTML = "Gute Wetter";
			//	document.getElementById("WindRainState").style.color = "#000000"; 
			//	}
			//	
			//if (stateObj.FanState==0) {
			//	document.getElementById('FanState').innerHTML = "Aus";
			//	document.getElementById("FanState").style.color = "#ff0000"; 
			//	} 
			//if (stateObj.FanState==1) {
			//	document.getElementById('FanState').innerHTML = "An";
			//	document.getElementById("FanState").style.color = "#ff0000"; 
			//	} 
			//	
			//document.getElementById('houtside').innerHTML = stateObj.houtside;
			//
			//document.getElementById('auto').innerHTML = stateObj.auto;
			//document.getElementById('mainOnCondition').innerHTML = stateObj.mainOnCondition;
			//document.getElementById('tMinCondition').innerHTML = stateObj.tMinCondition;
			//document.getElementById('timeCondition').innerHTML = stateObj.timeCondition;
			//document.getElementById('windRainCondition').innerHTML = stateObj.windRainCondition;
			//document.getElementById('minOffTimeCondition').innerHTML = stateObj.minOffTimeCondition;
			//document.getElementById('mainOffCondition').innerHTML = stateObj.mainOffCondition;
			//document.getElementById('jonok').innerHTML = stateObj.jonok;
			//document.getElementById('joffok').innerHTML = stateObj.joffok;
			//document.getElementById('RelayK2State').innerHTML = stateObj.RelayK2State;
			//document.getElementById('RelayK3State').innerHTML = stateObj.RelayK3State;
			// this was json. now:
			
			var vals = req.responseText.split('	');

			document.getElementById('datetime').innerHTML = vals[0];
			document.getElementById('tin').innerHTML = vals[1];
			document.getElementById('tout').innerHTML = vals[2];
			document.getElementById('houtside').innerHTML = vals[3];
			
			
			var allbits = parseInt(vals[6], 10);

			var bit0 = bit_test(allbits, 0); // gets the 0th bit FunState
			var bit1 = bit_test(allbits, 1); //          1th bit WindRainState
			var bit2 = bit_test(allbits, 2); //          2th bit auto
			var bit3 = bit_test(allbits, 3); //          3th bit auto mainOnCondition
			var bit4 = bit_test(allbits, 4); //          4th bit auto tMinCondition
			var bit5 = bit_test(allbits, 5); //          5th bit auto timeCondition
			var bit6 = bit_test(allbits, 6); //          6th bit auto windRainCondition
			var bit7 = bit_test(allbits, 7); //          7th bit auto minOffTimeCondition
			var bit8 = bit_test(allbits, 8); //          8th bit auto mainOffCondition
			var bit9 = bit_test(allbits, 9); //          9th bit auto RelayK2State
			var bit10= bit_test(allbits,10); //         10th bit auto RelayK3State

			document.getElementById('auto').innerHTML = bit2.toString();
			
			if (bit1) {
				document.getElementById('WindRainState').innerHTML = "Gute Wetter";
				document.getElementById("WindRainState").style.color = "#000000"; 
				} else {
				document.getElementById('WindRainState').innerHTML = "Schlechte Wetter";
				document.getElementById("WindRainState").style.color = "#ff0000"; 
				}
				
			if (bit0) {
				document.getElementById('FanState').innerHTML = "An";
				document.getElementById("FanState").style.color = "#ff0000"; 
				} else {
				document.getElementById('FanState').innerHTML = "Aus";
				document.getElementById("FanState").style.color = "#ff0000"; 
				} 
				

			document.getElementById('mainOnCondition').innerHTML = bit3.toString();
			document.getElementById('tMinCondition').innerHTML = bit4.toString();
			document.getElementById('timeCondition').innerHTML = bit5.toString();
			document.getElementById('windRainCondition').innerHTML = bit6.toString();
			document.getElementById('minOffTimeCondition').innerHTML = bit7.toString();
			document.getElementById('mainOffCondition').innerHTML = bit8.toString();
			
			document.getElementById('jonok').innerHTML = vals[4];
			document.getElementById('joffok').innerHTML = vals[5];
			
			document.getElementById('RelayK2State').innerHTML = bit9.toString();
			document.getElementById('RelayK3State').innerHTML = bit10.toString();
			
			
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

function refreshC() {
	// refresh function for system of class C !RHTCO2 monitoring control
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
