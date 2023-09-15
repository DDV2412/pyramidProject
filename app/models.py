from datetime import datetime
from mongoengine import (
    Document,
    StringField,
    DateTimeField,
    ReferenceField,
    ListField,
    BooleanField,
)


class Journal(Document):
    title = StringField(max_length=255, required=True, text=True)
    short_summary = StringField(text=True)
    issn = StringField(max_length=10, required=True)
    e_issn = StringField(max_length=10, required=True)
    abbreviation = StringField(max_length=10, required=True, text=True)
    site_url = StringField(required=True)
    content = StringField(default=None, text=True)
    thumbnail_image = StringField(default=None)
    main_image = StringField(default=None)
    contact_detail = StringField(required=True)
    editor_in_chief = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow())
    updated_at = DateTimeField(default=datetime.utcnow())

    def to_dict(self):
        return {
            "_id": str(self._id),
            "short_summary": self.short_summary,
            "title": self.title,
            "content": self.content,
            "issn": self.issn,
            "e_issn": self.e_issn,
            "abbreviation": self.abbreviation,
            "site_url": self.site_url,
            "contact_detail": self.contact_detail,
            "editor_in_chief": self.editor_in_chief,
            "thumbnail_image": self.thumbnail_image,
            "main_image": self.main_image,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class Article(Document):
    article_id = StringField(max_length=10, required=True)
    last_update = DateTimeField(default=datetime.utcnow())
    title = StringField(max_length=255, required=True, text=True)
    description = StringField(text=True)
    content = StringField(text=True)
    creators = ListField(StringField(), text=True)
    subjects = ListField(StringField(), text=True)
    publisher = StringField(text=True)
    publish_at = StringField()
    publish_year = StringField()
    doi = StringField(required=True, unique=True)
    thumbnail_image = StringField()
    main_image = StringField()
    featured = BooleanField(default=False)
    file_view = StringField()
    journal = ReferenceField(Journal)
    volume = StringField()
    issue = StringField()
    pages = StringField()
    created_at = DateTimeField(default=datetime.utcnow())
    updated_at = DateTimeField(default=datetime.utcnow())

    def to_dict(self):
        return {
            "article_id": self.article_id,
            "last_update": self.last_update,
            "title": self.title,
            "description": self.description,
            "content": self.content,
            "creators": self.creators,
            "subjects": self.subjects,
            "publisher": self.publisher,
            "publish_at": self.publish_at,
            "publish_year": self.publish_year,
            "doi": self.doi,
            "file_view": self.file_view,
            "journal": str(self.journal),
            "featured": self.featured,
            "volume": self.volume,
            "issue": self.issue,
            "pages": self.pages,
            "thumbnail_image": self.thumbnail_image,
            "main_image": self.main_image,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
