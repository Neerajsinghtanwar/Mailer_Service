from app.settings import db, mail
from app.models import User, Emails, Notification
from app.app import app
from flask import jsonify, request, render_template
from flask_mail import Message
from apscheduler.schedulers.background import BackgroundScheduler
import uuid
from sqlalchemy import desc


def send_email():
    print('sending....')
    with app.app_context():
        users = User.query.filter_by(admin=False).all()
        for user in users:
            unique_number = str(uuid.uuid4().int & (1 << 64) - 1)
            html = render_template('mail_template.html', email=user.email, id=unique_number)
            msg = Message('Daily Morning Mail', sender='neerajtanwar17@gmail.com', recipients=[user.email], html=html)
            msg.body = "Hello, this is a test email"
            try:
                mail.send(msg)
                create_email(user, True, False, unique_number)
                create_notify(user, f'Email sent successfully to {user.name}')
                print('email sent')

            except Exception as e:
                create_email(user, False, False, unique_number)
                create_notify(user, f'Email not sent to {user.name}')
                print(str(e))


scheduler = BackgroundScheduler()
scheduler.add_job(func=send_email, trigger='cron', hour=6, minute=0)
# scheduler.add_job(func=send_email, trigger='interval', seconds=10)
scheduler.start()


@app.route('/')
def get():
    users = User.query.all()
    return jsonify({'users': [user.serialize() for user in users]})
    # return render_template('mail_template.html', email='theneerajtanwar@gmail.com', id='10754133299629705795')


@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.form
        print(bool(data['is_admin']))
        user = User(
            name=data['name'],
            email=data['email'],
            password=data['password'],
            admin=bool(int(data['is_admin']))
        )
        db.session.add(user)
        db.session.commit()

        return jsonify({'success': True, 'message': 'User created successfully.'})

    except Exception as e:
        print(e)
        return jsonify({'success': False, 'message': str(e)})


@app.route('/signin', methods=['POST'])
def signin():
    try:
        data = request.form
        email = data['email']
        password = data['password']
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'success': False, 'message': 'User not found.'})

        if user.password != password:
            return jsonify({'success': False, 'message': 'Invalid password.'})

        return jsonify({'success': True, 'message': 'Login Successfully.', 'user': user.serialize()})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/emails', methods=['GET'])
def emails():
    try:
        obj = Emails.query.all()
        return jsonify({'success': True, 'mails': [mails.serialize() for mails in obj]})

    except Exception as e:
        return jsonify({'success': False, 'msg': str(e)})


@app.route('/notifications', methods=['GET'])
def notifications():
    try:
        obj = Notification.query.order_by(desc(Notification.id)).all()
        return jsonify({'success': True, 'notifications': [notify.serialize() for notify in obj]})

    except Exception as e:
        return jsonify({'success': False, 'msg': str(e)})


@app.route('/email-seen', methods=['GET'])
def email_seen():
    email = request.args['email']
    id = request.args['id']
    user = User.query.filter_by(email=email).first()
    create_notify(user, f"{user.name} seen today email")
    obj = Emails.query.filter_by(unique_id=id).first()
    obj.is_seen = True
    db.session.commit()
    return jsonify({'success': True, 'msg': 'email seen'})


def create_email(user, sent, seen, id):
    add_mail = Emails(
        user_id=user.id,
        user=user,
        is_sent=sent,
        is_seen=seen,
        unique_id=id
    )
    db.session.add(add_mail)
    db.session.commit()


def create_notify(user, text):
    notify = Notification(
        user_id=user.id,
        user=user,
        msg=text
    )
    db.session.add(notify)
    db.session.commit()
