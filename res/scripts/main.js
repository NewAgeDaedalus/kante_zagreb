let current_json_obj = null;

async function get_data(restrictions){
	console.log("http://0.0.0.0:1234"+restrictions)
	let response = await fetch("http://0.0.0.0:1234"+restrictions) // Don't have domain
	return await response.json()
}

async function get_query_data(){
	//Get the select
	const dropbar = document.getElementById("drop-bar")
	const filter = document.getElementById("filter");
	if (filter.value == '')
		return "/api/wildcard=" + filter.value;
	let ret = "/api/"
	for ( option of dropbar.options ){
		if ( !option.selected ){
			continue;
		}
		ret = ret + String(option.value) + ","
	}
	ret = ret.substring(0, ret.length -1); //remove ,
	return ret + "=" + filter.value;
}

function create_cell(value){
	cell = document.createElement("td");
	cell.innerHTML=value
	return cell;
}

function create_kante_cell(object){
	cell = document.createElement("td")
	button = document.createElement("button");
	button.setAttribute("onClick", "show_kante(" + String(object.id) + ");");
	button.innerHTML = "Prikaži kante"
	cell.appendChild(button)
	return cell;
}

function create_row_kanta(object, table){
	row = document.createElement("tr")
	row.appendChild(create_cell(String(object.id)))
	row.appendChild(create_cell(String(object.ime)))
	row.appendChild(create_cell(String(object.adresa)));
	row.appendChild(create_cell(String(object.četvrt)));
	row.appendChild(create_cell(String(object.telefonski_broj)));
	row.appendChild(create_cell(String(object.radno_vrijeme)));
	row.appendChild(create_cell(String(object.geo_širina)));
	row.appendChild(create_cell(String(object.geo_dužina)));
	row.appendChild(create_kante_cell(object))
	table.appendChild(row)
}

function create_table(){
	document.getElementById("kante-table-container").setAttribute("hidden", "");
	let table = document.getElementById("tb")
	table.innerHTML=""
	for (let i = 0; i < current_json_obj.length; i++){
		create_row_kanta(current_json_obj[i], table)
	}
}

function show_kante(id){
	//Find the kante
	let obj = null;
	for (let i=0; i < current_json_obj.length; i++){
		if (current_json_obj[i].id == id){
			obj = current_json_obj[i];
			break;
		}
	}
	if (obj == null)
		return;
	table = document.getElementById("kante-body");
	table.innerHTML = "";
	for ( kanta of obj.kante){
		row = document.createElement("tr")
		row.appendChild(create_cell(kanta.id))
		row.appendChild(create_cell(kanta.prima))
		table.appendChild(row);
	}
	document.getElementById("kante-label").innerHTML = "Spremnici u " + String(obj.ime);
	document.getElementById("kante-table-container").removeAttribute("hidden");
}

function downloadObjectAsJson(exportObj, exportName){
	var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(exportObj));
	var downloadAnchorNode = document.createElement('a');
	downloadAnchorNode.setAttribute("href",     dataStr);
	downloadAnchorNode.setAttribute("download", exportName + ".json");
	document.body.appendChild(downloadAnchorNode); // required for firefox
	downloadAnchorNode.click();
	downloadAnchorNode.remove();
}

function export_json(){
// 	let dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(current_json_obj));
// 	let downloadAnchorNode = document.createElement('a');
// 	downloadAnchorNode.setAttribute("href",     dataStr);
// 	downloadAnchorNode.setAttribute("download", "kante.json");
// 	document.body.appendChild(downloadAnchorNode); // required for firefox
// 	downloadAnchorNode.click();
// 	downloadAnchorNode.remove();
	let new_tab = window.open('data:application/json,' + JSON.stringify(current_json_obj));
}
function construct_csv(){
	let csv = "id,tip,otpad,četvrt,rd,adresa,geo_širina,geo_visina\n";
	for ( rd of current_json_obj ){
		let line =""
		line +=String(rd.id)+","
		line +=String(rd.ime)+","
		line +=String(rd.adresa)+","
		line +=String(rd.četvrt)+","
		line +=String(rd.telefonski_broj)+","
		line +=String(rd.radno_vrijeme)+","
		line +=String(rd.geografska_širina)+","
		line +=String(rd.geografska_dužina)+","
		for ( kanta of rd.kante ){
			csv += line + String(kanta.id) + "," + String(kanta.prima) + "\n";
		}
	}
	return csv;
}

function export_csv(){
	csv = construct_csv()
	let dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(csv);
	let downloadAnchorNode = document.createElement('a');
	downloadAnchorNode.setAttribute("href",     dataStr);
	downloadAnchorNode.setAttribute("download", "kante.csv");
	document.body.appendChild(downloadAnchorNode); // required for firefox
	downloadAnchorNode.click();
	downloadAnchorNode.remove()
}

async function query(e){
	if (e.keyCode != 13)
		return null;
	current_json_obj = await get_data(await get_query_data())
	create_table()
}

async function main(){
	//Get the data
	current_json_obj = await get_data("/api/wildcard=")
	create_table()
}

main()
