import psycopg2 
import json
from export import rows_to_json
from urllib.parse import unquote
from os import environ

def extract_restrictions(path:str) -> list:
    attributes = []
    path_list = path.split('=')
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
    db_user = environ['KANTE_ZAGREB_USER']
    conn = psycopg2.connect(f"dbname=kante_zagreb user={db_user}")
    cur = conn.cursor()
    rows = None
    try:
        cur.execute(query)
        rows = cur.fetchall()
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
    
def oldapi(path:bytes) -> bytes:
    path = unquote(path)
    path = path.removeprefix('/oldapi/')
    # Determine table
    #Determine restrictions
    attributes, value = extract_restrictions(path)
    if (attributes == None or  value == None):
        return bytes(json.dumps({"error": "Invalid url"}), "utf-8")
    return get_rd_data(attributes, value)

# New rest API
def wrap_response(status, message, response):
    return {
        "status": status,
        "message": message,
        "response": response
    }

def get_all_rds():
    rds = None
    query = '''
    SELECT reciklažna_dvorišta.*, kante.id as kanta_id, kante.prima from
    reciklažna_dvorišta join kante on reciklažna_dvorišta.id = id_dvorišta
    '''
    db_user = environ['KANTE_ZAGREB_USER']
    conn = psycopg2.connect(f"dbname=kante_zagreb user={db_user}")
    cur = conn.cursor()
    rows = None
    try:
        cur.execute(query)
        rows = cur.fetchall()
    except:
        rows = None
    if rows == None:
        cur.close()
        conn.close()
        return None
    rds = rows_to_json(rows)
    return rds


def get_rd(id):
    rd = None
    query = f'''
    SELECT reciklažna_dvorišta.*, kante.id as kanta_id, kante.prima from
    reciklažna_dvorišta join kante on reciklažna_dvorišta.id = id_dvorišta
    where reciklažna_dvorišta.id = {id}
    '''
    db_user = environ['KANTE_ZAGREB_USER']
    conn = psycopg2.connect(f"dbname=kante_zagreb user={db_user}")
    cur = conn.cursor()
    rows = None
    try:
        cur.execute(query)
        rows = cur.fetchall()
    except:
        rows = None
    if rows == None:
        cur.close()
        conn.close()
        return None
    rd = rows_to_json(rows)
    if (rd == []):
        return None
    return rd[0]

def get_rds_by_district(district:str):
    rds = None
    query = f'''
    SELECT reciklažna_dvorišta.*, kante.id as kanta_id, kante.prima from
    reciklažna_dvorišta join kante on reciklažna_dvorišta.id = id_dvorišta
    where CAST(reciklažna_dvorišta.četvrt as VARCHAR) like \'{district}\'
    '''
    db_user = environ['KANTE_ZAGREB_USER']
    conn = psycopg2.connect(f"dbname=kante_zagreb user={db_user}")
    cur = conn.cursor()
    rows = None
    try:
        cur.execute(query)
        rows = cur.fetchall()
    except:
        rows = None
    if rows == None:
        cur.close()
        conn.close()
        return None
    rds = rows_to_json(rows)
    if (rds == []):
        return None
    return rds

def get_rds_by_garbage(garbage_type:str):
    rds = None
    query = f'''
    SELECT reciklažna_dvorišta.*, kante.id as kanta_id, kante.prima from
    reciklažna_dvorišta join kante on reciklažna_dvorišta.id = id_dvorišta
    where CAST(kante.prima as VARCHAR) like \'{garbage_type}\'
    '''
    db_user = environ['KANTE_ZAGREB_USER']
    conn = psycopg2.connect(f"dbname=kante_zagreb user={db_user}")
    cur = conn.cursor()
    rows = None
    try:
        cur.execute(query)
        rows = cur.fetchall()
    except:
        rows = None
    if rows == None:
        cur.close()
        conn.close()
        return None
    rds = rows_to_json(rows)
    fill_missing_containers(cur, rds)
    if (rds == []):
        return None
    return rds

def get_rd_by_name(name:str):
    rds = None
    query = f'''
    SELECT reciklažna_dvorišta.*, kante.id as kanta_id, kante.prima from
    reciklažna_dvorišta join kante on reciklažna_dvorišta.id = id_dvorišta
    where reciklažna_dvorišta.ime like \'{name}\'
    '''
    db_user = environ['KANTE_ZAGREB_USER']
    conn = psycopg2.connect(f"dbname=kante_zagreb user={db_user}")
    cur = conn.cursor()
    rows = None
    try:
        cur.execute(query)
        rows = cur.fetchall()
    except:
        rows = None
    if rows == None:
        cur.close()
        conn.close()
        return None
    rds = rows_to_json(rows)
    if (rds == []):
        return None
    return rds

