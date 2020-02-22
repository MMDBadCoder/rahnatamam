from django.forms import ModelForm
from accounting.models import Account, Human
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class HumanForm(ModelForm):
    class Meta:
        model = Human
        fields = ['birth_date', 'birth_month', 'birth_year', 'national_id', 'father_name', 'first_name', 'last_name',
                  'gender']


class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ['caravan', 'phone_number', 'participated_count', 'grade', 'entry_year', 'educational_status',
                  'college']


class UserSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=150, help_text='Email')

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)

# Creating a form to add an article.
# >> > form = ArticleForm()
#
# # Creating a form to change an existing article.
# >> > article = Article.objects.get(pk=1)
# >> > form = ArticleForm(instance=article)
