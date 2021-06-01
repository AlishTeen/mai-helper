from flask import Flask
from flask_login import LoginManager
from flask_talisman import Talisman
from flask_pymongo import PyMongo
import config

app = Flask(__name__)

talisman = Talisman(app, content_security_policy={'default-src': '\'self\'',
                                                  'media-src': ['youtube.com',
                                                                'youtu.be'],
                                                  'img-src': '*',
                                                  'script-src': [
                                                      '\'self\'',
                                                      'cdn.jsdelivr.net',
                                                      'code.jquery.com',
                                                      'cdnjs.cloudflare.com',
                                                      'cdn.jsdelivr.net',
                                                      'code.jquery.com',
                                                      'cdn.datatables.net'
                                                  ],
                                                  'style-src': [
                                                      '\'self\'',
                                                      'cdn.jsdelivr.net',
                                                      'use.fontawesome.com',
                                                      'cdnjs.cloudflare.com',
                                                      'cdn.datatables.net',
                                                  ],
                                                  'font-src': [
                                                      'use.fontawesome.com'
                                                  ]
                                                  },
                    content_security_policy_nonce_in=['script-src'],
                    feature_policy={
                        'geolocation': '\'none\'',
                    }
                    )

app.config['MONGO_URI'] = f'mongodb+srv://{config.DB_CREDENTIALS["login"]}:' \
                          f'{config.DB_CREDENTIALS["password"]}@' \
                          f'{config.DB_CREDENTIALS["host"]}/bot_db'

app.config['UPLOAD_FOLDER'] = 'sweater/temp_files'
app.config['MAX_CONTENT_PATH'] = '16777216'

app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

app.secret_key = config.TOKEN

mongo_db = PyMongo(app)
db = mongo_db.db
manager = LoginManager(app)

from sweater import routes, models
