import dbf
import re
import os, sys
import tblstruct as ddl
import tocsv as tocsv

dbf_file_array = []

SQL_CREATE_TABLES = 'db_create.sql'
SQL_DROP_TABLES   = 'db_drop.sql'
SQL_FILL_TABLES   = 'db_fill.sql'

SERVER_DIR = 'D:\\\\work\\\\2mysql\\\\'


def readheaderdbf(name_dbf):
    table = dbf.Table(name_dbf)
    array_struct = []
    dbf_struct = table.structure()
    
    for s in dbf_struct:
        fld_lst = s.split()
        array_struct.append([ fld_lst[0], fld_lst[1][:1] ])
        if fld_lst[1].find('(') > -1:
            for k in re.split(',', re.search(  '\(([^)]+)', fld_lst[1] ).group(1)):
                array_struct[len(array_struct)-1].append(k)
        else:
           array_struct[len(array_struct)-1].append(0)    

    return array_struct
    
    
    
def createtablemysql(head_dbf, dbf_name):
    print("Запись скрипта создания копии файла ", dbf_name)
    
    table_name = os.path.splitext(os.path.basename(dbf_name))[0].upper()
    
    with open(SQL_CREATE_TABLES, 'a', encoding='utf-8') as f:
   
        f.write( ddl.HEAD_DDL.replace('%1', table_name) + '\n')
        curr_idx = 0
        for s in head_dbf:
            curr_idx = curr_idx+1
            if (curr_idx == len(head_dbf)):    
                f.write(ddl.getDDLfield(s)[:-1] + '\n')
            else:
                f.write(ddl.getDDLfield(s) + '\n') 
        
        f.write(ddl.FIN_DDL + '\n')
    f.close()
    
    with open(SQL_DROP_TABLES, 'a', encoding='utf-8') as f:
        f.write(ddl.DROP_DDL.replace('%1', table_name) + '\n')
    f.close()
    
    with open(SQL_FILL_TABLES, 'a', encoding='utf-8') as f:
        f.write(ddl.LOAD_STR.replace('%1', table_name).replace('%2', SERVER_DIR + table_name + '.csv') + '\n')
    f.close()



def main():
    if len (sys.argv) > 1:
        pathdbf = sys.argv[1]
        for file in os.listdir(pathdbf):
            if file.upper().endswith(".DBF"):
                dbf_file_array.append(os.path.join(pathdbf, file))
                
        if os.path.isfile(SQL_CREATE_TABLES):
            os.remove(SQL_CREATE_TABLES)
        if os.path.isfile(SQL_DROP_TABLES):
            os.remove(SQL_DROP_TABLES)    
        if os.path.isfile(SQL_FILL_TABLES):
            os.remove(SQL_FILL_TABLES)             
    else:
        print ("Использование: 2mysql.py <path-to-dbf>")
        sys.exit()
        
    for dbf_item in dbf_file_array: 
        tocsv.correct_codepage_dbf(dbf_item)
        
        print("Обработка dbf-таблицы ", dbf_item)    
        header_dbf = readheaderdbf(dbf_item)
        createtablemysql(header_dbf, dbf_item)
        
        print("Конвертация в csv ", dbf_item)
        tocsv.dbf_to_csv(dbf_item)
        
        primary_csv_file = dbf_item[:-4]+ ".csv"
        print("Установка значений по умолчанию в NULL в ", primary_csv_file)
        tocsv.replace_illegal_symbols_in_file(primary_csv_file )
    

if __name__ == "__main__":
    main()