def update_kanta(kanta:dict, rd_id:int, cur):
    garbage_types = set([
        'papir', 'karton', 'plastika', 'metalna ambalaža', 'stiropor',
        'stare baterije', 'stakleni ambalažni otpad', 'ravno staklo',
        'PET - boce', 'PE - folija', 'limenke',
        'stari lijekovi', 'otpadne gume bez naplatka',
        'metalni glomazni otpad (električna i elektronička oprema)',
        'elektronički otpad', 'glomazni otpad',
        'drveni otpad', 'tekstil', 'odjeća',
        'akumulatore', 'fluorescentne cijevi', 'zeleni otpad',
        'otpadna motorna i jestiva ulja', 'kiseline', 'lužine',
        'ambalažu onečišćenu opasnim tvarima'
    ])
    if (kanta['prima'] not in garbage_types):
        return 1
    #check if the kanta exists
    cur.execute(f"SELECT id from kante where id = {kanta['id']}")
    if ( len(cur.fetchall()) == 1 ):
        query = f'''
            UPDATE kante
            SET prima = \'{kanta['prima']}\'
            where id = {kanta['id']}
        '''
        cur.execute(query)
    else:
        query = f'''
            INSERT INTO kante(id, id_dvorišta, prima)
            VALUES
            ({kanta['id']}, {rd_id}, \'{kanta['prima']}\')
        '''
        cur.execute(query)
    return 0

def update_rd(rd:dict):
    rd_attributes = set(["id", "ime", "adresa", "telefonski_broj", "četvrt", "radno_vrijeme", "geo_širina", "geo_dužina", "kante"])
    valid_districts = set([
        'Donji grad', 'Gornji grad - Medveščak',
        'Trnje', 'Maksimir', 'Peščenica – Žitnjak', 'Novi Zagreb - istok',
        'Novi Zagreb - zapad', 'Trešnjevka - sjever', 'Trešnjevka - jug',
        'Črnomerec', 'Gornja Dubrava', 'Donja Dubrava',
        'Stenjevec', 'Podsused - Vrapče', 'Podsljeme',
        'Sesvete', 'Brezovica'
    ])
    db_user = environ['KANTE_ZAGREB_USER']
    conn = psycopg2.connect(f"dbname=kante_zagreb user={db_user}")
    cur = conn.cursor()
    try:
        rd["id"]
    except KeyError:
        return 1
    cur.execute(f"SELECT id from reciklažna_dvorišta where id = {rd['id']}")
    if(len(cur.fetchall()) != 1):
        return 2

    query = f'''
    UPDATE reciklažna_dvorišta
    SET'''

    for attr in rd.keys():
        print(attr)
        if attr not in rd_attributes:
            return 3
        if (attr == "id"):
            continue
        elif (attr == "kante"):
            print("???")
            if (type(rd[attr]) != list):
                return 4.5
            for kanta in rd[attr]:
                print(kanta)
                ret = update_kanta(kanta, rd['id'], cur)
                if (ret != 0):
                    return 4
            continue
        elif (attr == "četvrt"):
            if (rd[attr] not in valid_districts):
                return 5
        query += f" {attr} = \'{rd[attr]}\',"
    if (query[:-1] == ','):
        query = query[:-1] #remove last ','
        query += f"\nWHERE id = {rd['id']}"
        ret = cur.execute(query)
        if (ret != None):
            curr.close()
            conn.close()
            return 6
    conn.commit()
    cur.close()
    conn.close()
    return 0

def create_rd(rd:dict):
    db_user = environ['KANTE_ZAGREB_USER']
    conn = psycopg2.connect(f"dbname=kante_zagreb user={db_user}")
    cur = conn.cursor()
    query = f'''
    INSERT INTO reciklažna_dvorišta (id, ime, adresa, telefonski_broj, četvrt, radno_vrijeme, geo_širina, geo_dužina) VALUES
    ({rd['id']}, \'{rd['ime']}\', \'{rd['adresa']}\', \'{rd['telefonski_broj']}\', \'{rd['četvrt']}\', \'{rd['radno_vrijeme']}\',
    {rd['geo_širina']}, {rd['geo_dužina']})
    ''' 
    try:
        cur.execute(query)
    except:
        cur.close()
        conn.close()
        return 1
    conn.commit()
    for kanta in rd['kante']:
        query = f'''
            INSERT INTO kante(id, id_dvorišta, prima)
            VALUES
            ({kanta['id']}, {rd['id']}, \'{kanta['prima']}\')
        '''
        try:
            cur.execute(query)
        except:
            cur.close()
            conn.close()
            return 1
    conn.commit()
    cur.close()
    conn.close()
    return 0

def delete_rd(rd_id):
    db_user = environ['KANTE_ZAGREB_USER']
    conn = psycopg2.connect(f"dbname=kante_zagreb user={db_user}")
    cur = conn.cursor()

    cur.execute(f"SELECT id from reciklažna_dvorišta where id={rd_id}")
    if (len(cur.fetchall()) == 0):
        return 1
    query = f'''
        DELETE FROM kante
        WHERE id_dvorišta={rd_id}
    '''
    try:
        cur.execute(query)
    except:
        cur.close()
        conn.close()
        return 1
    conn.commit()
    query = f'''
        DELETE FROM reciklažna_dvorišta
        WHERE id = {rd_id}
    '''
    try:
        cur.execute(query)
    except:
        cur.close()
        conn.close()
        return 1
    conn.commit()
    return 0

