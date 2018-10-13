from gmail import GMail, Message

def sent_mail(x,y):
    gmail = GMail("dangsonhai26061995@gmail.com","Theeternal0610")
    html_content = """
    Cảm ơn bản đã sử dụng dịch vụ của chúng tôi
    Mật khẩu mới của bạn là:{}
    Trân trọng cảm ơn!""".format(y)
    msg = Message('Khôi phục mật khẩu',to = x ,html = html_content)
    gmail.send(msg)

def sent_mail_verify(x,y):
    gmail = GMail("dangsonhai26061995@gmail.com","Theeternal0610")
    html_content = """
    Cảm ơn bản đã sử dụng dịch vụ của chúng tôi
    Vui lòng click vào link dưới để xác nhận đăng ký tài khoản:{}
    Trân trọng cảm ơn!""".format(y)
    msg = Message('Xác nhận đăng ký tài khoản',to = x ,html = html_content)
    gmail.send(msg)