# -*- coding: utf-8 -*-
# Create Date 2015/12/10
__author__ = 'wubo'
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, email, Regexp, EqualTo
from wtforms import ValidationError
from web import User


class LoginForm(Form):
    account = StringField("account", validators=[DataRequired(message=u'用户名不能为空！'), Length(4, 20, message=u'用户名长度必须是4-20位！')])
    passwd = PasswordField("password", validators=[DataRequired(message=u'密码不正确！'), Length(5, 16, message=u'密码长度为5-16位！')])
    remember_me = BooleanField(u'Keep me logged in')
    submit = SubmitField(u'登陆')


# class RegistrationForm(Form):
#     account = StringField("account", validators=[DataRequired(message=u'用户名不能为空！'), Length(4, 20, message=u'用户名长度必须是4-20位！')])
#     email = StringField("email", validators=[email(message=u'邮箱不能为空！')])
#     password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must match.')])
#     password2 = PasswordField('Confirm password', validators=[DataRequired()])
#     submit = SubmitField('Register')



