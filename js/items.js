$(function() {
	//set color to selected option
	var roledata = "";
	$("div#items #header").each(function() {
		roledata = $(this).find("form select").val().split('|');
		$(this).css('background-color',roledata[1]);
	});
	//$("div#items #content").css('background-color',roledata[1]);
	
	//change color and update role on select option change
	$("div#items div#header form select").change(function() {
		//change color
		var roledata = $(this).val().split('|');
		$(this).parent().parent().css('background-color',roledata[1]);
		//$(this).parent().parent().parent().find("#content").css('background-color',roledata[1]);
		//send ajax update to python (to add to db)
		var itemid = $(this).parent().parent().parent().attr('id');
		itemid = itemid.split('-')
		$.ajax({
			type: "POST",
			url: "viewtools.py",
			data: "roleid="+roledata[0]+"&itemid="+itemid[1]+"&do=setrole"
		});
	});
	//show content and permalink on mouseover of item header
	$("div#items div#header").hover(function() {
		$(this).parent().find('div#content').toggle();
		$(this).find('a#permalink').toggle();
	});
	$("div#items div#content").hover(function() {
	 	$(this).toggle();
		$(this).parent().find('div#header a#permalink').toggle();
	});
	
});