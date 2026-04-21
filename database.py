# DB接続設定（SQLAlchemy）

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLiteのDB接続URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# DB接続エンジン作成（FastAPI + SQLite用）
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# DB操作用セッション作成
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# モデル定義用のベースクラス
Base = declarative_base()