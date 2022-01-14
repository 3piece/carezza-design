odoo.define('carezza_custom_access_inventory.portal_shipdate', function (require) {
	"use strict";
	
	$("#operation_type").change(function(){		
		var selValue = $(this).val();
		$("#operation_type_value").val(selValue)
	});


	$(".ship-date").change(function(){
          var element = $(this).parent().next().next().children()
          element[0].classList.add("dislay-block");
          element[0].classList.remove('dislay-none')
 	  element[1].classList.remove("dislay-block");
          element[1].classList.add('dislay-none')
	});

	$(document).ready(function(){
	  $(".btn-submit").click(function(){
	     $(this).removeClass("btn-primary");
	    $(this).addClass("btn-success"); 
	    $(this).next().addClass('dislay-block') 
            $(this).next().removeClass('dislay-none') 
            $(this).addClass('dislay-none')
	  });
	});

});


