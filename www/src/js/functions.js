////////////////////////
//////// FUNCTIONS /////
////////////////////////

const DEBUG = false;
const loadIT = true;

//// MAIN ////
function fileExists(url) {
    if (url) {
        var req = new XMLHttpRequest();
        req.open('GET', url, false);
        req.send();
        return req.status == 200;
    } else {
        return false;
    }
}

function loadSite(site) {
    var siteFullPath = 'views/' + site + '.html';
    $(".content-viewer > .content").addClass('content-grey').addClass('content-zero');
    $.get(siteFullPath, function(data) {
        setTimeout(function() {
            $(".content-viewer > .content").remove();
            $(".content-viewer").html(data);
        }, 500);
        setTimeout(function() {
            $(".content-viewer > .content").removeClass('content-zero');
            setTimeout(function() {
                if (site == 'logs') { loadLog('midiDisplay.log'); }
                if (site == 'devices') { loadDevices(); }
            }, 250);
        }, 1000);
        if (DEBUG) { console.log("loadSite(" + site + ") ==> " + siteFullPath); }
    }, 'text');
}
//// MENU HEADER ////
function urlParam(urlparam) {
    window.location.href = urlparam;
    if (urlparam == '#refresh') {
        window.location.reload();
        window.location.href = '/www';
    }
    if (DEBUG) { console.log("urlParam(urlparam)::" + urlparam); }
}

//// DEVICES ////
function checkDeviceJSON(deviceID) {
    if (deviceID!=null || deviceID!=undefined || deviceID!="undefined") {
        /* CHECK IF DEVID IS AVAILABLE AND RETURN TRUE/FALSE */

        var jsonFile = 'device_' + deviceID + '.json';
        var jsonFilePath = '/conf/devices/' + jsonFile;

        $.getJSON(jsonFilePath, function(data, textStatus) {
            if (textStatus == "success") {
                if (DEBUG) { console.log("checkDeviceJSON(" + deviceID + ")::found ==> " + jsonFile); }
                return;
            }
        });
    }
}

function loadDeviceFromJSON(deviceID) {
    if (deviceID != null || deviceID != undefined || deviceID != "undefined" || deviceID != "") {
        /* LOAD DEVICE DATA FROM JSON */

        var jsonFile = 'device_' + deviceID + '.json';
        var jsonFilePath = '/conf/devices/' + jsonFile;
        var device = [];
        var line;

        $.getJSON(jsonFilePath, function(data, textStatus) {
            if (textStatus == "success") {
                $.each(data, function(key, val) { device[key] = val; });
                var line = '<div class="device" deviceID="' + device['deviceID'] + '"><div onclick="deviceSettings(\'' + device['deviceID'] + '\');" class="settings" id="device' + device['deviceID'] + '" device-id="' + device['deviceID'] + '" device-title="' + device['title'] + '" device-usbid="' + device['usbID'] + '" device-desc="' + device['desc'] + '" device-icon="' + device['icon'] + '"></div><div class="icon" style="background:url(assets/images/icons/midi/' + device['icon'] + ') center no-repeat;background-size:contain;"></div><div class="title">' + device['title'] + '</div><div class="portid">' + device['deviceID'] + ':0</div><div class="midi"><div class="icon"></div><div class="command">none</div></div></div>';
                $("#devices > .devices").append(line);
            }
        });
    }
}

