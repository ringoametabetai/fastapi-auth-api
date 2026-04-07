# models.pyはデータベースの設計図を書く場所

from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users" # テーブル名の作成

    id = Column(Integer, primary_key=True, index=True) # idカラムの作成。主キー(Primary_Key)にして、indexで検索しやすくなる
    username = Column(String, unique = True, index = True, nullable = False) # usernameカラムの作成。重複禁止・検索高速化・空禁止にする
    hashed_password = Column(String, nullable = False) # ハッシュ化されたパスワードを文字列として保存し、空は禁止する