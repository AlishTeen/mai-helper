# from database import connect
# from database.models import *
#
#
# # Что-то много кода, может как-то можно объеденить, но я не знаю как
# # Функция добавления абитуриента
# def add_applicant(applicant: Applicant):
#     query = Applicant.insert(applicant).values()
#     connect.execute(query)
#
#
# # Функция изменения атрибутов абитуриента, в where нужно закинуть id
# def update_applicant():
#     applicant = Applicant.update().where().values()
#     connect.execute(applicant)
#
#
# # Функция удаления абитуриента, в where нужно закинуть id
# def delete_applicant():
#     applicant = Applicant.delete().where()
#     connect.execute(applicant)
#
#
# # Функция извлечения абитуриента
# def select_applicant():
#     applicant = Applicant.select()
#     result = connect.execute(applicant)
#     return result
#
#
# # Функция добавления вопроса
# def add_question():
#     question = Question.insert.values()
#     connect.execute(question)
#
#
# # Функция удаления вопроса, в where нужно закинуть id вопроса или может id абитуриента
# def delete_question():
#     question = Question.delete().where()
#     connect.execute(question)
#
#
# # Функция извлечения воппросов по ID абитуриента
# def select_question():
#     question = Question.select().where()
#     result = connect.execute(question)
#     return result
#
#
# # Функция добавления ответа
# def add_answer():
#     question = Answer.insert.values()
#     connect.execute(question)
#
#
# # Функция удаления вопроса, в where нужно закинуть id вопроса
# def delete_answer():
#     question = Answer.delete().where()
#     connect.execute(question)
#
#
# # Функция добавления рассылаемого сообщения
# def add_message():
#     message = Messages.insert.values()
#     connect.execute(message)
#
#
# # Функция удаления рассылаемого сообщения
# def delete_message():
#     message = Messages.delete().where()
#     connect.execute(message)
