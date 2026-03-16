from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import requests


app = FastAPI(title="CURRENCY CONVERTER API",
    description="API for converting currencies using exchange rates",
    version="1.0.0"
)

templates = Jinja2Templates(directory="templates")

API_KEY = "442fb08f2d37da7167e35054"

@app.get("/convert" )
def home(request: Request):
    return templates.TemplateResponse(
        "index.html" , {"request": request})



@app.post("/convert")
def convert(request: Request,
            amount: float = Form(...),
            from_currency: str = Form(...),
            to_currency: str = Form(...)):

    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{from_currency}"

    try:
        response = requests.get(url).json()
        rate = response["conversion_rates"][to_currency]
        result = round(amount * rate, 2)
    except Exception as e:
        result = f"Error: {e}"

    return templates.TemplateResponse("index.html", {"request": request, "result": result})
