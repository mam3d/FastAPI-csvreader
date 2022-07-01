
import pandas as pd
from fastapi import (
            FastAPI,
            UploadFile,
            BackgroundTasks,
            Response,
            HTTPException,
            )
from pymongo import MongoClient


client = MongoClient("mongodb://mongodb:27017/")
db = client["mydatabase"]
collection = db["csv"]

app = FastAPI()


def csv_to_mongo(file):
    df = pd.read_csv(file.file)
    collection.insert_many(df.to_dict("records"))


@app.post("/",status_code=202)
def home(file: UploadFile, backgroundtask: BackgroundTasks):
    if file.content_type == "text/csv":
        backgroundtask.add_task(csv_to_mongo, file)
        return Response(status_code=202)
    raise HTTPException(status_code=400, detail="we can only support csv files")


@app.get("/")
def home():
    return list(collection.find({},{"_id":False}))


@app.delete("/")
def home():
    collection.delete_many({})