odoo.define('carezza_custom_access_inventory.portal_shipdate', function (require) {
	"use strict";
	
	$("#operation_type").change(function(){		
		var selValue = $(this).val();
		$("#operation_type_value").val(selValue)
	});


	$(".ship-date").change(function(){
          var element = $(this).parent().next().next().children()
	  debugger;
          element[0].classList.add("pointer-visible");
          element[0].classList.remove('pointer-none')

          element[1].classList.add('display-none')
          element[1].classList.remove('display-block')

	});

	$(".attachment-excel").change(function(){
          var element = $(this).parent().next().children()
	  debugger;
          element[0].classList.add("pointer-visible");
          element[0].classList.remove('pointer-none')

          element[1].classList.add('display-none')
          element[1].classList.remove('display-block')

	});

	$(document).ready(function(){
	  $(".btn-submit").click(function(){
            $(this).addClass('pointer-none')
	    debugger
            var a =  $(this).next()
	    $(this).next().addClass('display-block')	
            $(this).next().removeClass('display-none')
		 
	  });


	});


});


