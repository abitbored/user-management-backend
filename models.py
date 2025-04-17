from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from app import db

class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    nama: Mapped[str] = mapped_column(String(120), nullable=False)