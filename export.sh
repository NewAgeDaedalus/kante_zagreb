#/bin/bash

db_name="kante_zagreb"
format=$1
output_file=$2

json_query=\
"select array_to_json(array_agg(row_to_json(t))) "\
"from ( "\
"	select id, geo_visina, geo_širina, ( "\
"		select row_to_json(četvrti) "\
"		from četvrti "\
"		where četvrti.id=četvrt_id "\
"	) as četvrt, "\
"	("\
"		select row_to_json(kante_tip) "\
"		from kante_tip "\
"		where tip_id=kante_tip.id "\
"	) as tip "\
"	from kante "\
") t; "

csv_query=\
"COPY (select kante.id, geo_visina, geo_širina, kante_tip.ime as ime_kante, prima, privatno, četvrti.ime as ime_četvrti, "\
"površina, broj_stanovnika "\
"from kante, četvrti, kante_tip "\
"where kante.tip_id=kante_tip.id and kante.četvrt_id=četvrti.id) TO STDOUT with csv"

if [[ $output_file == "" || $format == "" ]]; then
	exit 1;
fi

if [ $format == "json" ]; then
	psql -d $db_name -q -c "$json_query" | grep "\[" > $output_file
elif [ $format == "csv" ]; then
	psql -d $db_name -c "$csv_query" > $output_file
fi
