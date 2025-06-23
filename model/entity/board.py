from sqlmodel import Field, SQLModel

class Board(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(default=None, nullable=False)
    image: str = Field(default=None, nullable=False)
    content_type: str = Field(default=None, nullable=False)
    field: str = Field(default=[{"bbox": [12,12,12,12],"name": "제목","type": "nlp","validValues":["test","produce","green"]},{"bbox": [102,120,103,104],"name": "체크박스","type": "checkBox","checkBox":"T"}], nullable=True)
    group_id: int = Field(default=0, nullable=True)

