
      function plot5(data) {
		var svg = dimple.newSvg("#chart",'80%', '650');

        var offense = dimple.filterData(data, "off_def", ["G", "OT", "C", "QB", "WR", "TE" ,"RB"]);
		var defense = dimple.filterData(data, "off_def", ["DT", "DE", "CB", "DB", "OLB", "MLB", "SS", "NT", "FS" ]);
		//dimple.filterData(data, "off_def",['offense','defense','unknown'])

        // Creating the chart
			   
		xMin = d3.min(data, function (d) { return d.weight; })  ;
		xMax = d3.max(data, function (d) { return d.weight; }) ;
		yMin = d3.min(data, function (d) { return d.height_cm; }) ;
		yMax = d3.max(data, function (d) { return convert_to_cm(d.height); }) ;

		function convert_to_cm(hh) {   
			if ( hh.length == 5) { 
				return 30.48*parseInt(hh[0]) + 2.54*parseInt(hh[2]) }
			else if(hh.length == 6) { 
				return 30.48*parseInt(hh[0]) + 2.54*parseInt(hh[2]+hh[3]) }
	
			else{ console.error("invalid height")	
				return 0	}
		}


		f1(data)
		function f1(data) {
		
		$('#getJ').click(function() { 

											svg.remove()
											$("#char").text('') })
		
		var myChart = new dimple.chart(svg, data);
		myChart.setBounds('12%','10%', '80%', '75%')
		var x = myChart.addMeasureAxis("x", "weight")
		x.showGridlines = true;
		x.overrideMax = xMax
		x.overrideMin = xMin


		var y = myChart.addCategoryAxis("y", ["height_cm"]);
		y.addOrderRule('height_cm')

		var s
		if ($('#off_def').val() == 'def') {
		s = myChart.addSeries(["pid","name","team","height_cm","position"], dimple.plot.bubble);
		}
		else {
		s = myChart.addSeries(["pid","name","team","height_cm","position","off_def"], dimple.plot.bubble);
		}
		
		s.lineWeight = 8;
		s.lineMarkers = true;


		var myLegend = myChart.addLegend('95%', '10%', 60, '85%', "Right");
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
		
		var filterValues
		if ($('#off_def').val() == 'def') {
			filterValues = dimple.getUniqueValues(data, "position");
		}
		else {
			filterValues = dimple.getUniqueValues(data, "off_def");
		}

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
		if ($('#off_def').val() == 'def') {
			myChart.data = dimple.filterData(data, "position", filterValues);
		}
		else {
			myChart.data = dimple.filterData(data, "off_def", filterValues);
		}		

		myChart.draw(800);
		});
		

}		
		
   };


