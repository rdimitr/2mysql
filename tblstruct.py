DROP_DDL = 'DROP TABLE IF EXISTS %1;'

HEAD_DDL = 'CREATE TABLE IF NOT EXISTS %1 ('

DDL = {
    'I': '%1 INT,', 
    'C': '%1 VARCHAR(%2),', 
    'F': '%1 FLOAT(%2,%3),', 
    'D': '%1 DATETIME,', 
}

FIN_DDL  = ');'

LOAD_STR = '''LOAD DATA INFILE \'%2\' 
INTO TABLE %1 
CHARACTER SET UTF8
FIELDS TERMINATED BY \'#\' 
ENCLOSED BY \'\"\' 
LINES TERMINATED BY \'\\r\\n\' 
IGNORE 1 ROWS;\n'''


def getDDLfield(fld_array):
    if fld_array[1] == 'N' and fld_array[3] == '0': 
        str_ddl = DDL['I'].replace('%1', fld_array[0])
    elif fld_array[1] == 'N' and fld_array[3] != '0':
        str_ddl = DDL['F'].replace('%1', fld_array[0]).replace('%2', fld_array[2]).replace('%3', fld_array[3])
    elif fld_array[1] == 'C':
        str_ddl = DDL['C'].replace('%1', fld_array[0]).replace('%2', fld_array[2])
    elif fld_array[1] == 'D':
        str_ddl = DDL['D'].replace('%1', fld_array[0])
    else:
        str_ddl = DDL[fld_array[1]]

    return str_ddl
    