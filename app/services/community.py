# from sqlmodel import Session, select
# from app.models.community import Community, Membership, Post
# from app.models.user import User
# from app.schemas.community import CommunityCreate, PostCreate
# from typing import List


# def create_community(session: Session, creator: User, data: CommunityCreate) -> Community:
#     community = Community(**data.dict(), creator_id=creator.id)
#     session.add(community)
#     session.commit()
#     session.refresh(community)

#     # auto-join creator as a member
#     membership = Membership(user_id=creator.id, community_id=community.id)
#     session.add(membership)
#     session.commit()

#     return community


# def list_communities(session: Session) -> List[Community]:
#     return session.exec(select(Community)).all()


# def join_community(session: Session, user: User, community_id: str) -> Membership:
#     membership = Membership(user_id=user.id, community_id=community_id)
#     session.add(membership)
#     session.commit()
#     session.refresh(membership)
#     return membership


# def create_post(session: Session, user: User, community_id: str, data: PostCreate) -> Post:
#     post = Post(**data.dict(), user_id=user.id, community_id=community_id)
#     session.add(post)
#     session.commit()
#     session.refresh(post)
#     return post


# def get_feed(session: Session, user: User) -> List[Post]:
#     # posts from communities user has joined
#     statement = (
#         select(Post)
#         .join(Community, Community.id == Post.community_id)
#         .join(Membership, Membership.community_id == Community.id)
#         .where(Membership.user_id == user.id)
#         .order_by(Post.created_at.desc())
#     )
#     return session.exec(statement).all()

from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.community import Community, Membership, Post
from app.schemas.community import CommunityCreate, PostCreate
from app.models.user import User

def create_community_service(db: Session, data: CommunityCreate, user: User):
    community = Community(
        name=data.name,
        description=data.description,
        creator_id=user.id
    )
    db.add(community)
    db.commit()
    db.refresh(community)

    # Add creator as owner
    membership = Membership(user_id=user.id, community_id=community.id, role="owner")
    db.add(membership)
    db.commit()

    return community

def join_community_service(db: Session, community_id: str, user: User):
    existing = db.exec(select(Membership).where(
        Membership.community_id == community_id,
        Membership.user_id == user.id
    )).first()
    if existing:
        raise HTTPException(400, "Already a member")

    membership = Membership(user_id=user.id, community_id=community_id, role="member")
    db.add(membership)
    db.commit()
    db.refresh(membership)
    return membership

def leave_community_service(db: Session, community_id: str, user: User):
    membership = db.exec(select(Membership).where(
        Membership.community_id == community_id,
        Membership.user_id == user.id
    )).first()
    if not membership:
        raise HTTPException(400, "Not a member")
    if membership.role == "owner":
        raise HTTPException(400, "Owner cannot leave their own community")
    db.delete(membership)
    db.commit()
    return {"message": "Left community"}

def create_post_service(db: Session, community_id: str, data: PostCreate, user: User):
    membership = db.exec(select(Membership).where(
        Membership.community_id == community_id,
        Membership.user_id == user.id
    )).first()
    if not membership:
        raise HTTPException(403, "Join the community first")

    post = Post(community_id=community_id, author_id=user.id, content=data.content)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

def get_feed_service(db: Session, user: User):
    memberships = db.exec(select(Membership).where(Membership.user_id == user.id)).all()
    community_ids = [m.community_id for m in memberships]
    posts = db.exec(select(Post).where(Post.community_id.in_(community_ids)).order_by(Post.created_at.desc())).all()
    return posts