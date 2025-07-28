from fastapi import FastAPI
from .routes import plans

app = FastAPI(title="ZubaSchool Subscription Management Service")

app.include_router(plans.router, prefix="/plans")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}