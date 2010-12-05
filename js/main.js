$(function() {
	//jquery ui tabs
	var tabs = $("#tabs").tabs({
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
	var rolecolor = $.farbtastic("div#addupdaterole div#colorchoose","input#color");
	var roledialog = $("div#roles").dialog({autoOpen: false,
			buttons: [
				{
			        text: "New Role",
			        click: function() {
						//show new dialog for adding role info
						$(this).find("div#addupdaterole").show();
						$(this).parent().find("div.ui-dialog-buttonpane").hide();
					}
	   		}],
			width: 450
	});
	var roledata = "";
	$("div#roles ol li").each(function() {
		roledata = $(this).find('span.hidden').text();
		roledata = roledata.split('|');
		$(this).css('background-color',roledata[1]);
	});
	
	//actually add a new role
	$("div#addupdaterole a#submit").click(function() {
		var rolename = $(this).parent().find("input#name").val();
		rolecolor = rolecolor.color;
		rolecolor = rolecolor.split('#');
		var attrdata = new Array();
		var attrparams = "";
		var counter = 0;
		$(this).parent().find("div#attrs div").each(function() {
			attrdata[0] = $(this).find("select#attr").val(); //attr 
			attrdata[1] = $(this).find(" input#value").val(); //value
			attrdata[2] = $(this).find("select#comparison").val(); //comparison
			if (attrdata[1] != "") {
				attrparams = attrparams+"&attr"+counter+"="+attrdata[0]+"&val"+counter+"="+attrdata[1]+"&comp"+counter+"="+attrdata[2];	
			}
			counter = counter+1;
		});
		alert("rolename="+rolename+"&rolecolor="+rolecolor[1]+"&do=addrole"+attrparams);
		$.ajax({
			type: "POST",
			url: "viewtools.py",
			data: "rolename="+rolename+"&rolecolor="+rolecolor[1]+"&do=addrole"+attrparams,
			complete: function() {
				location.reload();
			}
		});
	});
	
	//remove role
	$("a#remove").click(function() {
		//remove role from view
		$(this).parent().hide();
		roledata = $(this).parent().find('span.hidden').text();
		roledata = roledata.split('|');
		//remove role from db and set all items with that role to -1 (none)
		$.ajax({
			type: "POST",
			url: "viewtools.py",
			data: "roleid="+roledata[0]+"&do=removerole"
		});
		//refresh tab
		var selected = tabs.tabs("option","selected");
		tabs.tabs('load',selected);
	});
	
	//edit role
	$("div#roles ol li a#edit").click(function() {
	});

	//roles link dialog box
	$("div#roleslink").click(function() {
		
		roledialog.dialog("open");
		$("div#roles").show();
	});

	//add a role attribute
	$("div#roles div[id|=attr] a").click(function() {
		var showdiv = $(this).attr('id');
		showdiv = showdiv.split('-');
		$(this).parent().parent().find('div#attr-'+showdiv[1]).show();
	})
});