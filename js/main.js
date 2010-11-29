$(function() {
	//jquery ui tabs
	$("#tabs").tabs({
		ajaxOptions: {
						error: function( xhr, status, index, anchor ) {
							$( anchor.hash ).html(
								"Couldn't load this tab. We'll try to fix this as soon as possible. " +
								"If this wouldn't be a demo." );
						}
					}
	});
	
	//roles-modifying dialog box
	$("div#roles ol").sortable({handle: 'img'});
	
	var roledialog = $("div#roles").dialog({autoOpen: false,
			buttons: [
				{
			        text: "New Role",
			        click: function() {
						//add a new role
					}
	   		}]
	});
	var roledata = "";
	$("div#roles ol li").each(function() {
		roledata = $(this).find('span.hidden').text();
		roledata = roledata.split('|');
		$(this).css('background-color',roledata[1]);
	});
	$("div#roles ol li a#remove").click(function() {
		//remove role
	});
	$("div#roles ol li a#edit").click(function() {
		//edit role
	});
	//roles link dialog box
	$("a#roleslink").click(function() {
		roledialog.dialog("open");
	});
});