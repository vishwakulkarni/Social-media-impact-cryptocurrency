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
	
document.addEventListener("DOMContentLoaded",function(event) {
fetch(api)
	.then(function(response){ return response.json(); })
	.then(function(data1) {
		parseData1(data1);
		})
		.catch(function(err){console.log(err);})
	});	
	
function parseData(data) {
	for(var i in data.bpi) {
		time.push(new Date(i));
		bitcoinPrice.push(data.bpi[i]);
		
	}
}

function parseData1(data1) {
	
	var p=0;
	
	for(var i in data1.bpi) {
		time.push(new Date(i));
		if(p%2 == 0 )predictedPrice.push(data1.bpi[i]+200);
		else predictedPrice.push(data1.bpi[i]-200);
		
		p++;
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