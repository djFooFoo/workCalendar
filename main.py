import fastapi

app = fastapi.FastAPI()


@app.get("/hi")
async def sit():
    return "hello world"
