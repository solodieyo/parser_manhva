from sqlalchemy import Integer, BigInteger, Text, Boolean
from sqlalchemy.orm import mapped_column

from db.base import Base


class Manhva(Base):
	__tablename__ = 'manhva'

	id = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
	user_id = mapped_column(BigInteger, nullable=False, index=True)
	manhva_name = mapped_column(Text, nullable=False)
	archived = mapped_column(Boolean, nullable=False, default=False)
