
	function plot11(){

	
        // Set up the plot window.
        var margin = 40;
        var w = 700 - 2 * margin, h = 500 - 2 * margin;
        var svg = d3.select("#chart_div1").append("svg")
                        .attr("width", w + 2 * margin)
                        .attr("height", h + 2 * margin)
                    .append("svg:g")
                        .attr("transform", "translate(" + margin + ", " + margin + ")");

        // The colorbar.
        var color = d3.scale.quantize()
                      .range(["blue","green","red","yelow"])
                      .domain([1,27]);

        // Axes scaling functions.
        var xscale = d3.scale.linear().range([0, w])
					.domain([150,215]);
        var yscale = d3.scale.linear().range([h, 0])
					.domain([150,380]);

        // The axes objects themselves.
        var xaxis = d3.svg.axis().scale(xscale).ticks(12);
        var yaxis = d3.svg.axis().scale(yscale).ticks(12).orient("left");

        svg.append("svg:g").attr("class", "x axis")
                           .attr("transform", "translate(0, " + h + ")");
        svg.append("svg:g").attr("class", "y axis");

        // Show the information about a particular point.
        var show_info = function (d) {
            d3.select("#paragraph").text("This is player "+d.first_name+" " + d.last_name + " with id# "+ d.id 
	        + "( weight " + d.weight + "pd, height " + d.height + ").");
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
	//convert d.heigh in cm
	function convert_to_cm(hh) {   
					if ( hh.length == 5) { 
						return 30.48*parseInt(hh[0]) + 2.54*parseInt(hh[2]) }
					else if(hh.length == 6) { 
						return 30.48*parseInt(hh[0]) + 2.54*parseInt(hh[2]+hh[3]) }
				
					else{ console.error("invalid height")	
						return 0	}
	}
	
        // Load the data.
        var callback = function (data) { 
            // Rescale the axes.
	//color.domain(d3.min(data,function(d) {
/*            xscale.domain([d3.min(data, function (d) { return d.height; })   ,
                           d3.max(data, function (d) { return d.height; }) + 1]);
            yscale.domain([d3.min(data, function (d) { return d.weight; })   ,
                           d3.max(data, function (d) { return d.weight; }) + 1]);

			dd= d3.min(data, function (d) { return d.height; });
			alert(dd)
*/       // Display the axes.
            svg.select(".x.axis").call(xaxis);
            svg.select(".y.axis").call(yaxis);
            // Insert the data points.
           svg.selectAll("circle").data(data).enter()
                .append("circle")
                    .attr("id", function (d) { return d.id; })
                    .attr("cx", function (d) {  if (typeof d.height == 'string') {
						 return xscale(convert_to_cm(d.height));}
						else {return 0;} })
                    .attr("cy", function (d) { return yscale(d.weight); })
                    .attr("r", function (d) { return 3; })
                    .attr("fill", function (d) { return color(position_color(d.position)); })
                    .on("mousedown", show_info);
        };

        d3.tsv("static/js/mydata.tsv", callback);

	//callback(data);

	}

