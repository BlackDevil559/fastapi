from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
DATAGOVINDIA_API_KEY="579b464db66ec23bdd0000019b19496dc32649b35ab212cccf54971a"
from datagovindia import DataGovIndia
from urllib.parse import parse_qs
import json
datagovin = DataGovIndia(DATAGOVINDIA_API_KEY)
datagovin.sync_metadata()
app =FastAPI()
origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/query/{parameter}")
def search(parameter):
    search_data = datagovin.search(parameter)
    return (search_data)
@app.get("/filters/{id}")
def get_filters(id):
    k = datagovin.get_resource_info(id)
    filter = k["field"]
    return filter
@app.get("/database/{id}")
def final_data(id: str, request: Request):
    raw_query_params = request.query_params
    print(raw_query_params)
    data = datagovin.get_data(id, filters=raw_query_params)
    json_data = data.to_json(orient='records')
    return json_data
