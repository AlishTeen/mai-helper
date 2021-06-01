from flask import render_template, url_for, request, redirect, flash, jsonify, send_file
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from sweater import app, db, utils
from sweater.models import Admin
from io import BytesIO
from base64 import b64decode
from datetime import datetime, timedelta
import calendar
import os
from unidecode import unidecode


@app.errorhandler(404)
def not_found(e):
    return render_template('sweater/404.html'), 404


@app.errorhandler(401)
def unauthorized(e):
    return render_template('sweater/login.html'), 401


@app.errorhandler(500)
def internal(e):
    return render_template('sweater/500.html', e=e), 500


@app.route('/favicon.ico')
def favicon():
    return send_file('static/images/mai-web.svg')


@app.route('/')
@app.route('/main')
@login_required
def main():
    now = datetime.utcnow()
    today = datetime(now.year, now.month, now.day)
    last_7_days = now - timedelta(7)
    this_month = datetime(now.year, now.month, 1)
    users_count = {'all': db.users.estimated_document_count(),
                   'today': db.users.count_documents({'register_time': {'$gt': today}}),
                   'last_7': db.users.count_documents({'register_time': {'$gt': last_7_days}}),
                   'this_month': db.users.count_documents({'register_time': {'$gt': this_month}})}
    questions_count = {'all': db.questions.estimated_document_count(),
                       'today': db.questions.count_documents({'datetime': {'$gt': today}}),
                       'last_7': db.questions.count_documents({'datetime': {'$gt': last_7_days}}),
                       'this_month': db.questions.count_documents({'datetime': {'$gt': this_month}})}
    dialogflow_count = {'all': db.autoinc.find_one({'_id': 'dflow_count'})['counter']}

    return render_template('sweater/main.html', users_count=users_count, questions_count=questions_count,
                           dflow_count=dialogflow_count)


@app.route('/questions', methods=['GET', 'POST'])
@login_required
def questions():
    questions_list = list(db.questions.find({'answered': False}))
    users_list = list(db.users.find({}, {'user_id': 1, 'real_name': 1, '_id': 0}))
    for question in questions_list:
        res = db.users.find_one({'user_id': int(question['user_id'])}, {'real_name': 1, '_id': 0})
        question['name'] = res['real_name'] if res else question['user_id']
    return render_template('sweater/questions.html', question=questions_list)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash(message='Вы уже авторизованы', category='auth')
        return redirect(url_for('main'))
    login_input = request.form.get('login_')
    password_input = request.form.get('pass_')
    if login_input and password_input:
        admin = db.admins.find_one({'username': login_input})
        if admin and check_password_hash(admin['password_hash'], password_input):
            admin_obj = Admin(username=admin['username'])
            login_user(admin_obj, remember=True)
            return redirect(url_for('main'))
        else:
            flash('Неправильный логин или пароль')
    return render_template('sweater/login.html')


@app.route('/mailing')
@login_required
def mailing():
    for f in os.listdir(app.config['UPLOAD_FOLDER']):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], f))
    return render_template('sweater/mailing.html')


@app.route('/users')
@login_required
def users():
    all_users_list = list(db.users.find())
    return render_template('sweater/users.html', users=all_users_list)


@app.route('/intro')
@login_required
def intro():
    return render_template('sweater/intro.html')


@app.route('/dialogflow')
@login_required
def dialogflow():
    return render_template('sweater/dialogflow.html')


# API METHODS

@app.route('/api/stat/count')
@login_required
def api_stat_count():
    now = datetime.utcnow()
    last_days = [calendar.monthrange(now.year, i + 1)[1] for i in range(12)]

    data = {
        'datasets': [{'dataName': 'Пользователи',
                      'data': [db.users.count_documents({'register_time': {'$gte': datetime(now.year, n + 1, 1),
                                                                            '$lte': datetime(now.year, n + 1, i)}})
                               for n, i in enumerate(last_days)]},
                     {'dataName': 'Вопросы',
                      'data': [db.questions.count_documents({'datetime': {'$gte': datetime(now.year, n + 1, 1),
                                                                           '$lte': datetime(now.year, n + 1, i)}})
                               for n, i in enumerate(last_days)]}],
        'dataCols': ['Январь', 'Февраль', 'Март',
                     'Апрель', 'Май', 'Июнь',
                     'Июль', 'Август', 'Сентябрь',
                     'Октябрь', 'Ноябрь', 'Декабрь']
    }

    return jsonify(data)


@app.route('/api/stat/nation')
@login_required
def api_stat_nation():
    data = {
        'datasets': [{'dataName': 'Гражданство',
                      'data': [db.users.count_documents({'nation': '🇷🇺 РФ'}),
                               db.users.count_documents({'nation': '🇰🇿 РК'})]}],
        'dataCols': ['РФ', 'РК']
    }
    return jsonify(data)


@app.route('/api/avatar')
@login_required
def api_avatar():
    uid = request.args.get('uid')
    user = db.users.find_one({'user_id': int(uid)})
    if user:
        user_avatar = BytesIO(b64decode(user['avatar_b64'])) \
            if user['avatar_b64'] \
            else 'static/images/default_avatar.png'
        return send_file(
            user_avatar,
            mimetype='image/jpeg',
            as_attachment=True,
            attachment_filename=f'avatar-{uid}.jpg')
    else:
        return 'User not found', 404


@app.route('/api/submit/message', methods=['POST'])
@login_required
def api_submit_message():
    qid = request.form.get('qid')
    text = request.form.get('text')
    uid = request.form.get('uid')
    question = request.form.get('q-text')
    if utils.send_message(uid, qid, text, question):
        db.questions.update_one({'_id': int(qid)}, {'$set': {'answered': True, 'answer': text}})
        flash('Сообщение успешно отправлено.')
    else:
        flash('Возникла ошибка. Возможно, пользователь запретил боту отправлять сообщения.')
    return redirect(url_for('questions'))


@app.route('/api/submit/file', methods=['POST'])
@login_required
def api_submit_file():
    file = request.files['file']
    filename = secure_filename(unidecode(file.filename))
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return 'ok', 200


@app.route('/api/submit/mailing', methods=['POST', 'GET'])
@login_required
def api_submit_mailing():
    text = request.form.get('m-text')
    users_id = [el['user_id'] for el in db.users.find({}, {'user_id': 1, '_id': 0})]
    res = utils.mailing(users_id, text)
    flash(f'Успешно отправлено {res} из {len(users_id)} пользователей')
    return redirect(url_for('mailing'))
