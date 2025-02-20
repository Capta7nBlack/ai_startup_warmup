from fastapi import FastAPI, HTTPException, Response, Request, Cookie
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


from entities import RentInstrumentRequest, ReturnInstrumentRequest, CreateInstrumentRequest
from entities import InstrumentStatusResponse, AvailableInstrumentResponse

from db import DatabaseOperations

from helper import generate_user_id, initialize_user


app = FastAPI()
db_ops = DatabaseOperations()




@app.get("/init")
def init_user(response: Response):
    user_id = initialize_user(response)
    return {"message": "User initialized", "user_id": user_id}




@app.post("/rent")
def rent_instrument(request: RentInstrumentRequest, response: Response, user_id: str = Cookie(None)):
    if not user_id:
        user_id = initialize_user(response)


    try:
        result = db_ops.rented(request.user_id, request.instrument_id, request.instrument_name)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))



@app.post("/return")
def return_instrument(request: ReturnInstrumentRequest, response: Response, user_id: str = Cookie(None)):

    if not user_id:
        user_id = initialize_user(response)


    try:
        result = db_ops.returned(request.user_id, request.instrument_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))



@app.post("/instruments")
def create_instrument(request: CreateInstrumentRequest):
    try:
        result = db_ops.create_instrument(request.instrument_name)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/instruments/{instrument_id}/status")
def get_instrument_status(instrument_id: int):
    try:
        result = db_ops.get_instrument_status(instrument_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/instruments/available", response_model=list[AvailableInstrumentResponse])
def get_available_instruments():
    try:
        available_instruments = db_ops.get_available_instruments()
        return available_instruments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
