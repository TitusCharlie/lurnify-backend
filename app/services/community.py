from sqlmodel import Session, select
from app.models.community import Community, Membership, Post
from app.models.user import User
from app.schemas.community import CommunityCreate, PostCreate
from typing import List


def create_community(session: Session, creator: User, data: CommunityCreate) -> Community:
    community = Community(**data.dict(), creator_id=creator.id)
    session.add(community)
    session.commit()
    session.refresh(community)

    # auto-join creator as a member
    membership = Membership(user_id=creator.id, community_id=community.id)
    session.add(membership)
    session.commit()

    return community


def list_communities(session: Session) -> List[Community]:
    return session.exec(select(Community)).all()


def join_community(session: Session, user: User, community_id: str) -> Membership:
    membership = Membership(user_id=user.id, community_id=community_id)
    session.add(membership)
    session.commit()
    session.refresh(membership)
    return membership


def create_post(session: Session, user: User, community_id: str, data: PostCreate) -> Post:
    post = Post(**data.dict(), user_id=user.id, community_id=community_id)
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


def get_feed(session: Session, user: User) -> List[Post]:
    # posts from communities user has joined
    statement = (
        select(Post)
        .join(Community, Community.id == Post.community_id)
        .join(Membership, Membership.community_id == Community.id)
        .where(Membership.user_id == user.id)
        .order_by(Post.created_at.desc())
    )
    return session.exec(statement).all()