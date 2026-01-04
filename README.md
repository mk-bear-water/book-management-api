# Book Management API
- 書籍（Books）と著者（Authors）を管理するシンプルな REST API です。

# 技術スタック
- 開発言語: Python 3.14
- フレームワーク: FastAPI
- データベース: MySQL 8.4
- 開発環境: Docker

# 開発環境のセットアップ手順
1. 起動
```bash
docker compose up -d --build
```
2. 起動確認
```bash
curl -i 'http://localhost:8000/health'
```
3. データベースマイグレーション
- 初回起動時、またはスキーマ変更時に実行してください。
```bash
docker compose exec api sh -lc "cd /app && python -m alembic upgrade head"
```

# API エンドポイント一覧
## 著者 （Author）
### POST /authors
- 新しい著者を登録します (50文字以内) 。
```bash
curl -i -X POST 'http://localhost:8000/authors' \
  -H 'Content-Type: application/json' \
  -d '{
    "name":"{著者名}"
  }'
```
## 書籍 （Book）
### POST /books
- 新しい書籍を登録します (100文字以内) 。
- 登録時には、既存の著者ID (author_id) を指定する必要があります。
```bash
curl -i -X POST 'http://localhost:8000/books' \
  -H 'Content-Type: application/json' \
  -d '{
    "author_id": "{author_id}",
    "title": "{書籍タイトル}"
  }'
```
### GET /books
- 登録されている書籍の一覧を取得します。
```bash
curl -sS 'http://localhost:8000/books'
```
### GET /books/{book_id}
- 指定されたIDの書籍情報を取得します。
```bash
curl -sS 'http://localhost:8000/books/{book_id}'
```
### DELETE /books/{book_id}
- 指定されたIDの書籍を削除します。
```bash
curl -i -X DELETE 'http://localhost:8000/books/{book_id}'
```

# 意識した点
## 技術スタック
- Python と MySQL はサポート期間を考慮してLTS版を選定しています。
## セットアップ
- 本番・ステージング環境での運用を想定し、環境変数で設定を切り替えられる構成です。
- ローカル開発では docker-compose.override.yml によりホットリロードが有効になります。
## モジュール設計
- 全体の設計思想は FastAPI 公式のテンプレートを参考としました。
- https://github.com/fastapi/full-stack-fastapi-template/tree/master
### app
- DB スキーマは models.py で定義し、入出力のバリデーションは schemas.py で定義しています。
### app/api
- エンドポイント追加時は routes/*.py を増やし、router.py に登録するだけで実装できるようにしています。
- errors.py に 404/409 などの例外生成をまとめ、エラーレスポンス形式を統一しています。
### app/core
- config.py で環境変数を一元管理し、設定オブジェクトは lru_cache により再生成されないようにしています。
- DB 接続は DATABASE_URL を優先し、未指定の場合は DATABASE_* から組み立てることで柔軟に指定できるようにしています。
- db.py では get_db() を FastAPI の Dependency として提供し、リクエスト単位で Session を管理しています。
