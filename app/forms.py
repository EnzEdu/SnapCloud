from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

class EditProfileForm(FlaskForm):
    full_name = StringField("Nome Completo", validators=[DataRequired(), Length(max=100)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    description = TextAreaField("Descrição", validators=[Length(max=300)])