function loadDevices() {
    var deviceFile = '/www/logs/midiDisplay.list',
        line;
    //var device = [];
    if (DEBUG) { console.log("loadDevices()::loading ==> " + deviceFile); }
    setTimeout(function() {
        $.get(deviceFile, function(data) {
            var lines = data.split("\n");
            if (DEBUG) {
                console.log("deviceFile: " + deviceFile + " loaded");
                console.log("loadDevices()::lines ==> " + lines);
            }
            for (var i = 0, len = lines.length; i < len; i++) {
                var lineData = lines[i].split(":");
                var deviceID = lineData[1];
                if (deviceID != null || deviceID != undefined || deviceID != "undefined" || deviceID != "") {
                    if (DEBUG) {
                        console.log("loadDevices()::lineData ==> " + lineData);
                        console.log("loadDevices()::deviceID ==> " + deviceID);
                    }
                    //var ChkDevJSON = checkDeviceJSON(deviceID);
                    //if (!checkDeviceJSON(deviceID)) {
                    var file = '/conf/devices/device_' + deviceID + '.json';
                    var Ffile = new File([""], file);
                    //if (!fileExists(urlToFile)) {
                    if (Ffile) {
                        // checkDeviceJSON = TRUE
                        if (DEBUG) {
                            console.log('fileExists(' + urlToFile + ')::TRUE');
                            console.log('loadDeviceFromJSON(' + deviceID + ')::TRUE');
                        }
                        loadDeviceFromJSON(deviceID);

                    } else {
                        // checkDeviceJSON = FALSE
                        if (DEBUG) {
                            console.log('fileExists(' + Ffile + ')::FALSE');
                            console.log('loadDeviceFromJSON(' + deviceID + ')::FALSE ==> USING ' + deviceFile);
                        }
                        var line = '<div class="device" deviceID="' + lineData[1] + '"><div onclick="deviceSettings(\'' + lineData[1] + '\');" class="settings" id="device' + lineData[0] + '" device-id="' + lineData[0] + '" device-title="' + lineData[0] + '" device-usbid="' + lineData[1] + ':0" device-desc="none" device-icon="piano.svg"></div><div class="icon"></div><div class="title">' + lineData[0] + '</div><div class="portid">' + lineData[1] + ':0</div><div class="midi"><div class="icon"></div><div class="command">none</div></div></div>';
                        if (lineData[1] != undefined && lineData[0] != undefined && deviceID != undefined) { $("#devices > .devices").append(line); }
                    }
                }
            }
        }, 'text');
    }, 25);
}

function saveDeviceAsJSON(deviceID, title, usbid, desc, icon) {
    // save Device in JSON file
    if (deviceID != undefined || title != undefined || usbid != undefined || desc != undefined || icon != undefined) {
        $.get("/saveDevice", { id: deviceID, devicename: title, usbid: usbid, desc: desc, icon: icon },
            function(data, status) {
                setTimeout(function() { window.location.reload(true); }, 100);
                if (DEBUG) { console.log("Data: " + data + "\nStatus: " + status); }
            });
    }
}

function create_iconPicker() {
    var jsonStream = '/listIcons',
        icons = [],
        iconsNoExt = [];

    $.getJSON(jsonStream, function(result){
      $.each(result, function(i, field){
        var lines = field;
        for (var c = 0, len = lines.length; c < len; c++) {
            var splitline = lines[c].split("midi/"),
                splitlineExt = splitline[1].split(".svg");
            icons[c] = splitline[1];
            iconsNoExt[c] = splitlineExt[0];

            // GENERATE HTML CODE WITH ICON
            var line = '<div class="icon-picker_icon" id="' + iconsNoExt[c] + '" onclick="javascript:iconPickerSelectIcon(this);" style="background-image: url(/www/assets/images/icons/midi/' + icons[c] + ');"></div>\n';
            $("#icon-picker > .icon-picker_icons").append(line);
            
            if(DEBUG) {
                console.log('icon: ' + icons[c]);
                console.log('iconsNoExt: ' + iconsNoExt[c]);
            }
        }
      });
    });
}

function iconPicker() {
    var toggle = $(".icon-icon").attr('toggle');
    if (toggle == "disabled") {
        $(".icon-icon").attr({ "toggle": "enabled" });
        $("#icon-picker").css({ "width": "100%", "opacity": 1 });
        if (DEBUG) { console.log('iconPicker()::clicked ==> enabled'); }
    } else {
        $(".icon-icon").attr({ "toggle": "disabled" });
        $("#icon-picker").css({ "width": "0%", "opacity": 0 });
        if (DEBUG) { console.log('iconPicker()::clicked ==> disabled'); }
    }
}

function iconPickerFocusOut() {
	setTimeout(function() {
	    $(".icon-icon").attr({ "toggle": "disabled" });
	    $("#icon-picker").css({ "width": "0%", "opacity": 0 });
	    if (DEBUG) { console.log('iconPicker()::clicked ==> focus-out > disabled'); }
	}, 500);
}

