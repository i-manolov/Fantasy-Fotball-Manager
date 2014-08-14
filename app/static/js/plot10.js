
	function plot10(data){

	//alert(data)
	//get the data from the json
	//var P_TE=[Active]
	//alert(P_TE)
	//var P-
	

    // Set up the plot window.
    var margin = 40;
    var w = 700 - 2 * margin, h = 500 - 2 * margin;

    var svg = d3.select("#chartContainer").append("svg")
				.attr("width", w + 2 * margin)
				.attr("height", h + 2 * margin)
					.append("svg:g")
					.attr("transform", "translate(" + margin + ", " + margin + ")");

    // The colorbar.
    var color = d3.scale.quantize()
                  .range(["aliceblue","antiquewhite","aqua","aquamarine","black","blue",
			"blueviolet","brown","burlywood","cadetblue","chartreuse","chocolate",
			,"crymson","cyan","darkcyan","darkgoldenrod","darkolivegreen",
			"darkorange","darkorchid","darkred","darkslateblue","deeppink",
			"deepskyblue","dimgrey","dodgerblue4","firebrick","gold"])
                  .domain([1,27]);

    // Axes scaling functions.
    var xscale = d3.scale.linear().range([0, w]);
    var yscale = d3.scale.linear().range([h, 0]);


    // The axes objects themselves.
    var xaxis = d3.svg.axis().scale(xscale).ticks(12);
    var yaxis = d3.svg.axis().scale(yscale).ticks(12).orient("left");

    svg.append("svg:g").attr("class", "x axis")
		   .attr('fill', 'blue')
                       .attr("transform", "translate(0, " + h + ")");
    svg.append("svg:g").attr("class", "y axis")
		   .attr('fill', 'blue');

    // Show the information about a particular point.
    var show_info = function (d) {
        d3.select("#result").text("Player "+d.name + " position  "+ d.position
        + " team "+d.team + " ( weight " + d.weight + " pd, height " + d.height + ").");
    };
	
	// convert position to color
	var _all_pos = { "TE":1, "T":2, "OG":3,"OL":4,"QB":5,"NT":6,"OLB":7,"G":8,"UNK":9,
	"RB":10,"MLB":11,"OT":12,"S":13,"WR":14,"LS":15,"SAF":16,"P":17,"DB":18,
	"K":19,"CB":20,"C":21,"FB":22,"LB":23,"ILB":24,"DT":25,"DE":26,"FS":27 };
	var _all_sta = {"Unknown":100, "Active":101, "InjuredReseve":102, "PUP":103};

	function position_color(d) { 
		for (var i in _all_pos) {
			if (i==d) { return _all_pos[i] }	
		}
	}
	// add legend 

/*	 var legend = svg.selectAll(".legend")
	      .data(color.domain())
	    .enter().append("g")
	      .attr("class", "legend")
	      .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

	  legend.append("rect")
	      .attr("x", width - 18)
	      .attr("width", 18)
	      .attr("height", 18)
	      .style("fill", color);

	  legend.append("text")
	      .attr("x", width - 24)
	      .attr("y", 9)
	      .attr("dy", ".35em")
	      .style("text-anchor", "end")
	      .text(function(d) { return d.position; });
*/
	/*var myLegend = d3.select('#chart').append('svg')
		  .attr('class','legend')
		  .attr('width', 4)
		  .attr('height', 4)
		  .selectAll('g')
			.data(data, function(d) {return d.position})
			.enter().append('g')('tranform', function(d,i) { return 'translate(0,'+i*10+')';})

	mylegend.append
	*/				

	//convert d.heigh in cm
	function convert_to_cm(hh) {   
		if ( hh.length == 5) { 
			return 30.48*parseInt(hh[0]) + 2.54*parseInt(hh[2]) }
		else if(hh.length == 6) { 
			return 30.48*parseInt(hh[0]) + 2.54*parseInt(hh[2]+hh[3]) }
	
		else{ console.error("invalid height")	
			return 0	}
	}
	callback(data);


    // Load the data.
        function callback(data) { 
        // Rescale the axes.
	xMax = d3.min(data, function (d) { return d.weight; }) - 1 ;
	xMin = d3.max(data, function (d) { return d.weight; }) + 1 ;
	yMin = d3.min(data, function (d) { return convert_to_cm(d.height); }) - 1 ;
	yMax = d3.max(data, function (d) { return convert_to_cm(d.height); }) + 1 ;
    xscale.domain([xMin , xMax]);
	yscale.domain([yMax , yMin]);

    // Display the axes.
	
	svg.select(".x.axis").call(xaxis);
	svg.select(".y.axis").call(yaxis);
	// Insert the data points.
	svg.selectAll("circle").data(data).enter()
		.append("circle")
		.attr("id", function (d) { return d.id; })
		.attr("cy", function (d) {  if (typeof d.height == 'string') {
										return yscale(convert_to_cm(d.height));}
									else {
										return 0;} })
		.attr("cx", function (d) { return xscale(d.weight); })
		.attr("r", function (d) { return 3; })
		.attr("fill", function (d) { return color(position_color(d.position)); })
		.on("mousedown", show_info)

        };


/*		var legend = svg.selectAll(".legend")
	      	.data(color.domain())
	    	.enter().append("g")
	      	.attr("class", "legend")
	      	.attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

		legend.append("rect")
				  .attr("x", width - 18)
				  .attr("width", 18)
				  .attr("height", 18)
				  .style("fill", color);

		svg.call(legend)
*/


	}