# @returns wrapped response, HTTP respnse code
def api(path:bytes, method:bytes, body_object:bytes=None) -> dict:
    path = unquote(path)
    path = path.removeprefix('/api/')
    if (method == b'GET'):
        if (path == "rds"):
            rds = get_all_rds()
            return json.dumps(wrap_response("OK", "Dobavi sva reciklažna dvorišta", rds)), 200
        elif (path.startswith("rd_by_id/")):
            id = None
            try:
                id = int(path[9:])
            except ValueError:
                return json.dumps(wrap_response("ERROR", f"ID reciklažnog dvorišta mora biti prirodan broj", "null")), 400
            finally:
                rd = get_rd(id)
                if (rd == None):
                    return json.dumps(wrap_response("ERROR", f"Ne postoji reciklažno dvorište s identifikatorom {id}", "null")), 404
                return json.dumps(wrap_response("OK", f"Dobavi reciklažno dvorište s identifikatorom {id}" , rd)), 200
        elif (path.startswith("rd_by_name/")):
            name = path[len("rd_by_name/"):]
            rd = get_rd_by_name(name)
            if (rd == None):
                return json.dumps(wrap_response("ERROR", f"Ne postoji reciklažno dvorište s imenom {name}", "null")), 404
            return json.dumps(wrap_response("OK", f"Dobavi reciklažno dvorište po imenu {name}", rd)), 200
        elif (path.startswith("rds_by_garbage_type/")):
            garbage_type = path[len("rds_by_garbage_type/"):]
            rds  = get_rds_by_garbage(garbage_type)
            if (rds == None):
                return json.dumps(wrap_response("ERROR", f"Ne postoje reciklažna dvorišta koja primaju {garbage_type}", "null")), 404
            return json.dumps(wrap_response("OK", f"Dobavi reciklažna dvorišta koja primaju otpad {garbage_type}", rds)), 200
        elif (path.startswith("rds_by_district/")):
            district = path[len("rds_by_district/"):]
            rds = get_rds_by_district(district)
            if (rds == None):
                return json.dumps(wrap_response("ERROR", f"Ne postoje reciklažna dvorišta koja se nalaze u {district}", "null")), 404
            return json.dumps(wrap_response("OK", f"Dobavi reciklažna dvorišta koja se nalaze u gradskoj četvrti {district}", rds)), 200
        else:
            return json.dumps(wrap_response("ERROR", f"Nevaljan URL", "null")), 404 
    elif (method == b'PUT'):
        if (path.startswith("rd")):
            rd = None
            try:
                rd = json.loads(body_object.decode("utf-8"))
            except json.decoder.JSONDecodeError:
                return json.dumps(wrap_response("ERROR", f"Neispravan json primljen", "null")), 400
            if (type(rd) != dict):
                return json.dumps(wrap_response("ERROR", f"Body ne smije biti lista", "null")), 400
            ret = update_rd(rd)
            if (ret != 0):
                return json.dumps(wrap_response("ERROR", f"Neuspješno ažuriranje", "null")), 400
            return json.dumps(wrap_response("OK", "Uspješno ažuriranje", "null")), 400
        else:
            return json.dumps(wrap_response("ERROR", f"Nevaljan URL", "null")), 404 
    elif (method == b'POST'):
        if (path.startswith("rd")):
            rd = None
            try:
                rd = json.loads(body_object.decode("utf-8"))
            except json.decoder.JSONDecodeError:
                return json.dumps(wrap_response("ERROR", f"Neispravan json primljen", "null")), 400
            if (type(rd) != dict):
                return json.dumps(wrap_response("ERROR", f"Body ne smije biti lista", "null")), 400
            ret = create_rd(rd)
            if (ret != 0):
                return json.dumps(wrap_response("ERROR", f"Neuspješno dodavanje", "null")), 400
            return json.dumps(wrap_response("OK", "Uspješno dodavanje", "null")), 400
        else:
            return json.dumps(wrap_response("ERROR", f"Nevaljan URL", "null")), 404 
    elif (method == b'DELETE'):
        if (path.startswith("rd/")):
            rd_id = None
            try:
                rd_id = int(path[3:])
            except ValueError:
                return json.dumps(wrap_response("ERROR", f"Id mora biti prirodan broj", "null")), 400
            ret = delete_rd(rd_id)
            if (ret != 1):
                return json.dumps(wrap_response("ERROR", f"Neuspješno brisanje", "null")), 404
            return json.dumps(wrap_response("OK", "Uspješno briasnje", "null")), 400
        else:
            return json.dumps(wrap_response("ERROR", f"Nevaljan URL", "null")), 404 

    else:
        return json.dumps(wrap_response("ERROR", f"Nije implementirano", "null")), 501


