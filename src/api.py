import psycopg2 
import json
from export import rows_to_json
from urllib.parse import unquote

def extract_restrictions(path:str) -> list:
    restrictions = []
    restrictions_str = path.split('&')
    for restriction_str in restrictions_str:
        tmp = restriction_str.split('=')
        if len(tmp) != 2:
            return None
        restrictions.append((tmp[0], tmp[1]))
    return restrictions

# Completly exposed to sql injection
def get_kante_data(restrictions) -> bytes:
    data = None
    query = ''' 
    SELECT kante.id, kante_tip.ime, kante_tip.prima, kante_tip.privatno,
        četvrti.ime, četvrti.površina, četvrti.broj_stanovnika,
        reciklažna_dvorišta.ime, reciklažna_dvorišta.adresa,
        geo_visina, geo_širina
    FROM kante
    LEFT JOIN reciklažna_dvorišta ON reciklažno_dvorište_id = reciklažna_dvorišta.id
    LEFT JOIN četvrti ON četvrti.id = četvrt_id
    LEFT JOIN kante_tip ON kante_tip.id = tip_id
    '''
    if restrictions:
        if len(restrictions) != 0:
            query += '\n WHERE '
        i=0
        for restriction in restrictions:
            query += f"{restriction[0]} = \'{restriction[1]}\'"
            if (i != len(restrictions) -1):
                query += ' and '
            i+=1
    query += ';'
    conn = psycopg2.connect("dbname=kante_zagreb user=fabian")
    cur = conn.cursor()
    rows = None
    try:
        cur.execute(query)
        rows = cur.fetchall()
        print(rows)
    except:
        rows = None
    finally:
        cur.close()
        conn.close()
    if rows == None:
        return None
    data = rows_to_json(rows)
    return bytes(json.dumps(data), "utf-8")


    
def api(path:bytes) -> bytes:
    path = unquote(path)
    path = path.removeprefix('/api/')
    # Determine table
    table = path[:path.find('?')]
    if ( (table != 'kante' and table != 'rd') or ('?' not in path)):
        return None
    path = path[path.find('?')+1:]
    #Determine restrictions
    restrictions = extract_restrictions(path)
    if table == 'kante':
        return get_kante_data(restrictions)
    elif table == 'rd':
        return get_rd_data(restrictions)
    else:
        return None

