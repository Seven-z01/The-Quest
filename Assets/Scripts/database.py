import sqlite3

from .manager import DB_FILE, TBL_NAME, SQL, MEMORY_LIST


class Database():
    db_file = DB_FILE
    table = TBL_NAME
    sql = SQL
    memory_list = MEMORY_LIST

    def init_table(self):
        self.crud_query(f'''CREATE TABLE {self.table} {self.sql}''')
        self.create_data('', 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0.5, 0.5, 800, 800, 1, self.memory_list)

    def crud_query(self, query, *args):
        cnn = sqlite3.connect(self.db_file) # Create the database or connect to it
        cur = cnn.cursor() # Create cursor
        try:
            if args != (): cur.executemany(query, *args) # Make the query list
            else: cur.execute(query) # Make the query
        except sqlite3.OperationalError as error:
            self.init_table()
            # print(error)
        finally:
            self.data = cur.fetchall() # Search the data
            cnn.commit() # Commit changes
            cnn.close()  # Close connection

    def create_data(self, username='', style=0, model=0, weapon=1, level=1, highlevel=1, score=0, highscore=0, enemy=0, T_enemy=0, meteor=0, T_meteor=0, music=0.5, sound=0.5, screen_w=800, screen_h=800, play=1, *args):
        if args != ():
            mul = '?,' * len(self.memory_list[0])
            self.crud_query(f'INSERT INTO {self.table} VALUES ({mul[:-1]})', *args)
        else:
            self.crud_query(f'INSERT INTO {self.table} VALUES ("{username}", {style}, {model}, {weapon}, {level}, {highlevel}, {score}, {highscore}, {enemy}, {T_enemy}, {meteor}, {T_meteor}, {music}, {sound}, {screen_w}, {screen_h}, {play})')

    def read_data(self, field=None, tidy=None):
        if tidy!= None:
            self.crud_query(f'SELECT * FROM {self.table} ORDER BY {field} ASC LIMIT {tidy}')
        elif field != None:
            self.crud_query(f'SELECT * FROM {self.table} WHERE USERNAME like "{field}"')
        else:
            self.crud_query(f'SELECT * FROM {self.table}')

        return self.data

    def update_data(self, username, **kwargs):
        query = list(kwargs.items())[0]
        self.crud_query(f'UPDATE {self.table} SET {query[0].upper()}={query[1]} WHERE USERNAME like "{username}"')

    def delete_data(self, username):
        self.crud_query(f'DELETE FROM {self.table} WHERE USERNAME like "{username}"')
