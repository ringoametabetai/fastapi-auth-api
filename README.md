# FastAPI Auth API

FastAPIとSQLAlchemyを用いたJWT認証付きユーザー管理APIです。

## 機能

- ユーザー登録
- ログイン認証（JWT発行）
- 認証付きエンドポイント（/me）
- パスワードのハッシュ化（argon2）

## 使用技術

- FastAPI
- SQLAlchemy
- SQLite
- JWT（python-jose）
- pwdlib（argon2）

## エンドポイント

### ユーザー登録
POST /users

### ログイン
POST /login

### ユーザー一覧
GET /users

### 自分の情報取得（認証必要）
GET /me

## 認証方法

ログインで取得したJWTを以下の形式でヘッダーに付与

Authorization: Bearer <access_token>

## 実行方法

```bash
uvicorn main:app --reload
```

## 工夫点
- パスワードは平文で保存せず、argon2でハッシュ化
- 認証失敗時のメッセージを統一し、ユーザー存在の推測を防止
- JWTを用いた認証機構を実装
