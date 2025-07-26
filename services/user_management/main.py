from fastapi import FastAPI
from .routes.tenants import router as tenants_router

app = FastAPI(title="ZubaSchool User Management Service")

app.include_router(tenants_router, prefix="/tenants")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}