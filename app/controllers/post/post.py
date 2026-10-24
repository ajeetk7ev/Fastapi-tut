from sqlalchemy.orm import Session

from core.exceptions import AppException
from models.post import Post
from schemas.post import PostCreate, PostUpdate


def create_post(db: Session, post_data: PostCreate) -> Post:
    post = Post(**post_data.model_dump())

    try:
        db.add(post)
        db.commit()
        db.refresh(post)
        return post
    except Exception:
        db.rollback()
        raise


def get_posts(db: Session) -> list[Post]:
    return db.query(Post).order_by(Post.id.desc()).all()


def get_post_by_id(db: Session, post_id: int) -> Post:
    post = db.query(Post).filter(Post.id == post_id).first()

    if post is None:
        raise AppException(
            message="Post not found",
            status_code=404,
            errors={"post_id": f"No post exists with ID {post_id}"},
        )

    return post


def update_post(
    db: Session,
    post_id: int,
    post_data: PostUpdate,
) -> Post:
    post = get_post_by_id(db, post_id)
    update_data = post_data.model_dump(exclude_unset=True)

    if not update_data:
        raise AppException(
            message="No fields provided",
            status_code=400,
            errors={"body": "Provide at least one field to update"},
        )

    if any(value is None for value in update_data.values()):
        raise AppException(
            message="Invalid update data",
            status_code=422,
            errors={"body": "Fields cannot be null"},
        )

    try:
        for field, value in update_data.items():
            setattr(post, field, value)

        db.commit()
        db.refresh(post)
        return post

    except Exception:
        db.rollback()
        raise


def delete_post(db: Session, post_id: int) -> int:
    post = get_post_by_id(db, post_id)

    try:
        db.delete(post)
        db.commit()
        return post_id

    except Exception:
        db.rollback()
        raise
