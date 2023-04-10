from flask import Flask, render_template
from faker import Faker
from werkzeug.exceptions import abort


app = Flask(__name__)
application = app
fake = Faker()


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


images_id = [
    "2d2ab7df-cdbc-48a8-a936-35bba702def5",
    "6e12f3de-d5fd-4ebb-855b-8cbc485278b7",
    "7d4e9175-95ea-4c5f-8be5-92a6b708bb3c",
    "afc2cfe7-5cac-4b80-9b9a-d5c65ef0c728",
    "cab5b7f2-774e-4884-a200-0c0180fa777f"
]


def generate_post(index):
    return {
        'title': "Заголовок поста",
        'img_id': images_id[index],
        'text': fake.paragraph(nb_sentences=100),
        'author': fake.name(),
        'date': fake.date_time_between(start_date='-2y', end_date='now')
    }


posts_list = [generate_post(i) for i in range(5)]

commnets = [
    ["Stephanie Franklin", "Leave whom discussion possible win. Performance Democrat fund that short hit song. Others something care make again series they ability."],
    ["Andrew Mcconnell", "Data now less religious. Action argue surface memory decision. Education move everybody."]
]


def comments_post(index):
    return {
        'comment_img': "icon",
        'person': commnets[index][0],
        'comment': commnets[index][1]
    }


comments_list = [comments_post(i) for i in range(len(commnets))]


@ app.route('/')
def index():
    return render_template('index.html', msg='qq')


@ app.route('/posts')
def posts():
    return render_template('posts.html', title="Посты", posts_list=posts_list, comments_list=comments_list)


@ app.route('/post/<int:post_id>')
def post(post_id):
    return render_template('post.html', post=posts_list[post_id], comments_list=comments_list)


@ app.route('/about')
def about():
    return render_template('about.html', title="Об авторе")


