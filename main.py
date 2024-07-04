from typing import Optional
from fastapi import FastAPI, Request, Query
from fastapi.responses import JSONResponse
import requests

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/api/hello")
async def hello(request: Request, visitor_name: str = Query(..., alias='visitor_name')):
    url = "https://api.geoapify.com/v1/ipinfo?apiKey=1b12fda6b84d4f658f751913397c291f"

    response = requests.get(url)
    message = response.json()

    client_ip = message['ip']
    location = message["city"]["name"]
    latitude = message['location']['latitude']
    longitude = message['location']['longitude']

    key = 'f1a9d0152acc4c86be2067de2f512b79'
    temp_url = f'https://api.weatherbit.io/v2.0/current?lat={latitude}&lon={longitude}&key={key}'

    try:
        result = requests.get(temp_url).json()
    except:
        return JSONResponse(status_code=500, content={"error": "Failed to fetch temperature"})

    temperature = result['data'][0]['temp']

    greeting = f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {location}"

    return JSONResponse({
        "client_ip": client_ip,
        "location": location,
        "greeting": greeting
    })

