from mongoengine import *
import mlab

mlab.connect()
class Comment(Document):
    article_id = StringField()
    content = StringField()
    author = StringField()
    time = DateTimeField()

class Article(Document):
    title = StringField()
    sapo = StringField()
    thumbnail = StringField()
    content = StringField()
    time = DateTimeField()
    author = StringField()
    level = IntField()
    category = StringField()
    view_count = IntField(default=0)
    comment = ListField(ReferenceField(Comment))
# 0 là chưa duyệt, 1 là đã duyệt và có thể hiển thị

# article = Article(
#     title = "Sport",
#     comment = []
# )
# article.save()

# comment = Comment(
#     author = "Nguyen"
# )
# comment.save()
# article.update(push__comment = comment)