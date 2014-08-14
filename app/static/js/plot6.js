
      function plot6(data) {
		var svg = dimple.newSvg("#chart",'80%', '650');

        var offense = dimple.filterData(data, "position", ["G", "T", "C", "QB", "WR", "TE" ,"RB", "FB", "OL"]);
		var defense = dimple.filterData(data, "position", ["NT", "DT", "DE", "DB", "CB", "OLB", "MLB", "SS","FS" ]);
		//alert(offense)
        // Creating the chart
			   
		xMin = d3.min(data, function (d) { return d.weight; })  ;
		xMax = d3.max(data, function (d) { return d.weight; }) ;
		yMin = d3.min(data, function (d) { return convert_to_cm(d.height); }) - 20 ;
		yMax = d3.max(data, function (d) { return convert_to_cm(d.height); }) + 5 ;
		//alert(xMin+'l'+xMax)

		function convert_to_cm(hh) {   
			if ( hh.length == 5) { 
				return 30.48*parseInt(hh[0]) + 2.54*parseInt(hh[2]) }
			else if(hh.length == 6) { 
				return 30.48*parseInt(hh[0]) + 2.54*parseInt(hh[2]+hh[3]) }
	
			else{ console.error("invalid height")	
				return 0	}
		}

		$('#off_def').change (function() { 
			if ($('#off_def').val() == "off") {	alert('if offen case '+offense.length); 
			f1(offense)
			}
			else if ($('#off_def').val() == 'def') {alert('if defen '+defense.length)
				f1(defense)
			}	
			else { f1(data) }		
		})

		f1(data)
		function f1(data) {

	    x.domain(d3.extent(data, function(d) { return d.weight; })).nice();
	  	y.domain(d3.extent(data, function(d) { return d.height_cm; })).nice();

		var myChart = new dimple.chart(svg, data);
		myChart.setBounds('10%','10%', '82%', '75%')
		var x = myChart.addMeasureAxis("x", "weight")//, null);
		x.showGridlines = true;
		//x.overrideMax = xMax
		//x.overrideMin = xMin


		var y = myChart.addCategoryAxis("y", ["height_cm"]);
		y.addOrderRule('height(cm)')
		var s = myChart.addSeries(["name","team","height_cm","position"], dimple.plot.bubble);
		s.lineWeight = 4;
		s.lineMarkers = true;


		var myLegend = myChart.addLegend('94%', '10%', 60, '85%', "Right");
		//myLegend.addLegend(
		myChart.draw(800);

		myChart.legends = [];

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
		


		var filterValues = dimple.getUniqueValues(data, "position");
		myLegend.shapes.selectAll("rect")
			.on("click", function del(e) {
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

		filterValues = newFilters;
		myChart.data = dimple.filterData(data, "position", filterValues);
		myChart.draw(800);
		});
		

}		
		
   };


