from passlib.context import CryptContext
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class DBUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    urls = relationship("URL", back_populates="user")


class URLAccess(Base):
    __tablename__ = "url_access"
    id = Column(Integer, primary_key=True)
    access_time = Column(DateTime, nullable=False)
    user_agent = Column(String, nullable=False)
    client_ip = Column(String, nullable=False)

    url_id = Column(Integer, ForeignKey("urls.id"), nullable=False)
    url = relationship("URL", back_populates="accesses")


class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True)
    full_url = Column(String)
    short_url_id = Column(String, unique=True)
    deleted = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("db_users.id"))
    user = relationship("DBUser", back_populates="urls")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
