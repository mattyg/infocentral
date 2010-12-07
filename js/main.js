function getdata(){
	$("div#newitems").text("checking for updates...");
	$("div#newitems").show();
 	$.ajax({
		url: "getdata.py",
		success: function(data,txtstatus,xmlresponse) {
			if(parseInt(data) > 0) {
				location.reload();
				$("div#newitems").text("Updated ["+data+" new items]");
				$("div#newitems").show();
			}
			else {
				$("div#newitems").hide();
			}
		}
	});
}
$(function() {
	//update getdata.py and reload tab every 5 mins
	getdata();
	setInterval("getdata()",60000);
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
	var positions = "";
	var res = $("div#roles ol").sortable({handle: 'img',
		update: function(event,ui) {
			var countr = 0;
			$(this).children('li').each(function() {
				var roleid = $(this).find('span.hidden').text().split('|')[0];
				$.ajax({
					type: "POST",
					url: "viewtools.py",
					data: "roleid="+roleid+"&do=editpositions"+"&roleposition="+countr
				});
				countr = countr+1;
			});                                     			
		}
	});
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
			attrdata[1] = $(this).find("input#value").val(); //value
			attrdata[2] = $(this).find("select#comparison").val(); //comparison
			if (attrdata[1] != "") {
				attrparams = attrparams+"&attr"+counter+"="+attrdata[0]+"&val"+counter+"="+attrdata[1]+"&comp"+counter+"="+attrdata[2];	
			}
			counter = counter+1;
		});
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
	$("div#roles ol li a#remove").click(function() {
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
	});
	
	///////feeds dialog box
	//build dialog
	var feeddialog = $("div#feeds").dialog({autoOpen: false,
			buttons: [
				{
			        text: "New Feed",
			        click: function() {
						//show new dialog for adding feed info
						$(this).find("div#addupdatefeed").show();
						$(this).parent().find("div.ui-dialog-buttonpane").hide();
					}
	   		}],
			width: 650
	});
	//open dialog
	$("div#feedslink").click(function() {
		feeddialog.dialog('open');
		$("div#feeds").show();
	});
	//remove feed
	$("div#feeds ul li a#remove").click(function() {
		//remove role from view
		$(this).parent().hide();
		feeddata = $(this).parent().find('span.hidden').text();
		//remove role from db and set all items with that role to -1 (none)
		$.ajax({
			type: "POST",
			url: "viewtools.py",
			data: "feedid="+feeddata+"&do=removefeed"
		});
		//refresh tab
		var selected = tabs.tabs("option","selected");
		tabs.tabs('load',selected);
	});
	//actually add feed
	$("div#addupdatefeed a#submit").click(function() {
		var feedtype = $(this).parent().find("select#type").val();
		var feedurl = $(this).parent().find("input#url").val();
		var feeduser = $(this).parent().find("input#secureuser").val();
		var feedpass = $(this).parent().find("input#securepass").val();
		var feedroleid = $(this).parent().find("select#roleid").val();
		var feeduserid = $(this).parent().find("span.hidden").text();
		$.ajax({
			type: "POST",
			url: "viewtools.py",
			data: "userid="+feeduserid+"&feedtype="+feedtype+"&feedurl="+feedurl+"&secureuser="+feeduser+"&securepass="+feedpass+"&roleid="+feedroleid+"&do=addfeed",
			complete: function() {
				location.reload();
			}
		});
	});
	
	//show 15 more old items
	$("div#moreitems").click(function() {
		var sel = parseInt(tabs.tabs("option","selected"));
		sel = eval(sel+1);
		var currentnum = $("div#tabs div#ui-tabs-"+sel.toString()+" div#items").find("span#hiddenrecent").text();
		currentnum = parseInt(currentnum);
		currentnum = eval(currentnum+15);
		var currenturl = $("div#tabs div#ui-tabs-"+sel.toString()+" div#items").find('span#hiddenurl').text();
		currenturl = currenturl.split("&recent=")[0];
		newurl = currenturl+"&recent="+currentnum;
		tabs.tabs('url',eval(sel-1),newurl);
		tabs.tabs('load',eval(sel-1));
	});
	
	//sort by roleselect
	$("div#roleselect select").change(function() {
		roleid = $(this).val();
		var sel = parseInt(tabs.tabs("option","selected"));
		sel = eval(sel+1);
		var currenturl = $("div#tabs div#ui-tabs-"+sel.toString()+" div#items").find('span#hiddenurl').text();
		currenturl = currenturl.split('&for=');
		newurl = currenturl[0]+"&for="+roleid;
		tabs.tabs('url',eval(sel-1),newurl);
		tabs.tabs('load',eval(sel-1));
	})
});