import sqlite3 as sql


CREATE_TABLE = """
CREATE TABLE texts (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    text TEXT
);
"""
DROP_TABLE = "DROP TABLE texts"
INSERT = "INSERT INTO texts (text) values(?)"
GET_IDS = "SELECT id FROM texts"
GET_TEXT = "SELECT text FROM texts WHERE id=?"


class Database:
    con: sql.Connection

    def __init__(self):
        self.con = None
    
    def connect(self):
        if self.con:
            raise ValueError("Database already connected")
        self.con = sql.connect('texts.db')

    def disconnect(self):
        if self.con is None:
            raise ValueError("Database isn't connected")
        self.con.close()
        self.con = None

    def create_texts(self):
        con = self.con
        try:
            with con:
                con.execute(CREATE_TABLE)
        except sql.OperationalError:
            pass

    def drop_texts(self):
        con = self.con
        with con:
            con.execute(DROP_TABLE)
            
    def insert_text(self, text: str):
        con = self.con
        with con:
            con.execute(INSERT, (text,))

    def get_indexes(self):
        return [data[0] for data in self.con.execute(GET_IDS)]

    def get_text(self, id: int):
        ret = self.con.execute(GET_TEXT, (id,)).fetchone()

        return ret if ret is None else ret[0]


if __name__ == "__main__":
    db = Database()

    db.connect()
    db.create_texts()

    db.insert_text("some text")
    db.insert_text("some text 2")

    print(db.get_indexes())

    text = db.get_text(5)
    print(text)

    if text is not None:
        db.drop_texts()

    db.disconnect()
    
    

