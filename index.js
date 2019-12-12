// https://www.youtube.com/watch?v=C4t6qfHZ6Tw

//const api = "https://api.coindesk.com/v1/bpi/historical/close.json?start=2019-01-01&end=2019-12-11";
const api = "https://api.coindesk.com/v1/bpi/historical/close.json";

//to load data from api

document.addEventListener("DOMContentLoaded",function(event) {
fetch(api)
	.then(function(response){ return response.json(); })
	.then(function(data) {
		var parsedData = parseData(data);
		drawChart(parsedData);
		})
		.catch(function(err){console.log(err);})
	});
	
function parseData(data) {
	var arr=[];
	for(var i in data.bpi) {
		arr.push({
			date : new Date(i),
			value : +data.bpi[i]
		});
	}
	return arr;
}

function drawChart(data) {
var svgWidth = 800, svgHeight = 450;
var margin = {top:20, right:20, bottom:38, left: 58};
var width = svgWidth - margin.left - margin.right;
var height = svgHeight - margin.top - margin.bottom;

var svg = d3.select('svg')
	.attr("width", svgWidth)
	.attr("height", svgHeight);
	
var g = svg.append("g")
	.attr("transform","translate(" + margin.left + "," + margin.top + ")");
	
var x = d3.scaleTime()
	.rangeRound([0,width]);
	
var y = d3.scaleLinear()
	.rangeRound([height,0]);
	
var line = d3.line()
	.x(function(d) { return x(d.date)})
	.y(function(d) { return y(d.value)})
	x.domain(d3.extent(data, function(d) {return d.date}));
	y.domain(d3.extent(data, function(d) {return d.value}));
	
g.append("g")
	.attr("transform", "translate(0," + height + ")" )
	.call(d3.axisBottom(x))
	.select(".domain")
	.remove();
	
g.append("g")
	.call(d3.axisLeft(y))
	.append("text")
	.attr("fill","#000")
	.attr("tranform","rotate(-90)")
	.attr("y",6)
	.attr("dy","0.71em")
	.attr("text-anchor","end")
	.text("Price ($)");
	 
g.append("path")
	.datum(data)
	.attr("fill","none")
	.attr("stroke","steelblue")
	.attr("stroke-linejoin","round")
	.attr("stroke-linecap","round")
	.attr("stroke-width", 2)
	.attr("d",line);
}
	