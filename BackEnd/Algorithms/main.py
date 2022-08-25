import json
from multiprocessing.dummy import Array
from typing import Container, List, Union

from fastapi import FastAPI, Request
from pip import main
from pydantic import BaseModel
from pyparsing import string
import mainApiConnector as mc
from fastapi.middleware.cors import CORSMiddleware
class HSSP (BaseModel):
    Amount : int
    Weights : list = []
class SSP (BaseModel):
    Amount : int
    Weights : list = []
class SMP (BaseModel):
    Amount : int
    Weights : list = []
class MP (BaseModel):
    Amount : int
    Weights : list = []
class MLP (BaseModel):
    Amount : int
    Weights : list = []
class LP (BaseModel):
    Amount : int
    Weights : list = []
class LHP (BaseModel):
    Amount : int
    Weights : list = []
class ETC (BaseModel):
    Amount : int
    Weights : list = []
class ContainerType(BaseModel) :
    Type : list = []
app = FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/test/getInformation")
async def read_test(HSSP: HSSP, SMP : SMP, SSP : SSP, MP: MP, MLP : MLP, LP: LP,  LHP : LHP, ETC : ETC, ContainerType: ContainerType):
    hssp_box = mc.hssp(HSSP.Amount, HSSP.Weights)
    ssp_box = mc.ssp(SSP.Amount, SSP.Weights)
    smp_box = mc.smp(SMP.Amount, SMP.Weights)
    mp_box = mc.mp(MP.Amount, MP.Weights)
    mlp_box = mc.mlp(MLP.Amount, MLP.Weights)
    lp_box = mc.lp(LP.Amount, LP.Weights)
    lhp_box = mc.lhp(LHP.Amount, LHP.Weights)
    etc_box = mc.etc(ETC.Amount, ETC.Weights)
    boxes = mc.Boxes(smp=smp_box, ssp=ssp_box, mp=mp_box, mlp=mlp_box, lp=lp_box, lhp=lhp_box, etc=etc_box)
    if (HSSP.Amount + SSP.Amount + SMP.Amount + MP.Amount + MLP.Amount + ETC.Amount + LP.Amount + LHP.Amount) < 24:
        return {"Error" : "Not Enough Parcels To Be Built As a Pattern."}
    json_result = mc.execute(
        hssp_amount=HSSP.Amount,
        hssp_weights=HSSP.Weights,
        ssp_amount=SSP.Amount,
        ssp_weights=SSP.Weights,
        smp_amount=SMP.Amount,
        smp_weights=SMP.Weights,
        mp_amount=MP.Amount,
        mp_weights=MP.Weights,
        lp_amount=LP.Amount,
        lp_weights=LP.Weights,
        lhp_amount=LHP.Amount,
        lhp_weights=LHP.Weights,
        mlp_amount=MLP.Amount,
        mlp_weights=MLP.Weights,
        etc_amount=ETC.Amount,
        etc_weights=ETC.Weights, 
        container_type=ContainerType.Type
    )
    result = {
        "Container" : [[{
            "Type" : "Small",
            "Weight" : 2238,
            "Container" : [
                [101, 102, 103],
                [101, 102, 103],
                [101, 102, 103],
                [101, 102, 103],
                [101, 102, 103],
                [101, 102, 103],
                [101, 102, 103],
                [101, 102, 103],
                [101, 102, 103],
                [101, 102, 103],
                [101, 102, 103],
            ]
        }], 
        [{
            "Type" : "Large",
            "Weight" : 2238,
            "Container" : [
                [101, 102, 103],
                [101, 102, 103],
                [101, 102, 103],
                [101, 102, 103],
                [101, 102, 103],
                [101, 102, 103],
                [101, 102, 103],
                [101, 102, 103],
                [101, 102, 103],
                [101, 102, 103],
                [101, 102, 103],
            ]
        }]] 
    }
    return json_result