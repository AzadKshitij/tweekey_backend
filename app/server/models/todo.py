from typing import Optional

from pydantic import BaseModel, Field


class ToDoSchema(BaseModel):
    user_id: str = Field(...)
    content: str = Field(...)
    done: bool = Field(...)
    color: str = Field(...)
    date: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "user_id": "627fcc315921d0ee12f43e19",

                "content": """[{
                        type: 'paragraph',
                        children: [
                            {text: 'This is editable '},
                            {text: 'rich', bold: true},
                            {text: ' text, '},
                            {text: 'much', italic: true},
                            {text: ' better than a '},
                            {text: '<textarea>', code: true},
                            {text: '!'},
                        ]
                    }]""",
                "done": "False",
                "color": "#ffffff",
                "date": "2020-01-01",
            }
        }


class UpdateToDoModel(BaseModel):
    user_id: Optional[str]
    content: Optional[str]
    done: Optional[bool]
    color: Optional[str]
    date: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "user_id": "627fcc315921d0ee12f43e19",

                "content": """[{
                        type: 'paragraph',
                        children: [
                            {text: 'This is editable '},
                            {text: 'rich', bold: true},
                            {text: ' text, '},
                            {text: 'much', italic: true},
                            {text: ' better than a '},
                            {text: '<textarea>', code: true},
                            {text: '!'},
                        ]
                    }]""",
                "done": "False",
                "color": "#ffffff",
                "date": "2020-01-01",
            }
        }
