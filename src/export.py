import psycopg2 
import json

def create_kanta_object(row):
    return { 
            'object_type': 'kanta', 'id':row[0], 
            'tip': {'ime':row[1], 'prima':row[2], 'privatno':row[3]},
            'četvrt':{'četvrt_ime': row[4], 'četvrt_površina':row[5], 'četvrt_broj_stanovnika':row[6]},
            'geo_visina':row[9], 'geo_širina':row[10]
    }

def rows_to_json(rows:list) -> list:
    result = []
    # Pronađi reciklažna_dvorišta
    rd_dvorišta = {}
    for row in rows:
        # Kanta pripada reciklažnom dvorištu
        if row[7] != None:
            try:
                rd_dvorišta[row[7]]
            except KeyError:
                rd_dvorišta[row[7]] = {
                        'object_type':'RD-dvorište',
                        'ime':row[7],
                        'adresa':row[8],
                        'kante':[]
                }
            rd_dvorišta[row[7]]['kante'].append(create_kanta_object(row))
        else:
            result.append(create_kanta_object(row))
    
    for dvorište in rd_dvorišta.values():
        result.append(dvorište)
    return result


# Stvrara listu koja sadržava objekta kanti i reckilažnih_dvorišta,
# reckilažna dvorišta sadrže objekte kanti
def export_json(cur):
    query = ''' 
    SELECT kante.id, kante_tip.ime, kante_tip.prima, kante_tip.privatno,
        četvrti.ime, četvrti.površina, četvrti.broj_stanovnika,
        reciklažna_dvorišta.ime, reciklažna_dvorišta.adresa,
        geo_visina, geo_širina
    FROM kante
    LEFT JOIN reciklažna_dvorišta ON reciklažno_dvorište_id = reciklažna_dvorišta.id
    LEFT JOIN četvrti ON četvrti.id = četvrt_id
    LEFT JOIN kante_tip ON kante_tip.id = tip_id;
    '''
    cur.execute(query)
    rows = cur.fetchall()

    return rows_to_json(rows)

def export_csv(cur):
    query = ''' 
    SELECT kante.id, kante_tip.ime, kante_tip.prima, kante_tip.privatno,
        četvrti.ime, četvrti.površina, četvrti.broj_stanovnika,
        reciklažna_dvorišta.ime, reciklažna_dvorišta.adresa,
        geo_visina, geo_širina
    FROM kante
    LEFT JOIN reciklažna_dvorišta ON reciklažno_dvorište_id = reciklažna_dvorišta.id
    LEFT JOIN četvrti ON četvrti.id = četvrt_id
    LEFT JOIN kante_tip ON kante_tip.id = tip_id;
    '''
    cur.execute(query)
    rows = cur.fetchall()
    csv_str = "id,tip,prima,privatna,ime_četvrti,četvrt_površina,četvrt_broj_stanovnika,ime_reciklažnog_dvorišta,adresa_reciklažnog_dvorišta,geo_visina,geo_širina\n"
    for row in rows:
        row_str = ",".join(list(map(lambda x: str(x), list(row))))+"\n"
        csv_str += row_str
    return csv_str[:-1]

def export(format:str, output_file:str):
    conn = psycopg2.connect("dbname=kante_zagreb user=fabian")
    cur = conn.cursor()
    
    if (format == "json"):
        result = export_json(cur)
        with open(output_file, "w") as file:
            json.dump(result, file)
    elif (format == "csv"):
        result = export_csv(cur)
        with open(output_file, "w") as file:
            file.write(result)
    else:
        print(f"Error, invalid format \"{format}\" in export function")
        cur.close()
        conn.close()
        return 1

    cur.close()
    conn.close()
    return 0
