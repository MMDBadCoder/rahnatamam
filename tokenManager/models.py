import random
import string

from django.db import models

# Create your models here.
from accounting.models import Account


class TokenCode(models.Model):
    class TokenType:
        ACTIVATE = 'ACTIVATE'

    code = models.CharField(max_length=100, null=False, blank=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=False, blank=False)
    type = models.CharField(max_length=30)

    @staticmethod
    def create_new_token(account, type):
        if type == TokenCode.TokenType.ACTIVATE:
            length = 5
        else:
            length = 20
        code = TokenCode.get_random_code(length)
        token = TokenCode(code=code, type=type, account=account)
        return token

    @staticmethod
    def get_random_code(length):
        letters = string.digits
        return ''.join(random.choice(letters) for i in range(length))
