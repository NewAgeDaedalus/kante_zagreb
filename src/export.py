import psycopg2 
import json
import os

def rows_to_json(rows:list) -> list:
    result = []
    # Pronađi reciklažna_dvorišta
    rd_dvorišta = {}
    for row in rows:
        try:
            rd_dvorišta[row[0]]
            rd_dvorišta[row[0]]["kante"].append({"id":row[8], "prima":row[9]})
        except KeyError:
            rd_dvorišta[row[0]] = {
                    "id":row[0],
                    "ime":row[1],
                    "adresa":row[2],
                    "telefonski_broj":row[3],
                    "četvrt":row[4],
                    "radno_vrijeme":row[5],
                    "geo_širina":row[6],
                    "geo_dužina":row[7],
                    "kante":[{"id":row[8], "prima":row[9]}]
            }

    
    for dvorište in rd_dvorišta.values():
        result.append(dvorište)
    return result

# Stvrara listu koja sadržava objekta kanti i reckilažnih_dvorišta,
# reckilažna dvorišta sadrže objekte kanti
def export_json(cur):
    query = ''' 
    SELECT reciklažna_dvorišta.*, kante.id as kanta_id, kante.prima from
    reciklažna_dvorišta join kante on reciklažna_dvorišta.id = id_dvorišta; 
    '''
    cur.execute(query)
    rows = cur.fetchall()

    return rows_to_json(rows)

def export_csv(cur):
    query = ''' 
    SELECT reciklažna_dvorišta.*, kante.id as kanta_id, kante.prima from
    reciklažna_dvorišta join kante on reciklažna_dvorišta.id = id_dvorišta; 
    '''
    cur.execute(query)
    rows = cur.fetchall()
    csv_str = "id,ime,adresa,telefonski_broj,četvrt,radno_vrijeme,geo_širina,geo_širina,geo_dužina,kanta_id,prima\n"
    for row in rows:
        row_str = ",".join(list(map(lambda x: str(x), list(row))))+"\n"
        csv_str += row_str
    return csv_str[:-1]

def export(format:str, output_file:str):
    db_user = os.environ["KANTE_ZAGREB_USER"]
    conn = psycopg2.connect(f"dbname=kante_zagreb user={db_user}")
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
