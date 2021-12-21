odoo.define('carezza_custom_access_inventory.portal_shipdate', function (require) {
	"use strict";
	
	$("#operation_type").change(function(){
		
		var selValue = $(this).val();
		debugger;
		$("#operation_type_value").val(selValue)

	});

});


