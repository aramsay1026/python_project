


$( document ).ready(function() {
    console.log( "ready!" );

    $('#id01').hide();
    $('#id02').hide();
    $('#id03').hide();


  	$("button#login_reg").click(function(){
      $(this).hide();
      $('#id01').show();
    });
 

    $("button#log_close").click(function(){
      $("button#login_reg").show();
      $('#id01').hide();
      $('#id02').hide();
    });

    $("a#reg_link").click(function(){
      $("button#login_reg").show();
      $('#id02').show();
      $('#id01').hide();
     
    });

    $("button#reg_close").click(function(){
      $("button#login_reg").show();
      $('#id02').hide();
      $('#id01').hide();
    });

    $("#reg_btn").click(function(){
    	$('#id02').hide();
    	$("#id03").show();
    });

    $(".cancelbtn").click(function(){
    	$("button#login_reg").show();
    	$('#id01').hide();
    	$('#id02').hide();
    });

    $("#type_cancelbtn").click(function(){
    	$('#id03').hide();
    });

    $("#first").change(function(){
    	if($(this).prop('checked')){
    		$("#append_1").html("<p class='warn' id='1'>Volunteers must be licensed and have access to a reliable vehicle</p>");
    		$("#1.warn").show();
    		$("#2.warn").hide();
    		$("#3.warn").hide();
      }
      else{
          $("#append_1").html(" ");
          $("#2.warn").hide();
          $("#3.warn").hide();
          $("#1.warn").hide();
      }
    });

    $("#second").change(function(){
    	 if($(this).prop('checked')){
      		$("#append_2").html("<p class='warn' id='2'>All prepared food must meet USDA standards for proper food safety and handling</p>");
      		$("#2.warn").show();
      		$("#3.warn").hide();
      		$("#1.warn").hide();
      }
        else{
          $("#append_2").html(" ");
          $("#2.warn").hide();
          $("#3.warn").hide();
          $("#1.warn").hide();
      }
    });

    $("#last").change(function(){
    	if($(this).prop('checked')){
    		$("#append_3").html("<p class='warn' id='3'>Potential Food Banks must be verified as legal non-profit entities by our team</p>");
    		$("#3.warn").show();
    		$("#1.warn").hide();
    		$("#2.warn").hide();
      }
      else{
          $("#append_3").html(" ");
          $("#2.warn").hide();
          $("#3.warn").hide();
          $("#1.warn").hide();
      }
    });

    $('input[type="checkbox"]').on('change', function() {
   	$(this).siblings('input[type="checkbox"]').prop('checked', false);
});

});	





