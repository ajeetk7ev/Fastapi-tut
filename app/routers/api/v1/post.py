from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from config.db import get_db
from controllers.post.post import create_post, get_post_by_id, get_posts, update_post, delete_post
from schemas.post import PostCreate, PostResponse, PostUpdate
from utils.response import success_response

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post_route(
    post_data: PostCreate,
    db: Session = Depends(get_db),
):
    post = create_post(db, post_data)

    response_data = PostResponse.model_validate(post)

    return success_response(
        message="Post created successfully",
        data=response_data,
        status_code=status.HTTP_201_CREATED,
    )


@router.get("/")
def get_posts_route(
    db: Session = Depends(get_db),
):
    posts = get_posts(db)

    response_data = [
        PostResponse.model_validate(post)
        for post in posts
    ]

    return success_response(
        message="Posts fetched successfully",
        data=response_data,
        status_code=status.HTTP_200_OK,
    )


@router.get("/{post_id}")
def get_post_by_id_route(
    post_id: int,
    db: Session = Depends(get_db),
):
    post = get_post_by_id(db, post_id)

    return success_response(
        message="Post fetched successfully",
        data=PostResponse.model_validate(post),
        status_code=status.HTTP_200_OK,
    )


@router.patch("/{post_id}", status_code=status.HTTP_200_OK)
def update_post_route(
    post_id: int,
    post_data: PostUpdate,
    db: Session = Depends(get_db),
):
    post = update_post(db, post_id, post_data)

    return success_response(
        message="Post updated successfully",
        data=PostResponse.model_validate(post),
        status_code=status.HTTP_200_OK,
    )


@router.delete("/{post_id}", status_code=status.HTTP_200_OK)
def delete_post_route(
    post_id: int,
    db: Session = Depends(get_db),
):
    deleted_id = delete_post(db, post_id)

    return success_response(
        message="Post deleted successfully",
        data={"id": deleted_id},
        status_code=status.HTTP_200_OK,
    )
