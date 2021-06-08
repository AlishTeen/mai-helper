# from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
# from sqlalchemy.ext.declarative import declarative_base
# from database import engine
#
# base = declarative_base()
#
#
# # Ниже классы для БД
# # У абитуриента связь с вопросами 1 к М, связь с рассылаемыми сообщениями 1 к М
# # У абитуриента ID атоикрементная, тоесть не нужно туда закидывать ID Telegram
#
# class Applicant(base):
#     __tablename__ = 'applicants'
#     id = Column(Integer, primary_key=True, autoincrement=False)
#     username = Column(String(30))
#     first_name = Column(String(30))
#     real_name = Column(String(30))
#     phone_number = Column(String(30))
#     email_address = Column(String(30))
#     nation = Column(String(30))
#     geo = Column(String(30))
#     menu_id = Column(Integer)
#     state = Column(Integer)
#     avatar = Column(String(100))
#     register_time = Column(DateTime)
#
#
# # У вопросов с ответами связь 1 к 1
# class Question(base):
#     __tablename__ = 'questions'
#     id = Column(Integer, primary_key=True)
#     applicants_id = Column(Integer, ForeignKey('applicants.id'))
#     text = Column(String(150))
#     datetime = Column(DateTime)
#     answered = Column(Boolean)
#
#
# class Answer(base):
#     __tablename__ = 'answers'
#     id = Column(Integer, primary_key=True)
#     text = Column(String(150))
#     question_id = Column(Integer, ForeignKey('questions.id'))
#     datetime = Column(DateTime)
#
#
# # У Администратора связь с рассылаемыми сообщениями 1 к М
# class Admin(base):
#     __tablename__ = 'admins'
#     id = Column(Integer, primary_key=True)
#     login = Column(String(30))
#     password = Column(String(200))
#
#
# class Messages(base):
#     __tablename__ = 'messages'
#     id = Column(Integer, primary_key=True)
#     text = Column(String(200))
#     datetime = Column(DateTime)
#     admin_id = Column(Integer, ForeignKey('admins.id'))
#
#
# base.metadata.create_all(engine)
