select array_to_json(array_agg(row_to_json(t)))
from (
	select id, geo_visina, geo_širina, (
		select row_to_json(četvrti)
		from četvrti
		where četvrti.id=četvrt_id
	) as četvrt,
	(
		select row_to_json(kante_tip)
		from kante_tip
		where tip_id=kante_tip.id
	) as tip
	from kante
) t;
