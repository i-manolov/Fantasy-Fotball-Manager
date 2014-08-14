
function m3() 
	{ 

		$("document").ready(function() 
		{	
			$('#char').text('OFFENSE')
			$('#char').css({'color': 'red', 'font':'sanserif','font-size':'20px','margin-top':'15 px', 'margin-left':'40%'})
			$.getJSON($SCRIPT_ROOT + '/_getJson', 
					{  
						pos1 : "G",
						pos2 : "TE",
						pos3 : "T",
						pos4 : "C",
						pos5 : "QB",
						pos6 : "WR",
						sta1 : "All",
					},
					function(data) 	
					{ 	//alert(data.length)	
						plot8(data)
			  		});

				//DEFENSE
			$.getJSON	($SCRIPT_ROOT + '/_getJson', 
					{ 
						pos1 : "NT",
						pos2 : "DT",
						pos3 : "DE",
						pos4 : "DB",
						pos5 : "CB",
						pos6 : "OLB",
						pos7 : "MLB",
						pos8 : "SS",
						pos9 : "FS",
						sta1 : "All"
				
					},
					function(data) 	
					{ 		
						plot8(data)
			  		});





			//submit_form()
			$('table').css({'width':'200px'})
			$("#td1").css({'height':'20px','max-width':'100px', 'oveflow':'hidden', 'background':'green'});
			$('#td1').bind('click', function() 
			{
				if ($('#chart_divd1').is(':visible')) 
				{	
					$('#chart_divd1').hide()
					
				} 
			})
			
			$('#td2').css({'height':'20px','width':'100px', 'background-color':'lightblue'})
			$('#td2').bind('click', function() { if ($('#chart_divd1').not(':visible')) {$('#chart_divd1').show()} })
			$('.p1').css({'color':'Blue', 'font-size':'15px', 'position':'relative', 'left': '-66px'})
			$('#chart_divd1').css({'background-color':'mintcream', 'height': '120px'})
			$('#choose_p').css({'float':'left'})
			$('#choose_s').css({ 'position':'relative','top':'0px','left':'40px'})
			$('#choose_y').css({ 'position':'relative','top':'-90px','left':'280px'})
			$('#legend').css({ 'position':'relative','top':'-130px','left':'390px'})
			$('#getJ').css({ 'position':'relative','margin':'40px,0px','top':'10px','left':'40px'})
			//$("#chart_divd1").bind('click', submit_form)
	
		}); 
		$(function f1() 
		{
			

			var submit_form = function submit_form(e)
		 	{
				
		
			  	$.getJSON($SCRIPT_ROOT + '/_getJson', 
					{
						pos1: $('select option[name="a1"]:selected').val() ,
						pos2: $('select option[name="a2"]:selected').val() ,
						pos3: $('select option[name="a3"]:selected').val() ,
						pos4: $('select option[name="a4"]:selected').val() ,
						pos5: $('select option[name="a5"]:selected').val() ,
						pos6: $('select option[name="a6"]:selected').val() ,
						pos7: $('select option[name="a7"]:selected').val() ,
						pos8: $('select option[name="a8"]:selected').val() ,
						pos9: $('select option[name="a9"]:selected').val() ,
						pos10: $('select option[name="a10"]:selected').val() ,
						pos11: $('select option[name="a11"]:selected').val() ,
						pos12: $('select option[name="a12"]:selected').val() ,
						pos13: $('select option[name="a13"]:selected').val() ,
						pos14: $('select option[name="a14"]:selected').val() ,
						pos15: $('select option[name="a15"]:selected').val() ,
						pos16: $('select option[name="a16"]:selected').val() ,
						pos17: $('select option[name="a17"]:selected').val() ,
						pos18: $('select option[name="a18"]:selected').val() ,
						pos19: $('select option[name="a19"]:selected').val() ,
						pos20: $('select option[name="a20"]:selected').val() ,
						pos21: $('select option[name="a21"]:selected').val() ,
						pos22: $('select option[name="a22"]:selected').val() ,
						pos23: $('select option[name="a23"]:selected').val() ,
						pos24: $('select option[name="a24"]:selected').val() ,
						pos25: $('select option[name="a25"]:selected').val() ,
						pos26: $('select option[name="a26"]:selected').val() ,
						pos27: $('select option[name="a27"]:selected').val() ,
						pos28: $('select option[name="a28"]:selected').val() ,
						sta1: $('select option[name="b1"]:selected').val() ,
						sta2: $('select option[name="b2"]:selected').val() ,
						sta3: $('select option[name="b3"]:selected').val() ,
						sta4: $('select option[name="b4"]:selected').val() ,
						sta5: $('select option[name="b5"]:selected').val() ,
						sta6: $('select option[name="b6"]:selected').val() ,
						sey1: $('select option[name="c1"]:selected').val() ,
						sey2: $('select option[name="c2"]:selected').val() ,
						sey3: $('select option[name="c3"]:selected').val() ,
						sey4: $('select option[name="c4"]:selected').val() ,
						sey5: $('select option[name="c5"]:selected').val() ,
						sey6: $('select option[name="c6"]:selected').val() 
		  				},
						function (data) 	
						{ 
							p =$('#Position').val() || [];
							s = $('#Status').val() || [];
//alert(p+'|  |'+s)
//alert(data.length)
//plot7(p, s, data)	
							plot5(data)
		  				}
					);
			}
 			
//			$('#off_def').bind('click',function() { 

			$('a#getJ').bind('click', submit_form);


			$('select .position:selected').bind('keydown', function(e) 
			{
		  		if (e.keyCode == 13) 
				{
	    			submit_form(e);
	  			}
			});

			$('select #Position').focus();
		});

	}
		

