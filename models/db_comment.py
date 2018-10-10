from mongoengine import *

class Comment(Document):
    article_id = StringField()
    content = StringField()
    author = StringField()
    time = StringField()