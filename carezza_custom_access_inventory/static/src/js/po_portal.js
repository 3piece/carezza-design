odoo.define('carezza_custom_access_inventory.portal_shipdate', function (require) {
	"use strict";

	function empty(){
	    console.log("empty");
	}

//    delete window.ready_to_submit;
	function ready_to_submit(element){
	    console.log("Ready");
//	    console.log(element);
	    element.find(".attachment-excel").removeClass("text-submitted")
//	    element.closest(".attachment-excel").removeClass("text-submitted")
	}

//    delete sending;
    function sending(element){
	    console.log("sending");
//	    console.log(element);
//	    element.find(".attachment-excel").val(null);
	    element.find(".attachment-excel").addClass("text-submitted");
//	    element.find(".attachment-excel").value = '';

	}

//    delete window.sent;
    function sent(){
	    console.log("sent");
	}
//
	$("#operation_type").change(function(){
		var selValue = $(this).val();
		$("#operation_type_value").val(selValue)
	});

//	$(".ship-date").off("change");

	$(".ship-date").change(function(){
          var element = $(this).parent().next().next().children();
          element[0].classList.add("pointer-visible");
          element[0].classList.remove('pointer-none');

          element[1].classList.add('display-none');
          element[1].classList.remove('display-block');

          ready_to_submit($(this).parent().parent());
	});

//	$(".attachment-excel").off("change");

	$(".attachment-excel").change(function(){
          var element = $(this).parent().next().children();
          element[0].classList.add("pointer-visible");
          element[0].classList.remove('pointer-none');

          element[1].classList.add('display-none');
          element[1].classList.remove('display-block');

          ready_to_submit($(this).parent());
	});

	$(document).ready(function(){

//    	$(".btn-submit").off("click");

        $(".btn-submit").click(function(){
                $(this).addClass('pointer-none');
                var a =  $(this).next();
                $(this).next().addClass('display-block');
                $(this).next().removeClass('display-none');
                setTimeout(function() {
                    $("#attachment").val(null);
                }, 2000);
                sending($(this).parent().parent());
        });

        empty();


	});

});


