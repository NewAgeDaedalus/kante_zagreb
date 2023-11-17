import psycopg2 
import json
from export import rows_to_json
from urllib.parse import unquote
from os import environ

def extract_restrictions(path:str) -> list:
    attributes = []
    path_list = path.split('=')
    print(path_list)
    if (len(path_list) < 2):
        return None, None
    attributes = path_list[0].split(",")
    return attributes, path_list[1]

def fill_missing_containers(cur, data):
    for rd in data:
        query='''
        SELECT kante.id, kante.prima
        FROM kante
        join reciklažna_dvorišta on id_dvorišta = reciklažna_dvorišta.id
        where id_dvorišta = 
        '''
        query += f'{rd["id"]};'
        cur.execute(query)
        rd["kante"] = []
        nove_kante = cur.fetchall()
        for nova_kanta in nove_kante:
            rd["kante"].append({
                "id": nova_kanta[0],
                "prima":nova_kanta[1]
            })

# Completly exposed to sql injection
def get_rd_data(atributi, value) -> bytes:
    data = None
    query = ''' 
    SELECT reciklažna_dvorišta.*, kante.id as kanta_id, kante.prima from
    reciklažna_dvorišta join kante on reciklažna_dvorišta.id = id_dvorišta
    '''
    if ( atributi == [] or atributi[0] == "wildcard"):
        restriction = value.lower()
        query += f"\n WHERE LOWER(CAST(reciklažna_dvorišta.id as VARCHAR)) like '%{restriction}%'"
        query += f"\n or LOWER(ime) like '%{restriction}%'"
        query += f"\n or LOWER(adresa) like '%{restriction}%'"
        query += f"\n or LOWER(telefonski_broj) like '%{restriction}%'"
        query += f"\n or LOWER(CAST(četvrt as VARCHAR)) like '%{restriction}%'"
        query += f"\n or LOWER(radno_vrijeme) like '%{restriction}%'"
        query += f"\n or LOWER(CAST(geo_širina as VARCHAR)) like '%{restriction}%'"
        query += f"\n or LOWER(CAST(geo_dužina as VARCHAR)) like '%{restriction}%'"
        query += f"\n or LOWER(CAST(kante.id as VARCHAR)) like '%{restriction}%'"
        query += f"\n or LOWER(CAST(prima as VARCHAR)) like '%{restriction}%'"
    elif (atributi != []):
        i = 0
        for atribut in atributi:
            value = value.lower()
            if (i == 0):
                query += f"\n WHERE LOWER(CAST({atribut} as VARCHAR)) like '%{value}%'"
            else:
                query += f"\n or LOWER(CAST({atribut} as VARCHAR)) like '%{value}%'"
            i+=1

    query += ";";
    print(query)
    db_user = environ['KANTE_ZAGREB_USER']
    conn = psycopg2.connect(f"dbname=kante_zagreb user={db_user}")
    cur = conn.cursor()
    rows = None
    try:
        cur.execute(query)
        rows = cur.fetchall()
        print(rows)
    except:
        rows = None
    if rows == None:
        cur.close()
        conn.close()
        return None
    data = rows_to_json(rows)
    fill_missing_containers(cur, data)
    cur.close()
    conn.close()
    return bytes(json.dumps(data), "utf-8")


    
def api(path:bytes) -> bytes:
    path = unquote(path)
    path = path.removeprefix('/api/')
    # Determine table
    #Determine restrictions
    attributes, value = extract_restrictions(path)
    if (attributes == None or  value == None):
        return bytes(json.dumps({"error": "Invalid url"}), "utf-8")
    return get_rd_data(attributes, value)

