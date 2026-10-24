from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from config.db import Base, engine
from models.post import Post
from config.env import env
from routers.api.v1.post import router as post_router

from core.exception_handlers import register_exception_handlers, AppException

app = FastAPI()
register_exception_handlers(app)
Base.metadata.create_all(bind=engine)


@app.get("/health")
def health_route():
    return JSONResponse(
        status_code=200,
        content={
            "success":True,
            "message":f"Server is running properly {env.PORT}"
            
        }
    )
    
@app.get("/test-error")
def test_error():
    raise AppException(
        message="Post not found",
        status_code=status.HTTP_404_NOT_FOUND,
        errors={"post_id": "No post exists with ID 99"},
    )
    
app.include_router(post_router, prefix="/api/v1")