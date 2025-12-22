from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base は ORM の基底(kitei)クラスです。
    これによって、SQLAlchemy はクラスをデータベースのテーブルとして扱えるようになります。
    """

    pass
