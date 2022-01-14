odoo.define('carezza_custom_access_inventory.portal_shipdate', function (require) {
	"use strict";
	
	$("#operation_type").change(function(){
		
		var selValue = $(this).val();
		debugger;
		$("#operation_type_value").val(selValue)

	});


	$(document).ready(function(){
	  $(".btn-submit").click(function(){
	     $(this).removeClass("btn-primary");
	    debugger;
	    $(this).addClass("btn-success"); 
	     var a = $(this).next()
	    $(this).next().append('<p>Transfers submitted</p>');    
	  });
	});

});


