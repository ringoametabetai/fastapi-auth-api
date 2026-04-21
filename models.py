# DBモデル定義（テーブル設計）

from sqlalchemy import Column, Integer, String
from database import Base


class User(Base):
    __tablename__ = "users"  # テーブル名

    id = Column(Integer, primary_key=True, index=True)  # 主キー
    username = Column(String, unique=True, index=True, nullable=False)  # ユーザー名（重複不可）
    hashed_password = Column(String, nullable=False)  # ハッシュ化パスワード