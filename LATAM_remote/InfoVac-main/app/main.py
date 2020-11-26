from fastapi import FastAPI
from pydantic import BaseModel

import uvicorn
from src.models.predict_model import predict, explain

app = FastAPI()


class Input(BaseModel):
    text : str


@app.get("/")
def main():
    return 'InfoVac.AI'


@app.post("/predict/{Input}")
def predict_(input: Input):
    probas = predict([input.text]).round(3)
    response = {'texto': input.text,
            'proba_no_confiable': probas[0, 0],
            'proba_confiable': probas[0, 1]}

    return response


@app.post("/explain/{Input}")
def explain_(input: Input):
    return explain([input.text])


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8001)
#

# To run in terminal
#uvicorn app:app --port 8001 --reload
# docker run -p 8001:8001 infovac-app