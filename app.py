from flask import *
import mlab
from models.db_user import User
from models.db_article import Article, Comment
from datetime import datetime
from sent_mail import sent_mail
from reset_pass import *

app = Flask(__name__)

mlab.connect()

app.secret_key = "secret key"
1
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods = [ 'GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        form = request.form
        new_user = User(
            fullname = form['fullname'],
            yob = form['yob'],
            email = form['email'],
            password = form['password'],
            level = 99
        )
        new_user.save()
        x = form['email']
        user = User.objects.get(email = x)
        user_id = user.user_id
        y = "http://127.0.0.1:5000/{}".format(user_id)
        verify_account(x,y)
        return redirect(url_for('login'))

@app.route('/verify_account/<user_id>')
def verify_account(user_id):
    user_id = User.objects.with_id(user_id)
    if user_id is not None:
        verify_user = User(
            level = 3
        )
        verify_user.update()
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route('/admin')
def admin():
    if 'loggedin' in session:
        if session['loggedin'] == True and session['level'] == 0:
            return render_template('admin.html', userid = session['id'])
        else:
            return redirect(url_for('homepage'))
    else:
        return redirect(url_for('login'))

@app.route('/admin/user')
def admin_user():
    users = User.objects()
    return render_template('admin_user.html', users = users)

@app.route('/admin/article')
def admin_article():
    articles = Article.objects()
    return render_template('admin_article.html', articles = articles)

@app.route('/login', methods = ["GET", "POST"])
def login():
    if "loggedin" in session:
        if session['loggedin'] == True:
            return redirect(url_for('homepage'))
        else:
            if request.method == "GET":
                return render_template('login.html')
            elif request.method == "POST":
                form = request.form
                email = form['email']
                password = form['password']

            found_user = User.objects.get(email = email, password = password)

            if found_user is not None:
                session['loggedin'] = True
                session['id'] = str(found_user.id)
                session['level'] = found_user.level
                if session['level'] == 0:
                    return redirect(url_for('admin'))
                else:
                    return redirect(url_for('homepage'))
            else:
                return redirect(url_for('login'))
    else:
        if request.method == "GET":
            return render_template('login.html')
        elif request.method == "POST":
            form = request.form
            email = form['email']
            password = form['password']

        found_user = User.objects.get(email = email, password = password)

        if found_user is not None:
            session['loggedin'] = True
            session['id'] = str(found_user.id)
            session['level'] = found_user.level
            if session['level'] == 0:
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('homepage'))
        else:
            return "Invalid username or password"

@app.route('/profile')
def profile():
    if "loggedin" in session:
        if session['loggedin'] == True:
            user_id = session['id']
            user_profile = User.objects.with_id(user_id)
            return render_template('profile.html',user_profile = user_profile)
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route('/detele_user/<user_id>')
def delete_user(user_id):
    delete_user = User.objects.with_id(user_id)
    if delete_user is not None:
        delete_user.delete()
        return redirect(url_for('admin'))
    else:
        return "Not found"

@app.route('/edit_user/<user_id>', methods = ['GET', 'POST'])
def edit_user(user_id):
    edit_user = User.objects.with_id(user_id)
    if edit_user is not None:
        if request.method == 'GET':
            return render_template('edit_user.html', edit_user = edit_user)
        elif request.method == 'POST':
            form = request.form
            edit_user.update(
                set__fullname = form['fullname'],
                set__yob = form['yob'],
                set__email = form['email']
            )
            return redirect(url_for('admin_user'))
    else:
        return redirect(url_for('admin'))

@app.route('/change_password', methods = ['GET', 'POST'])
def change_password():
    if "loggedin" in session:
        if session['loggedin'] == True:
            user_id = session['id']
            user_change_password = User.objects.with_id(user_id)
            # return render_template('profile.html',user_change_password = user_change_password)
        
    # user_change_password = User.objects.with_id(user_id)
            if user_change_password is not None:
                if request.method == 'GET':
                    return render_template ('change_password.html')
                elif request.method == 'POST':
                    form = request.form
                    current_password = form['current_password']
                    new_password = form['new_password']
                    password= form['password']
                    if current_password == user_change_password['password']:
                        if password == new_password:
                            user_change_password.update(
                                set__password = password
                            )
                            return redirect(url_for('login'))
                        else:
                            return redirect(url_for('admin'))
                    else:
                        return redirect(url_for('admin'))
            else:
                return redirect(url_for('aprofile'))
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

# Sửa thông tin bài viết
@app.route('/delete_article/<article_id>')
def delete_article(article_id):
    delete_article = Article.objects.with_id(article_id)
    if delete_article is not None:
        delete_article.delete()
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('admin'))


