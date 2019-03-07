// <script src='common.js'></script>
// NOT YET WORKING
// Functions to update the page automatically
function refresh() {
  var req = new XMLHttpRequest();
  console.log("Grabbing Value");
  req.onreadystatechange = function () {
    if (req.readyState == 4 && req.status == 200) {
      document.getElementById('StateTable').innerText = req.responseText;
    }
  }
  req.open("GET", 'reload.txt', true); // Grabs whatever you've written in this file
  req.send(null);
}

function init() // This is the function the browser first runs when it's loaded.
{
  refresh() // Then runs the refresh function for the first time.
  var int = self.setInterval(function () {
    refresh()
  }, 10000); 
  // Set the refresh() function to run every 10 seconds. 
  // [1 second would be 1000, and 1/10th of a second would be 100 etc.
}
