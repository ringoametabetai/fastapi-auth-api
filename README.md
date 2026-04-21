# FastAPI Auth API

FastAPIとSQLAlchemyを用いて作成した、JWT認証付きのユーザー管理APIです。  
ユーザー登録・ログイン・認証付きエンドポイントの基本機能を実装しました。

## 機能

- ユーザー登録
- ログイン認証（JWT発行）
- 認証付きエンドポイント（/me）
- ユーザー一覧取得
- パスワードのハッシュ化（argon2）

## 使用技術

- FastAPI
- SQLAlchemy
- SQLite
- JWT（python-jose）
- pwdlib（argon2）
- python-dotenv

## エンドポイント

### ユーザー登録
`POST /users`

### ログイン
`POST /login`

### ユーザー一覧
`GET /users`

### 自分の情報取得（認証必要）
`GET /me`

## 認証方法

ログインで取得したJWTを、以下の形式でAuthorizationヘッダーに付与して使用します。

```bash
Authorization: Bearer <access_token>
```

## セットアップ方法

1. リポジトリをクローン
```bash
git clone <リポジトリURL>
cd fastapi-auth-api
```

2. 仮想環境を作成・有効化
```bash
python -m venv venv
venv\Scripts\activate
```

3. 必要なライブラリをインストール
```bash
pip install fastapi uvicorn sqlalchemy python-jose[cryptography] pwdlib python-dotenv python-multipart
```

4. .env ファイルを作成
プロジェクト直下に .env を作成し、以下のように記述します。
```bash
SECRET_KEY=your_secret_key_here
```

5. アプリを起動
```bash
uvicorn main:app --reload
```

6. Swagger UIで動作確認
以下にアクセスします。
```bash
http://127.0.0.1:8000/docs
```

## 動作確認の流れ
1. POST /users でユーザー登録
2. POST /login でログインし、JWTを取得
3. 右上の Authorize から認証
4. GET /me でログイン中のユーザー情報を確認

## 工夫した点
- パスワードは平文で保存せず、argon2でハッシュ化
- JWTを用いて認証機構を実装
- 認証失敗時のメッセージを統一し、ユーザー存在の推測を防止
- response_model を用いて、レスポンスから不要な情報（hashed_passwordなど）を除外
- SECRET_KEY は .env で管理し、GitHubに直接公開しないように修正

## この成果物で学んだこと
- FastAPIでのAPI設計の基本
- SQLAlchemyを用いたDB操作
- JWT認証の流れ
- パスワードを安全に保存する考え方
- 環境変数を使った機密情報の管理

## 今後の改善点
- Depends を使ったDBセッション管理の改善
- schemas.py への分割
- 例外処理の整理
- Alembicを使ったマイグレーション管理
- Docker対応

## 補足

このプロジェクトは学習用・ポートフォリオ用として作成したものです。