from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from typing import List
import csv
import codecs
import pandas as pd
import folium 
from folium import plugins
import os
from tools import Data

PATH_OUT = 'res.png'
PATH_CSV = 'raw_data.csv'
PATH_MAP = 'map.html'
predict = Data()

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"])


@app.post("/upload_files")
async def upload(files: List[UploadFile] = File(...)):
    for file in files :
        csvReader = csv.DictReader(codecs.iterdecode(file.file, 'utf-8'))
        data = list(csvReader)
        predict.map(data)
        predict.get_predict()
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), PATH_CSV)
        os.remove(path)
        
        
@app.get("/get_out")
def get_out():    
    return FileResponse(PATH_OUT)    


@app.get("/get_map")
def get_map():    
    return FileResponse(PATH_MAP)