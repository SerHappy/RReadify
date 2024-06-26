from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def hello_world() -> dict[str, str]:
    """Stub function to test the API is working."""
    return {"message": "Hello World"}
