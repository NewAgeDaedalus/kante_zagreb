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
		return "/api/kante?";
	else
		return "/api/kante?" + dropbar.value + "=" + filter.value;
}


function create_cell(value){
	cell = document.createElement("td");
	cell.innerHTML=value
	return cell;
}

function create_row_kanta(object, table, rd, addr){
	row = document.createElement("tr")
	row.appendChild(create_cell(String(object.id)))
	row.appendChild(create_cell(String(object.tip.ime)))
	row.appendChild(create_cell(String(object.tip.prima)));
	row.appendChild(create_cell(String(object.četvrt.četvrt_ime)));
	row.appendChild(create_cell(rd));
	row.appendChild(create_cell(addr));
	row.appendChild(create_cell(String(object.geo_visina)));
	row.appendChild(create_cell(String(object.geo_širina)));
	table.appendChild(row)
}

function create_rows(object, table){
	for (let i=0; i < object.kante.length; i++){
		create_row_kanta(object.kante[i], table, object.ime, object.adresa);
	}
}

function create_table(){
	let table = document.getElementById("tb")
	table.innerHTML=""
	console.log(current_json_obj[0].object_type)
	for (let i = 0; i < current_json_obj.length; i++){
		if (current_json_obj[i].object_type == "kanta")
			create_row_kanta(current_json_obj[i], table, "NULL", "NULL");	
		else
			create_rows(current_json_obj[i], table);
	}
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
	let dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(current_json_obj));
	let downloadAnchorNode = document.createElement('a');
	downloadAnchorNode.setAttribute("href",     dataStr);
	downloadAnchorNode.setAttribute("download", "kante.json");
	document.body.appendChild(downloadAnchorNode); // required for firefox
	downloadAnchorNode.click();
	downloadAnchorNode.remove();
}
function construct_csv(){
	let csv = "id,tip,otpad,četvrt,rd,adresa,geo_širina,geo_visina\n";
	let table = document.getElementById("tb");
	let rows = table.querySelectorAll("tr"); 
	for (let i = 0; i < rows.length; i++){
		let row = rows[i];
		let cells = row.querySelectorAll("td");
		console.log(cells)
		for (let j = 0; j < cells.length; j++){	
			csv += cells[j].innerHTML;
			if ( j != cells.length -1 )
				csv += ","
		}
		if ( i != rows.length -1 )
			csv += "\n"
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
	current_json_obj = await get_data("/api/kante?")
	create_table()
}

main()
