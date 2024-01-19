from fastapi import FastAPI
from routers import auth_router, user_router, job_router, response_router
import uvicorn
from config import server_settings

app = FastAPI()
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(job_router)
app.include_router(response_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host=server_settings.host, port=server_settings.port, reload=True
    )
