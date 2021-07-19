import csv
import os
from dbfread import DBF
import dbf


def correct_codepage_dbf(fName):
    table = dbf.Table(fName)
    table.open(mode=dbf.READ_WRITE)
    cp=str(table.codepage)
    print("Кодовая страница таблицы {filename} - {cp}".format(filename=fName, cp=cp))
    if cp.find('cp866') == -1:
        print("Кодовая страница таблицы {filename} отличается от cp866. Преобразование...".format(filename=fName))
        table.codepage = dbf.CodePage('cp866')
    table.close()


def dbf_to_csv(dbf_table_pth):
    csv_fn = dbf_table_pth[:-4]+ ".csv" 
    table = DBF(dbf_table_pth)
    with open(csv_fn, 'w', newline = '', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='#', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(table.field_names) 
        #i = 0
        
        for record in table:
            #i = i+1
            lst = list(record.values())
            for j in range(len(lst)):
                if isinstance(lst[j], str):
                    lst[j] = lst[j].replace('"', '\'')
            #for j in s:
             #   if isinstance(j, str):
              #      j = j.replace('"', '\'')
               #     print(j)
            #print(s)
            #writer.writerow( list(record.values()) )
            writer.writerow( lst )
            #if i>10:
            #    return
    return csv_fn
    
    
    
def replace_illegal_symbols_in_file(input_file_name):
    new_file_name = input_file_name + '.new';
    with open(input_file_name, 'r', encoding='utf-8') as f1:
        with open(new_file_name, 'w', encoding='utf-8') as f2:
            for line in f1:
                f2.write(line.replace('""', '\\N').replace('\"\\\"', '\\N').replace('\\\\\"', '\"').replace('\\\"', '\"'))
    f1.close()
    f2.close()
    os.remove(input_file_name)
    os.rename(new_file_name, input_file_name)
    return new_file_name