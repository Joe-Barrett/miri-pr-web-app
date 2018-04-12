$(document).ready(function () {
	$(function () {
		$('.carousel').carousel();
	});

	$('.countryImage').click(function () {
		var country = $(this).data('country');
		$('#contributions .contribution').not(`[data-country="${country}"]`).hide();

		if ($('#contributions').find(`[data-country="${country}"]`).length > 0) {
			$(`#contributions .contribution[data-country="${country}"]`).show();
			$(`#contributions .contribution[data-country="${country}"] .details`).show();
		} else {
			$('#contributions .details').hide();
			$('#contributions .contribution').show();
		}

		$('.countryImage').css({
			fill: "FFFFFF"
		});
		$(this).css({
			fill: "34495E"
		});
	});
	
	
	$('.home').click(function () {
		$('#contributions .contribution').show();
		$('#contributions .details').hide();
		$('.countryImage').css({
			fill: "FFFFFF"
		});
	});

	$('#button').click(function () {
		$('#contributions .contribution').show();
		$('#contributions .details').hide();
		$('.countryImage').css({
			fill: "FFFFFF"
		});
	});

	$('.handle').click(function () {
		var country = $(this).parent('.contribution').data('country');

		$('#contributions .contribution').not(`[data-country="${country}"]`).hide();
		$(`#contributions .contribution[data-country="${country}"]`).show();
		$(`#contributions .contribution[data-country="${country}"] .details`).show();
		$('.countryImage').css({
			fill: "FFFFFF"
		});
		$(`.countryImage[data-country=${country}]`).css({
			fill: "34495E"
		});
	});


});