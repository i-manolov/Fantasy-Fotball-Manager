
function m1() { 
	//alert("m1")
	$("document").ready(function() {
	
	$('#chart_divd1').css({'height':'100px', 'background-color':'mintcream'})
	$('#choose_p').css({'float':'left', 'color':'navy'})
	$('#choose_s').css({ 'position':'relative','top':'0px','left':'100px','color':'navy'})
	;})
  $(function() {
	
    var submit_form = function(e) {
      $.getJSON($SCRIPT_ROOT + '/_getJson', {
				pos: $('select[name="a1"]').val() ,
				pos: $('select[name="a2"]').val() ,
				pos: $('select[name="a3"]').val() ,
				pos: $('select[name="a4"]').val() ,
				pos: $('select[name="a5"]').val() ,
				pos: $('select[name="a6"]').val() ,
				pos: $('select[name="a7"]').val() ,
				pos: $('select[name="a8"]').val() ,
				pos: $('select[name="a9"]').val() ,
				pos: $('select[name="a10"]').val() ,
				pos: $('select[name="a11"]').val() ,
				pos: $('select[name="a12"]').val() ,
				pos: $('select[name="a13"]').val() ,
				pos: $('select[name="a14"]').val() ,
				pos: $('select[name="a15"]').val() ,
				pos: $('select[name="a16"]').val() ,
				pos: $('select[name="a17"]').val() ,
				pos: $('select[name="a18"]').val() ,
				pos: $('select[name="a19"]').val() ,
				pos: $('select[name="a20"]').val() ,
				pos: $('select[name="a21"]').val() ,
				pos: $('select[name="a22"]').val() ,
				pos: $('select[name="a23"]').val() ,
				pos: $('select[name="a24"]').val() ,
				pos: $('select[name="a25"]').val() ,
				pos: $('select[name="a26"]').val() ,
				pos: $('select[name="a27"]').val() ,
				pos: $('select[name="a28"]').val() ,
				sta: $('select[name="b1"]').val() ,
				sta: $('select[name="b2"]').val() ,
				sta: $('select[name="b3"]').val() ,
				sta: $('select[name="b4"]').val() ,
				sta: $('select[name="b5"]').val() 

      }, function(data) { //alert('LLLLLLLLLLLLL')
	plot10(data)	
      });
      //return false;
    };

    $('a#getJ').bind('click', submit_form);

    $('input[type=text]').bind('keydown', function(e) {
      if (e.keyCode == 13) {
        submit_form(e);
      }
    });

    $('input[name=a]').focus();
  });
/*var p = $('#Position').val() || [] ;
			var s = $('#Status').val() || [] ;
				//alert (p)
				//alert(s)
			
			function getPosVal()
			{
				var pv = $('#Position').val() || [] ; 
				return pv;
			}

			function getStaVal()
			{
				var sv = $('#Status').val() || [] ; 
				return sv;
			}
*/
}




