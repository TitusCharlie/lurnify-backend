# from fastapi import APIRouter, Depends
# from sqlmodel import Session
# from typing import List
# from app.core.dependencies import get_current_user
# from app.core.database import get_session
# from app.services.community import (
#     create_community, list_communities, join_community,
#     create_post, get_feed
# )
# from app.schemas.community import (
#     CommunityCreate, CommunityRead,
#     PostCreate, PostRead, MembershipRead
# )
# from app.models.user import User


# router = APIRouter(
#     prefix="/community",
#     tags=["Community"]
# )


# @router.post("/", response_model=CommunityRead)
# def create_new_community(
#     data: CommunityCreate,
#     session: Session = Depends(get_session),
#     user: User = Depends(get_current_user),
# ):
#     return create_community(session, user, data)


# @router.get("/", response_model=List[CommunityRead])
# def get_all_communities(session: Session = Depends(get_session)):
#     return list_communities(session)


# @router.post("/{community_id}/join", response_model=MembershipRead)
# def join_existing_community(
#     community_id: str,
#     session: Session = Depends(get_session),
#     user: User = Depends(get_current_user),
# ):
#     return join_community(session, user, community_id)


# @router.post("/{community_id}/posts", response_model=PostRead)
# def create_community_post(
#     community_id: str,
#     data: PostCreate,
#     session: Session = Depends(get_session),
#     user: User = Depends(get_current_user),
# ):
#     return create_post(session, user, community_id, data)


# @router.get("/feed", response_model=List[PostRead])
# def get_user_feed(
#     session: Session = Depends(get_session),
#     user: User = Depends(get_current_user),
# ):
#     return get_feed(session, user)

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.community import Community, Membership, Post
from app.schemas.community import (
    CommunityCreate, CommunityRead,
    MembershipRead, PostCreate, PostRead
)
from app.services.community import (
    create_community_service,
    join_community_service,
    leave_community_service,
    create_post_service,
    get_feed_service
)
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/community",
    tags=["Community"]
)

# --- Community Endpoints ---
@router.post("/", response_model=CommunityRead)
def create_community(data: CommunityCreate, db: Session = Depends(get_session), user: User = Depends(get_current_user)):
    return create_community_service(db, data, user)

@router.get("/", response_model=list[CommunityRead])
def list_communities(db: Session = Depends(get_session)):
    return db.exec(select(Community)).all()

@router.get("/{id}", response_model=CommunityRead)
def get_community(id: str, db: Session = Depends(get_session)):
    community = db.get(Community, id)
    if not community:
        raise HTTPException(404, "Community not found")
    return community

@router.delete("/{id}")
def delete_community(id: str, db: Session = Depends(get_session), user: User = Depends(get_current_user)):
    # only owner can delete
    community = db.get(Community, id)
    if not community or community.creator_id != user.id:
        raise HTTPException(403, "Not allowed")
    db.delete(community)
    db.commit()
    return {"message": "Community deleted"}

# --- Membership ---
@router.post("/{id}/join", response_model=MembershipRead)
def join_community(id: str, db: Session = Depends(get_session), user: User = Depends(get_current_user)):
    return join_community_service(db, id, user)

@router.post("/{id}/leave")
def leave_community(id: str, db: Session = Depends(get_session), user: User = Depends(get_current_user)):
    return leave_community_service(db, id, user)

@router.get("/{id}/members", response_model=list[MembershipRead])
def list_members(id: str, db: Session = Depends(get_session)):
    return db.exec(select(Membership).where(Membership.community_id == id)).all()

# --- Posts ---
@router.post("/{id}/posts", response_model=PostRead)
def create_post(id: str, data: PostCreate, db: Session = Depends(get_session), user: User = Depends(get_current_user)):
    return create_post_service(db, id, data, user)

@router.get("/{id}/posts", response_model=list[PostRead])
def list_posts(id: str, db: Session = Depends(get_session)):
    return db.exec(select(Post).where(Post.community_id == id)).all()

# --- Feed ---
@router.get("/feed", response_model=list[PostRead])
def get_feed(db: Session = Depends(get_session), user: User = Depends(get_current_user)):
    return get_feed_service(db, user)
