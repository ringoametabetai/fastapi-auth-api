# データベースに接続するための設定ファイル

from sqlalchemy import create_engine # create_engine : DBとアプリをつなぐ"接続の本体"を作る関数
from sqlalchemy.orm import declarative_base, sessionmaker # sqlalchemy.orm : pythonみたいにDB操作するための機能セット
# declarative_base : モデル(テーブル)のベースになるクラスを作る関数。これにより、models.pyの(Base)が意味を持つ。「UserクラスはDBテーブルである」
# sessionmaker     : DB操作をするための"セッションを作る関数"これにより、データ追加・検索・更新・削除が可能になる。

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db" # このフォルダにあるtest.dbというSQLiteデータベースに接続する
# sqlite:   : 使うデータベースの種類を指定
# ///       : ローカルファイル指定(WebじゃなくてファイルとしてDBを使う)
# ./test.db : 初回起動時にtest.dbが自動で作られる

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args = {"check_same_thread":False}
)
'''
SQLiteは同じ処理(スレッド)でしかDBを使えないが、FastAPIは複数のリクエストを並列処理するため、別スレッドからでもアクセスOKにする必要がある
check_same_thread = False : 別スレッドからでもアクセスOKにする
create_engine(
    URL, どこに接続するか
    オプション どう接続するか
)
'''

SessionLocal = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine # どのDBに接続するか指定 engineを通してDBと通信
)
# sessionとは、DBとやり取りするための作業スペース。作業台
# autocommit = False : 自動保存しない。これにより、ミスったらロールバックできる
# autoflush = False  : 自動でDBに反映しない。これにより、予期しない動作を防ぐことができる

Base = declarative_base()