import pymongo


def get_next_id(cur):
    return cur.find_one_and_update(filter={'_id': 'last_id'}, update={'$inc': {'value': 1}}, new=True)['value']

pwd = 'InsertHere'
client = pymongo.MongoClient(
    f"mongodb+srv://user-741:{pwd}@pastebincluster.opwxr.mongodb.net/PasteBin?retryWrites=true&w=majority",
    read_preference=pymongo.ReadPreference.SECONDARY_PREFERRED
    )
client_db = client["publicbin"]
client_col = client_db["texts"]


class Database:
    con: pymongo.collection.Collection

    def __init__(self):
        self.con = None
    
    def connect(self):
        if self.con:
            raise ValueError("Database already connected")
        client_db = client["publicbin"]
        self.con = client_db["texts"]

    def disconnect(self):
        if self.con is None:
            raise ValueError("Database isn't connected")
        self.con = None

    def create_texts(self):
        try:
            self.con.insert_one({'_id': 'last_id' , 'value': 0})
        except pymongo.errors.DuplicateKeyError:
            pass

    def drop_texts(self):
        self.con.drop()
            
    def insert_text(self, text: str):
        con = self.con

        return con.insert_one({'_id': get_next_id(con), 'text': text}).inserted_id

    def get_indexes(self):
        id = self.con.find_one({'_id': 'last_id'})['value']

        return 1, id

    def get_text(self, id: int):
        ret = self.con.find_one({'_id': id})

        if ret is None:
            return ret

        return ret['text']


if __name__ == "__main__":
    db = Database()

    db.connect()
    db.create_texts()

    print(db.insert_text("some text"))
    print(db.insert_text("some text 2"))

    print(db.get_indexes())

    text = db.get_text(5)
    print(text)

    if text is not None:
        db.drop_texts()

    db.disconnect()
    
    

