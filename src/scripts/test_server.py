import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()


class TokenReq(BaseModel):
    grant_type: str
    client_id: str | None
    client_secret: str | None
    username: str | None
    password: str | None


@app.post("/api/token")
def read_root(token_req: TokenReq):
    print(token_req.model_dump_json())

    return {
        "access_token": "ABCD",
        "token_type": "bearer",
        "expires_at": "2026-06-26T10:33:32+00:00",
    }


@app.get("/api/employee/list")
def asddd(access_token: str = Header(...)):
    print("Access token: " + access_token)
    return [
        {
            "id": "8c8c13b6-35ed-3ffb-92d5-c438825df67f",
            "date_of_birth": "1990-06-29",
            "image": "https://lorempixel.com/640/480/people/?96612",
            "email": "andres34@gmail.com",
            "first_name": "Dayni",
            "last_name": "Mayez",
            "title": "Mr.",
            "address": "18342 Alisa Square Suite 259",
            "country": "USA",
            "bio": "…",
            "rating": "3.0600000000000001",
        }
    ]


import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081, proxy_headers=True)
