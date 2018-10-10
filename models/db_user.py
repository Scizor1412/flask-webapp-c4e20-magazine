from mongoengine import *

class User(Document):
    fullname = StringField()
    yob = IntField()
    email = EmailField()
    password = StringField()
    request = BooleanField()
    level = IntField()
# 0 là admin, 1 là user được phép post bài, 2 là user chờ phê duyệt, 3 là user được cmt, mặc định tạo tài khoản là 3