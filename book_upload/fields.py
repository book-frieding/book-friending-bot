# from aiogram_forms import forms, fields
from aiogram_forms.base import BaseField
import re


class StringField(BaseField):

    @classmethod
    def process_message(cls, msg: str):
        return msg


class ArrayField(BaseField):

    @classmethod
    def process_message(cls, msg: str):
        return msg.split(', ')