$(document).ready(function(){
	$(function() {
		$('#myCarousel').carousel();	
		
	});
	
	$('.contributions').children().each(function() {
		var country = $(this).attr('id');
		var flag = '../static/imgs/'+ country +'.jpg';

		$(this).prepend($('<img/>', {src:flag}).addClass('flags'));
		
	});
	
	$('.countryImage').click(function() {
			var countryID = $(this).attr('id');
			$('#contributors').children().not('#'+countryID).hide();
		
			if($('#contributors').find('#'+countryID).text().trim().length>0)	
			{
				$('#contributors').find('#'+countryID).show();
				$('#contributors').find('#'+countryID).find('.desc').show().css({display:"block"});
				$('#contributors').find('#'+countryID).find('.location').show();
				$('#contributors').find('#'+countryID).find('.imgs').show().css({display:"block"});
			}
			else
			{
				$('#contributors').children().find('.desc').hide();
				$('#contributors').children().find('.imgs').hide();
				$('#contributors').children().find('.location').hide();
				$('#contributors').children().show();
			}
		
			$('.countryImage').css({fill: "FFFFFF"});
			$(this).css({fill: "34495E"});
		});
	
	$('#button').click(function() {
		$('#contributors').children().show();
		$('#contributors').find('.desc').hide();
		$('#contributors').find('.location').hide();
		$('#contributors').find('.imgs').hide();
		$('.countryImage').css({fill: "FFFFFF"});
	});
	
	$('.flags').click(function() {
		var countryID = $(this).attr('id');
			$('#contributors').children().not('#'+countryID).hide();
			$('#contributors').find('#'+countryID).show();
			$('#contributors').find('#'+countryID).find('.desc').show().css({display:"block"});
			$('#contributors').find('#'+countryID).find('.location').show();
			$('#contributors').find('#'+countryID).find('.imgs').show().css({display:"block"});
			$('.countryImage').css({fill: "FFFFFF"});
			$('#'+countryID).css({fill: "34495E"});
	});

	
});