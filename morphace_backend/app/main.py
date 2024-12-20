from fastapi import FastAPI
from app.routers import user, sensor, habits, products


app = FastAPI()

app.include_router(user.router)
app.include_router(sensor.router)
app.include_router(habits.router)
app.include_router(products.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Morphace Backend"}
