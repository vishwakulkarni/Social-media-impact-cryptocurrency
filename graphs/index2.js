var bitcoinPrice = []
var time = []
var predictedPrice = []

const api = "https://api.coindesk.com/v1/bpi/historical/close.json";

document.addEventListener("DOMContentLoaded",function(event) {
fetch(api)
	.then(function(response){ return response.json(); })
	.then(function(data) {
		parseData(data);
		})
		.catch(function(err){console.log(err);})
	});
	
function parseData(data) {
	for(var i in data.bpi) {
		time.push(new Date(i));
		bitcoinPrice.push(data.bpi[i]);
		predictedPrice.push(data.bpi[i]+200);
	}
}

var ctx = document.getElementById("myChart");
var myChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: time,
    datasets: [
      { 
        data: bitcoinPrice,
		label: "Bitcoin Price in last 30 days",
		borderColor: "#3e95cd",
		fill: false
      },
	  {
		data: predictedPrice,
		label: "Predicted Price",
		borderColor: "#ff0000",
		fill: false
	  }  
    ]
  }
});