@app.route('/edit_article/<article_id>', methods =['GET' ,'POST'])
def edit_article(article_id):
    edit_article = Article.objects.with_id(article_id)
    if edit_article is not None:
        if request.method == 'GET':
            return render_template('edit_article.html', edit_article = edit_article)
        elif request.method == 'POST':
            form = request.form
            edit_article.update(
                title = form['title'],
                sapo = form['sapo'],
                thumbnail = form['thumbnail'],
                time = form['time'],
                content = form['content'],
                author = form['author']
            )
            return redirect(url_for('admin_article'))
    else:
        return redirect(url_for('admin'))

@app.route('/article/approval')
def article_approval():
    articles = Article.objects()
    return render_template ('article_approval.html', articles = articles)

@app.route('/article/approve/<article_id>')
def approve_article(article_id):
    approve_article = Article.objects.with_id(article_id)
    if approve_article is not None:
        approve_article.update(
            set__level = 1
        )
        return redirect(url_for('article_approval'))
    else:
        return redirect(url_for('article_approval'))

# Phê duyệt người dùng
@app.route('/user/request')
def user_approval():
    users= User.objects()
    return render_template ('user_approval.html', users = users)

@app.route('/user/approve/<user_id>')
def approve_user(user_id):
    approve_user = Request.objects.with_id(user_id)
    if approve_user is not None:
        approve_user.update(
            set__level = 1,
            set__request = False
        )
        return redirect(url_for('user_request'))
    else:
        return redirect(url_for('user_request'))

        
@app.route('/reject_user/<user_id>')
def reject_user(user_id):
    reject_user = User.objects.with_id(user_id)
    if reject_user is not None:
        reject_user.update(
            set__request = False
        )
        return redirect(url_for('user_request'))
    else:
        return redirect(url_for('user_request'))

@app.route('/homepage', methods = ["GET", "POST"])
def homepage():
    articles = Article.objects.order_by('-time')
    articles_view = Article.objects.order_by('-view_count')
    if request.method == "GET":
        return render_template("homepage.html", articles = articles, articles_view = articles_view)
    elif request.method == "POST":
        return redirect(url_for('search', keywords=request.form['keywords']))

@app.route('/article/<article_id>', methods = ["GET", "POST"])
def template(article_id):
    article = Article.objects.with_id(article_id)
    print(article)
    articles_view = Article.objects.order_by('-view_count')
    articles_type_time = Article.objects(category= article.category).order_by('-time')
    if request.method == "GET":
        article.update(
            set__view_count = article['view_count'] +1,
        )
        return render_template('template.html', article = article, articles_view = articles_view, articles_type_time=articles_type_time)
    elif request.method == "POST":
        form = request.form
        if 'search' in form: 
            return redirect(url_for('search', keywords=form['search']))
            # return "Search"
        else:
            if "loggedin" not in session:
                return redirect(url_for('login'))
            else:
                author = User.objects.with_id(session['id'])
                form = request.form
                comment = Comment(
                    author = author.fullname,
                    time = datetime.now(),
                    content = form['content']
                )
                comment.save()
                article.update(push__comment = comment)
                return render_template('template.html', article = article, articles_view = articles_view)
            # return "Comment"
        # if request.form['search'] in request.form:
        # else:

@app.route('/forgotpass', methods=['GET','POST'])
def forgotpass():
    if request.method == 'GET':
        return render_template('forgotpass.html')
    elif request.method == 'POST':
        form = request.form
        email = form['email']
        user_reset = User.objects.get(email = email).id
        user = User.objects.with_id(user_reset)
        password = password_generator(size=8, chars=string.ascii_letters + string.digits)
        user = user.update(
            password = password
        )
        sent_mail(email,password)
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['loggedin'] = False
    return redirect(url_for('login'))

@app.route('/search/<keywords>')
def search(keywords):
    articles = Article.objects(title__icontains=keywords)
    articles_view = Article.objects.order_by('-view_count')
    return render_template ('result.html', articles = articles, keywords = keywords, articles_view=articles_view)

@app.route('/coming')
def coming():
    return render_template('coming-soon.html')

@app.route('/category/game')
def game():
    articles = Article.objects(category = "Games").order_by('-time')
    articles_view = Article.objects.order_by('-view_count')
    if request.method == "GET":
        return render_template("homepage.html", articles = articles, articles_view = articles_view)
    elif request.method == "POST":
        return redirect(url_for('search', keywords=request.form['keywords']))

@app.route('/category/film')
def film():
    articles = Article.objects(category = "Film").order_by('-time')
    articles_view = Article.objects.order_by('-view_count')
    if request.method == "GET":
        return render_template("homepage.html", articles = articles, articles_view = articles_view)
    elif request.method == "POST":
        return redirect(url_for('search', keywords=request.form['keywords']))

@app.route('/category/tech')
def tech():
    articles = Article.objects(category = "Tech").order_by('-time')
    articles_view = Article.objects.order_by('-view_count')
    if request.method == "GET":
        return render_template("homepage.html", articles = articles, articles_view = articles_view)
    elif request.method == "POST":
        return redirect(url_for('search', keywords=request.form['keywords']))

if __name__ == '__main__':
  app.run(debug=True)