function iconPickerSelectIcon(element) {
	var thisElement = $(element),
		thisId = thisElement[0].id,
		fileName = thisId + '.svg',
		fileNamePath = 'assets/images/icons/midi/' + fileName;
		$( ".icon-image" ).attr({"src": fileNamePath});
		$( "input#device_icon" ).val(fileName);
		$( ".icon-picker" ).css({"width": "0%","opacity": 0});
	if (DEBUG==true){ 
		console.log('iconPicker()::elementID ==> ' + thisId + '\niconPicker()::image ==> ' + fileName + '\niconPicker()::path ==> ' + fileNamePath);
	}
}

function openEditor(deviceicon) {
    var icon_fullpath = 'assets/images/icons/midi/' + deviceicon;
    $(".icon-image").attr({ "src": icon_fullpath });
    $("input#device_icon").val(deviceicon);
    $("#overlay").css({ "display": "block" });
    setTimeout(function() {
        $("#overlay").css({ "transform": "scaleX(1)", "opacity": 1 });
        $("#editor").css({ "transform": "scaleY(1)", "opacity": 1 });
    }, 25);
    if (DEBUG) { console.log('openEditor()::clicked ==> ' + this); }
}

function closeEditor() {
    if (DEBUG) { console.log('closeEditor()::clicked ==> ' + this); }
    $("#editor").css({ "transform": "scaleY(0)", "opacity": 0 });
    $("#overlay").css({ "transform": "scaleX(0)", "opacity": 0 });
    setTimeout(function() { $("#overlay").css({ "display": "none" }); }, 250);
}

function submitEditor() {
    if (DEBUG) { console.log('form()::submit'); }
    var device_id = $("input#device_id").val(),
        device_icon = $("input#device_icon").val(),
        device_title = $("input#device_title").val(),
        device_usbid = $("input#device_usbid").val(),
        device_desc = $("input#device_desc").val();
    closeEditor();
    saveDeviceAsJSON(device_id, device_title, device_usbid, device_desc, device_icon);
    // return;
    location.reload(true);
}

function deviceSettings(deviceid) {
    // LOAD DEVICE SETTINGS INTO EDITOR
    if (deviceid != null || deviceid != undefined || deviceid != "undefined") {
        var elementid = '#device' + deviceid;
        var deviceid = $(elementid).attr('device-id'),
            devicetitle = $(elementid).attr('device-title'),
            deviceusbid = $(elementid).attr('device-usbid'),
            devicedesc = $(elementid).attr('device-desc'),
            deviceicon = $(elementid).attr('device-icon');
        openEditor(deviceicon);
        $("#device_id").val(deviceid);
        $("#device_title").val(devicetitle);
        $("#device_usbid").val(deviceusbid);
        $("#device_desc").val(devicedesc);
        $("#device_icon").val(deviceicon);
        if (DEBUG) {
            console.log('deviceSettings(' + deviceid + ')::clicked ==> ' + elementid);
            console.log('++DEVICE-DATA++\ntitle: ' + devicetitle + '\nid: ' + deviceid + '\nusbid: ' + deviceusbid + '\ndesc: ' + devicedesc + '\nicon: ' + deviceicon);
        }
    }
}

//// LOGS ////
function loadLog(logFile) {
    var logFile = 'logs/' + logFile;
    $.get(logFile, function(data) {
        $("#file-viewer > p").remove();
        $("#file-viewer").html('<p></p>');
        var lines = data.split("\n");
        for (var i = 0, len = lines.length; i < len; i++) {
            if (i < 10) { ii = '0' + i; } else { ii = i; }
            var line = '<div class="lines"><div class="line-row-num">' + ii + '</div><div class="line-row">' + lines[i] + "</div><br/>";
            if (lines[i]!=null && lines[i]!=undefined) { $("#file-viewer > p").append(line); }
        }
        if (DEBUG) { console.log("logFile: " + logFile + " loaded"); }
    }, 'text');
}