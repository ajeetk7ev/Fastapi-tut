from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from schemas import PostCreate
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from datetime import date
app = FastAPI()

posts:list[dict] =  [
    {
        "id": 1,
        "author": "Ajeet Kumar",
        "title": "Getting Started with Python",
        "content": "Python is a beginner-friendly programming language used for web development, automation, data science, and AI.",
        "date_posted": "2026-10-01"
    },
    {
        "id": 2,
        "author": "Rahul Sharma",
        "title": "Why Learn Data Structures and Algorithms?",
        "content": "Data structures and algorithms help developers solve complex problems efficiently and prepare for technical interviews.",
        "date_posted": "2026-10-03"
    },
    {
        "id": 3,
        "author": "Priya Singh",
        "title": "Introduction to Web Development",
        "content": "Web development involves building websites and web applications using technologies like HTML, CSS, JavaScript, and React.",
        "date_posted": "2026-10-05"
    },
    {
        "id": 4,
        "author": "Amit Verma",
        "title": "The Importance of Consistency",
        "content": "Consistent practice and continuous learning are essential for improving programming skills and becoming a better developer.",
        "date_posted": "2026-10-08"
    },
    {
        "id": 5,
        "author": "Neha Gupta",
        "title": "Understanding REST APIs",
        "content": "REST APIs allow different applications to communicate over HTTP using methods such as GET, POST, PUT, PATCH, and DELETE.",
        "date_posted": "2026-10-10"
    },
    {
        "id": 6,
        "author": "Rohit Patel",
        "title": "Getting Started with MongoDB",
        "content": "MongoDB is a NoSQL database that stores data in flexible, JSON-like documents called BSON documents.",
        "date_posted": "2026-10-12"
    },
    {
        "id": 7,
        "author": "Sneha Mishra",
        "title": "Tips for Learning React",
        "content": "Learn React components, props, state, event handling, hooks, and component composition to build interactive user interfaces.",
        "date_posted": "2026-10-15"
    },
    {
        "id": 8,
        "author": "Vikas Yadav",
        "title": "Introduction to Git and GitHub",
        "content": "Git helps developers track code changes, while GitHub makes it easier to collaborate and manage projects remotely.",
        "date_posted": "2026-10-18"
    },
    {
        "id": 9,
        "author": "Ananya Roy",
        "title": "Why Is Database Design Important?",
        "content": "Good database design reduces data duplication, maintains consistency, and improves the performance of applications.",
        "date_posted": "2026-10-20"
    },
    {
        "id": 10,
        "author": "Karan Mehta",
        "title": "Building Your First Backend",
        "content": "Start building backend applications by learning routing, middleware, validation, authentication, error handling, and database integration.",
        "date_posted": "2026-10-22"
    }
]


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    errors = {}

    for error in exc.errors():
        field = str(error["loc"][-1])
        error_type = error["type"]
        ctx = error.get("ctx", {})

        if error_type == "missing":
            message = f"{field} is required"

        elif error_type == "string_too_short":
            message = (
                f"{field} must be at least "
                f"{ctx.get('min_length')} characters"
            )

        elif error_type == "string_too_long":
            message = (
                f"{field} must not exceed "
                f"{ctx.get('max_length')} characters"
            )

        elif error_type == "greater_than":
            message = f"{field} must be greater than {ctx.get('gt')}"

        elif error_type == "less_than":
            message = f"{field} must be less than {ctx.get('lt')}"

        else:
            message = f"Invalid value for {field}"

        errors[field] = message

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Validation error",
            "errors": errors
        }
    )

@app.get("/")
def read_root():
    return {"Hello": "World from Windows"}


@app.post("/api/v1/posts")
def create_post(post:PostCreate):
    new_post = post.model_dump()

    new_post["id"] = len(posts) + 1
    posts.append(new_post)

    
    return JSONResponse(
        status_code=201,
        content=jsonable_encoder({
            "success" : True,
            "message":"Post created",
            "data":posts[len(posts)-1]
        })
    )

@app.get("/api/v1/posts")
def get_posts():
   return JSONResponse(
        status_code=200,
        content=jsonable_encoder({
            "success": True,
            "message": "Posts fetched successfully",
            "data": posts
        })
    )
   

@app.get("/api/v1/posts/{id}")
def get_post(id:int):
    for post in posts:
        if post.get("id") == id:
            return JSONResponse(
                    status_code=200,
                    content=jsonable_encoder({
                        "success": True,
                        "message": "Posts fetched successfully",
                        "data": post
                    })
                )
            
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "message": "Post not found",
            "data": None
        }
    )