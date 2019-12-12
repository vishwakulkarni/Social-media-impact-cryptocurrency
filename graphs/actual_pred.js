var predictedPrice = []
var index = []
var actualPrice = []


document.addEventListener("DOMContentLoaded",function(event) {
 

var mydata = JSON.parse(data)

//console.log(mydata.results[0][0])

for(var i in mydata.results) {
		
		predictedPrice.push(mydata.results[i][0])
		actualPrice.push(mydata.results[i][1])
		index.push(i)
		
	}

//console.log(index);

var ctx = document.getElementById("myChart");
var myChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: index,
    datasets: [
      { 
        data: predictedPrice,
		label: "Predicted Price ",
		borderColor: "#3e95cd",
		fill: false
      },
	  {
		data: actualPrice,
		label: "Actual Price",
		borderColor: "#ff0000",
		fill: false
	  }  
    ]
  }
});


 
});
	
	
