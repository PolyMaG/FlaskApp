from wtforms import Form, StringField, TextAreaField


class PostForm(Form):
    title = StringField("Title")
    body = TextAreaField("Body")


class CommentForm(Form):
    name = StringField("Name")
    body = TextAreaField("Body")
