from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from uber import getAllStoresSTATUS as getUberStatus
from deliveroo import getAllStoresSTATUS as getDeliverooStatus

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RestaurantStatusModel(BaseModel):
    deliverooBrandId: str


@app.post("/getAllVendorsStatus")
async def getAllStatus(data: RestaurantStatusModel):
    return {'uber': getUberStatus(), 'deliveroo': getDeliverooStatus(data.deliverooBrandId)}
