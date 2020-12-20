from wtforms import Form, StringField, TextAreaField


class CommentForm(Form):
    name = StringField("Name")
    body = TextAreaField("Body")
