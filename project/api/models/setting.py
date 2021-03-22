from sqlalchemy import Column
from sqlalchemy import String

from .base import db, BaseColumns


class Setting(db.Model, BaseColumns):
    __tablename__ = "setting"

    name = Column(String(50), unique=True, nullable=False, index=True)  # 配置项名称
    value = Column(String(500), nullable=False, server_default='')  # 值
    group = Column(String(100), nullable=False, server_default='')  # 分组
