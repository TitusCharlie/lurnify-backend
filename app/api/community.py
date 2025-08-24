from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List
from app.core.dependencies import get_current_user
from app.core.database import get_session
from app.services.community import (
    create_community, list_communities, join_community,
    create_post, get_feed
)
from app.schemas.community import (
    CommunityCreate, CommunityRead,
    PostCreate, PostRead, MembershipRead
)
from app.services.auth import get_current_user
from app.models.user import User


router = APIRouter(
    prefix="/community",
    tags=["Community"]
)


@router.post("/", response_model=CommunityRead)
def create_new_community(
    data: CommunityCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    return create_community(session, user, data)


@router.get("/", response_model=List[CommunityRead])
def get_all_communities(session: Session = Depends(get_session)):
    return list_communities(session)


@router.post("/{community_id}/join", response_model=MembershipRead)
def join_existing_community(
    community_id: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    return join_community(session, user, community_id)


@router.post("/{community_id}/posts", response_model=PostRead)
def create_community_post(
    community_id: str,
    data: PostCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    return create_post(session, user, community_id, data)


@router.get("/feed", response_model=List[PostRead])
def get_user_feed(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    return get_feed(session, user)