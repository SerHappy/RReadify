from fastapi import FastAPI

from app.schemas.user import UserInput

app = FastAPI()


@app.get("/")
def hello_world(data: UserInput) -> dict[str, str]:
    """Stub function to test the API is working."""
    return {"message": "Hello World"}
