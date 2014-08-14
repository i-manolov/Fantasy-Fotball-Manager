function plot7( p, s, data) {
//alert("7")

	// set the stage
	var margin = {t:30, r:40, b:20, l:40 },
		w = 600 - margin.l - margin.r,
		h = 500 - margin.t - margin.b,
		x = d3.scale.linear().range([0, w]),
		y = d3.scale.linear().range([h - 60, 0]),
		//colors that will reflect player position
		color = d3.scale.category10();

	var svg = d3.select("#chart").append("svg")
		.attr("width", w + margin.l + margin.r)
		.attr("height", h + margin.t + margin.b);

	// set axes, as well as details on their ticks
	var xAxis = d3.svg.axis()
		.scale(x)
		.ticks(20)
		.tickSubdivide(true)
		.tickSize(6, 3, 0)
		.orient("bottom");

	var yAxis = d3.svg.axis()
		.scale(y)
		.ticks(20)
		.tickSubdivide(true)
		.tickSize(6, 3, 0)
		.orient("left");

	// group that will contain all of the plots
	var groups = svg.append("g").attr("transform", "translate(" + margin.l + "," + margin.t + ")");

	// array of the positions, used for the legend
	
	var positions 	= p
	var status		= s
c=1

// call in the data, and do everything that is data-driven
	f1(data)
	function f1(data) {
		
		// sort data alphabetically by region, so that the colors match with legend
		if (c == 1) {
			data.sort(function(a, b) { return d3.ascending(a.position, b.position); })
		}
		else {
			data.sort(function(a, b) { return d3.ascending(a.status, b.status); })		
		}
		console.log(data)
		x.domain(d3.extent(data, function(d) { return d.weight; })).nice();
		y.domain(d3.extent(data, function(d) { return d.height_cm; })).nice();


	// style the circles, set their locations based on data
	var circles =
	groups.selectAll("circle")
		.data(data)
	  .enter().append("circle")
	  .attr("class", "circles")
	  .attr({
	    cx: function(d) { return x(+d.weight); },
	    cy: function(d) { return y(+d.height_cm); },
	    r: 8,
	    id: function(d) { return d.position; }
	  })
		
		.style("fill", function(d) { return color(d.position); });

	// what to do when we mouse over a bubble
	var mouseOn = function() { 
		var circle = d3.select(this);

	// transition to increase size/opacity of bubble
		circle.transition()
		.duration(800).style("opacity", 1)
		.attr("r", 16).ease("elastic");

		// append lines to bubbles that will be used to show the precise data points.
		// translate their location based on margins
		svg.append("g")
			.attr("class", "guide")
		.append("line")
			.attr("x1", circle.attr("cx"))
			.attr("x2", circle.attr("cx"))
			.attr("y1", +circle.attr("cy") + 26)
			.attr("y2", h - margin.t - margin.b)
			.attr("transform", "translate(40,20)")
			.style("stroke", circle.style("fill"))
			.transition().delay(200).duration(400).styleTween("opacity", 
						function() { return d3.interpolate(0, .5); })

		svg.append("g")
			.attr("class", "guide")
		.append("line")
			.attr("x1", +circle.attr("cx") - 16)
			.attr("x2", 0)
			.attr("y1", circle.attr("cy"))
			.attr("y2", circle.attr("cy"))
			.attr("transform", "translate(40,30)")
			.style("stroke", circle.style("fill"))
			.transition().delay(200).duration(400).styleTween("opacity", 
						function() { return d3.interpolate(0, .5); });

	// function to move mouseover item to front of SVG stage, in case
	// another bubble overlaps it
		d3.selection.prototype.moveToFront = function() { 
		  return this.each(function() { 
			this.parentNode.appendChild(this); 
		  }); 
		};

	// skip this functionality for IE9, which doesn't like it
		if (!$.browser.msie) {
			circle.moveToFront();	
			}
	};
	// what happens when we leave a bubble?
	var mouseOff = function() {
		var circle = d3.select(this);

		// go back to original size and opacity
		circle.transition()

		.duration(800).style("opacity", .5)
		.attr("r", 8).ease("elastic");

		// fade out guide lines, then remove them
		d3.selectAll(".guide").transition().duration(100).styleTween("opacity", 
						function() { return d3.interpolate(.5, 0); })
			.remove()
	};

	// run the mouseon/out functions
	circles.on("mouseover", mouseOn);
	circles.on("mouseout", mouseOff);

	// tooltips (using jQuery plugin tipsy)
	circles.append("title")
			.text(function(d) {  var ss= [d.name,d.position, d.height_cm+'(cm)',d.weight+'(pd)'];
							return ss; })
			.attr('class','labelText')

//	$(".circles").tipsy({ gravity: 's', });

	// the position legend color guide
	var legend = svg.selectAll("rect")
			.data(positions)
		.enter().append("rect")
		.attr({
		  x: function(d, i) { return (20 + i*20); },
		  y: h,
		  width: 15,
		  height: 7
		})
		.style("fill", function(d) { return color(d); });

	// legend labels	
		svg.selectAll("text")
			.data(positions)
		.enter().append("text")
		.attr({
		x: function(d, i) { return (20 + i*20); },
		y: h + 24,
		})
		.text(function(d) { return d; });

	svg.selectAll("title_text")
	  .data(["Click legend to","show/hide Pos:"])
	  .enter()
	  .append("text")
		.attr("x", '92%')
		.attr("y", function (d, i) { return 25 + i * 14; })
		.style("font-family", "sans-serif")
		.style("font-size", "10px")
		.style("color", "Black")
		.text(function (d) { return d; });


	// the status legend color guide
	var legend1 = svg.selectAll("rect")
			.data(status)
		.enter().append("rect")
		.attr({
		  x: w ,
		  y: function(d, i) { return (40 + i*40); },
		  width: 15,
		  height: 7
		})
		.style("fill", function(d) { return color(d); });

	// legend labels	
		svg.selectAll("text")
			.data(status)
		.enter().append("text")
		.attr({
		x: w + 24,
		y: function(d, i) { return (40 + i*40); },
		})
		.text(function(d) { return d; });

/*	svg.selectAll("title_text")
	  .data(["Click legend to","show/hide Pos:"])
	  .enter()
	  .append("text")
		.attr("x", '92%')
		.attr("y", function (d, i) { return 25 + i * 14; })
		.style("font-family", "sans-serif")
		.style("font-size", "10px")
		.style("color", "Black")
		.text(function (d) { return d; });
*/
/*

	var filterValues = dimple.getUniqueValues(data, "position");
	myLegend.shapes.selectAll("rect")
		.on("click", function (e) {
		var hide = false;
		var newFilters = [];
		filterValues.forEach(function (f) {
			if (f === e.aggField.slice(-1)[0]) {
				hide = true;
			} else {
				newFilters.push(f);
			}
		});

	if (hide) {
		d3.select(this).style("opacity", 0.2);
	} else {
		newFilters.push(e.aggField.slice(-1)[0]);
		d3.select(this).style("opacity", 0.8);
	}

*/
	// draw axes and axis labels
	svg.append("g")
		.attr("class", "x axis")
		.attr("transform", "translate(" + margin.l + "," + (h - 60 + margin.t) + ")")
		.call(xAxis);

	svg.append("g")
		.attr("class", "y axis")
		.attr("transform", "translate(" + margin.l + "," + margin.t + ")")
		.call(yAxis);

	svg.append("text")
		.attr("class", "x label")
		.attr("text-anchor", "end")
		.attr("x", w + 50)
		.attr("y", h - margin.t - 5)
		.text("weight (pd)");

	svg.append("text")
		.attr("class", "y label")
		.attr("text-anchor", "end")
		.attr("x", -20)
		.attr("y", 45)
		.attr("dy", ".75em")
		.attr("transform", "rotate(-90)")
		.text("height (cm)");
	};

}
