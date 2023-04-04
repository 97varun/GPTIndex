
from fastapi import FastAPI, BackgroundTasks
from fastapi import status

import json_schema as schema

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/query", status_code=status.HTTP_200_OK)
def get_gptindex_response(PromptPayload: schema.PromptPayload):

    query = PromptPayload.query
    print(query)
    # call function

    # return response

if __name__ == "__main__":
    # initialize class
    # process documents
    pass