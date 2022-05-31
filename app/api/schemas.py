from app.models import Post
from app.services import ma


class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        fields = ['uid', 'created', 'last_updated', 'type', 'title', 'content', 'images']

    validation_schema = {
        "type": "object",
        "properties": {
            "type": {"type": "string", "enum": ['blog', 'event']},
            "title": {"type": "string", "maxlength": 40},
            "content": {"type": "string"},
        },
        "required": ["type", "title", "content"],
    }



