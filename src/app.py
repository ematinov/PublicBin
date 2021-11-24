from fastapi import FastAPI, HTTPException

from database import Database
from models import Text, TextWithId


app = FastAPI()
db = Database()


def jsonify(**data):
    return data


@app.on_event("startup")
def startup():
    db.connect()
    db.create_texts()

@app.on_event("shutdown")
def shutdown():
    db.disconnect()

@app.get("/indexes")
def get_indexes():
    first_id, last_id = db.get_indexes()
    return jsonify(first_id=first_id, last_id=last_id)

@app.get("/texts/{item_id}", response_model=TextWithId)
def read_text(item_id: int):
    text = db.get_text(item_id)

    if text is None:
        raise HTTPException(status_code=404, detail="The required text details not found")

    return jsonify(id=item_id, text=text)

@app.post("/texts", response_model=TextWithId)
def write_text(text: Text):
    text = text.text
    id = db.insert_text(text)
    return jsonify(id=id, text=text)
    