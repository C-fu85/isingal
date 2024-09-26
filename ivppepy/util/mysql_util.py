import mysql.connector
from ivppepy.util import util

class MysqlIO :
    def __init__(self, db_info=None):
        self.conn = self.get_db_connection(db_info['host'], db_info['port'], db_info['user'], db_info['pwd'], db_info['db'])
        self.cursor = None

    def get_db_connection(self, host='', port='', user='root', password='', db=''):
        conn = mysql.connector.connect(user=user, passwd=password, host=host, database=db, charset='utf8')
        return conn    

    def get_cursor_dict_type(self, conn):
        return conn.cursor(dictionary=True)

    def get_cursor_exec(self, conn):
        return conn.cursor()    

    def db_close(self, conn = None, cursor = None):
        if self.cursor :
            self.cursor.close()
        if self.conn:
            self.conn.close()


    def get_row_by_query(self, query, only_one = False) :
        conn = self.conn
        self.cursor = cursor = self.get_cursor_dict_type(conn)
        cursor.execute(query.replace("\\",""))
        result = cursor.fetchall()
        if only_one and len(result) == 1 :
            return result[0]
        else :
            return result
        
    def insert_by_dict(self, table_name, rows, commit_size=20000):
        cursor = self.get_cursor_exec(self.conn)
            
        for row_num, row_dict in enumerate(rows):            
            if 'is_delete' not in row_dict:
                row_dict['is_delete'] = 0
            if 'ivp_create_time' not in row_dict:
                row_dict['ivp_create_time'] = None
            row_dict['ivp_create_time'] = util.get_datetime_now()
            
            field_list = list(row_dict.keys())
            
            str1 = ",".join(list(map(lambda x: "`%s`"%(x,), field_list)))
            str2 = ",".join(['%s']*len(field_list))
            _tuple = tuple(list(map(lambda x: str(row_dict[x]), field_list)))
                            
            sqlstr = "INSERT INTO %s (%s) VALUES (%s)"%( \
                table_name, str1, str2)
            cursor.execute(sqlstr, _tuple)
        
            if row_num % commit_size == commit_size - 1:
                self.conn.commit()
        self.conn.commit()
        
    def truncate_table(self, table_name):
        conn = self.conn
        self.cursor = cursor = self.get_cursor_exec(conn)
        sqlstr = "TRUNCATE %s;"%(table_name,)
        cursor.execute(sqlstr)
        conn.commit()
        
    def insert_a_row(self, sqlstr):
        conn = self.conn
        self.cursor = cursor = self.get_cursor_exec(conn)
        cursor.execute(sqlstr)
        conn.commit()
        
        return True    