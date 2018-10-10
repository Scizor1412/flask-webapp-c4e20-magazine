import mongoengine
# mongodb://<dbuser>:<dbpassword>@ds111113.mlab.com:11113/magazine

host= "ds111113.mlab.com"
port = 11113
db_name= "magazine"
username = "magazine"
password = "magazine4"

def connect():
    mongoengine.connect(
        db_name,
        host=host,
        port=port,
        username=username,
        password=password
    )