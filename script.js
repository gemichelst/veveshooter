//**************************************************//
// GEMICHELST.DE ANIMATION SCRIPT                   //
// developed by MICHAEL MATZAT 2019                 //
//**************************************************//
// CHANGES WILL BREAK THE ANIMATION                 //
// DONT CHANGE CODE IF YOU NOT KNOWING WHAT TO DO!  //
//**************************************************//

////////////
// DEBUG: //
////////////
const debug = false;
const version = '0.1';

///////////////
// FUNCTIONS //
///////////////
$.fn.name = function () {

};
$.urlParam = function(name) {
	var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
	if (results == null) { return null; }
	return decodeURI(results[1]) || 0;
};

function csv_output(data) {
	var html;
	if(typeof(data[0]) === 'undefined') {
        console.log('CSV_OUTPUT: no data!')
        return null;
      } else {
		$.each(data, function( index, row ) {

			html += '<tr class="mdc-data-table__row">';
			html += '<td class="mdc-data-table__cell mdc-data-table__cell--checkbox td-delete"><span class="material-icons" data-shootid="" id="btn-delete">delete</span></td>';
			$.each(row, function( index, colData ) {
				html += '<td class="mdc-data-table__cell mdc-data-table__cell--numeric">' + colData + '</td>';
				// html += '<td class="mdc-data-table__cell mdc-data-table__cell--numeric">' + colData + '</td>';
			});
			html += '</tr>';
		  
		});
		$('#tbody').append(html);
	  }
}

///////////
// READY //
///////////
$(document).ready(function(){


// STATE
console.log('veveshooter v'+version);
console.log('coded by www.madz.dev');
console.log('\n');

// READ CSV
var data;
$.ajax({
	type: "GET",
	url: "shoots.csv",
	dataType: "text",
	success: function(response)
	{
		data = $.csv.toArrays(response);
		csv_output(data);
		if(debug==true){console.log(data);}
		
	} 
});






});