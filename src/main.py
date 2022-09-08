import fastapi

app = fastapi.FastAPI()


@app.get("/events/today")
async def list_today_events():
    events = []
    return events
