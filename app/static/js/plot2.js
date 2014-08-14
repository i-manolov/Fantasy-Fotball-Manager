function top_players(data,val) {
	
		$('#graph1').click(function() { 
			svg.remove()
		})
		var svg = dimple.newSvg("#graph", 590, 400);

		var myChart = new dimple.chart(svg, data);
		myChart.setBounds(60, 30, 420, 330)
		var x = myChart.addCategoryAxis("x", ["name","period"]);
		x.showGridlines = true;
		x.addOrderRule(val);
		var y = myChart.addMeasureAxis("y", val);
		y.tickFormat = "d";
		var s = myChart.addSeries(["team","period"], dimple.plot.bar);
		s.lineWeight = 100;
		s.lineMarkers = true;
		var myLegend = myChart.addLegend(540, 100, 60, 300, "Right");
		myChart.draw();
		myChart.legends = [];
		svg.selectAll("title_text")
		  .data(["Click legend to","show/hide owners:"])
		  .enter()
		  .append("text")
			.attr("x", 499)
			.attr("y", function (d, i) { return 80 + i * 14; })
			.style("font-family", "sans-serif")
			.style("font-size", "10px")
			.style("color", "Black")
			.text(function (d) { return d; });

		var filterValues = dimple.getUniqueValues(data, "period");
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
			filterValues = newFilters;
			myChart.data = dimple.filterData(data, "period", filterValues);
			myChart.draw(800);
			$('h1').click(function() { svg.remove() });
	});



}

