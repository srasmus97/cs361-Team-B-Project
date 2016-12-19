from google.appengine.ext import ndb


class Question(ndb.model):
    student = ndb.StringProperty(required=True)
    course = ndb.StringProperty(required=True)
    subject = ndb.StringProperty(required=True)
    content = ndb.TextProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    last_modified = ndb.DateTimeProperty(auto_now=True)

    def createQuestion(self, student, course, subject, content):
        question = Question(student=student, course=course, subject=subject, content=content)
        question.put()
