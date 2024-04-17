from fastapi import FastAPI
import uvicorn
from fastapi.staticfiles import StaticFiles
import os
from Api.Routes.usersRoutes import userRoutes
from Api.Routes.defaultRoute import defaultRoute
from Api.Routes.tendersDataCleaningRoutes import tendersDataCleanRoutes
from Api.Routes.tendersCreatingEmbeddingsRoutes import tendersCreateEmbeddingRoutes
from Api.constant.constants import GOOGLE_API_KEY
from fastapi.middleware.cors import CORSMiddleware
os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY
app = FastAPI(title="FastAPI-Users-Backend",description = "CRUD API")

app.mount("/static", StaticFiles(directory="static"), name="static")
origins = ["*"] 

# Add CORS middleware to the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(userRoutes,tags=['Users'], prefix='/api/users')
app.include_router(defaultRoute)
app.include_router(tendersDataCleanRoutes)
app.include_router(tendersCreateEmbeddingRoutes)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)


