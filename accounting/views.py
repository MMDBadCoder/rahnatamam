import threading

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from accounting.error_handler import create_error_text
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from accounting.forms import UserSignUpForm, AccountForm, HumanForm
from accounting.models import Account, Human
from tokenManager.models import TokenCode


def signup(request):
    if request.method == 'POST':
        user_form = UserSignUpForm(request.POST)
        account_form = AccountForm(request.POST)
        human_form = HumanForm(request.POST)

        if user_form.is_valid() and account_form.is_valid() and human_form.is_valid():

            email = user_form.cleaned_data.get('email')

            q = User.objects.filter(email=email, is_active=True)
            if q.exists():
                return HttpResponseBadRequest('یک حساب کاربری با این بست الکتریکی وجود دارد.')

            if account_form.cleaned_data.get('caravan') != Account.CaravanType.MARRIED:
                gender = human_form.cleaned_data.get('gender')
                caravan = account_form.cleaned_data.get('caravan')
                if (gender == Human.Gender.MALE and caravan == Account.CaravanType.WOMEN) or (
                        gender == Human.Gender.FEMALE and caravan == Account.CaravanType.MEN):
                    return HttpResponseBadRequest('جنسیت وارد شده با کاروان انتخاب شده متناغض است')

            for user in User.objects.filter(email=email):
                user.delete()

            human = human_form.save()
            human.refresh_from_db()
            human.save()

            account = account_form.save()
            account.refresh_from_db()
            account.save()

            password = user_form.cleaned_data.get('password1')
            user = User.objects.create_user(username=account.id, password=password, email=email)
            user.save()
            user.is_active = False
            user.save()

            account.user = user
            account.human = human
            account.save()

            threading.Thread(target=send_activate_code, args=(request, user,)).start()

            return HttpResponse(status=200)

        else:
            error_list = [user_form.errors, account_form.errors, human_form.errors]
            error = create_error_text(error_list)
            return HttpResponseBadRequest(error)
    else:
        return render(request, 'accounting/signup.html')


def send_activate_code(request, user):
    current_site = get_current_site(request)
    token = TokenCode.create_new_token(account=user.account, type=TokenCode.TokenType.ACTIVATE)
    token.save()
    data = {
        'user': user,
        'domain': current_site.domain,
        'code': token.code,
    }
    html_content = render_to_string('accounting/activation.html', data)
    to_email = user.email
    subject, from_email, to = 'فعال سازی سامانه راه ناتمام', 'joorabnakhi@gmail.com', to_email
    text_content = 'This is an important message.'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@login_required
def panel(request):
    data = {
        'humans': {
            'self': request.user.account.human,
            'spouse': request.user.account.human.spouse,
            'children': Human.objects.filter(parent=request.user.account.human)
        }
    }
    return render(request, 'accounting/account_panel.html', data)


@login_required
def add_relative_human(request):
    if request.user.account.caravan != Account.CaravanType.MARRIED:
        return HttpResponseBadRequest('اضافه کردن خویشاوند تنها برای کاروان متاهلین تعریف شده است')
    relative_type = request.POST.get('relative_type')
    pass
    if request.POST:
        human_form = HumanForm(request.POST)
        if not human_form.is_valid():
            error_list = [human_form.errors]
            error = create_error_text(error_list)
            return HttpResponseBadRequest(error)

        human = request.user.account.human
        new_relative = human_form.save()
        if relative_type == 'SPOUSE':
            human.spouse = new_relative
            human.save()
        elif relative_type == 'CHILD':
            new_relative.parent = human
            new_relative.save()
        else:
            return HttpResponseBadRequest('رابطه خویشاوندی غلط')
        return HttpResponse(status=200)

    else:
        return HttpResponseBadRequest()


@login_required
@csrf_exempt
def delete_relative(request, human_id):
    if request.user.account.human.id is human_id:
        return HttpResponseBadRequest('شما نمیتوانید خودتان را حذف کنید')
    if request.user.account.caravan != Account.CaravanType.MARRIED:
        return HttpResponseBadRequest('شما در کاروان متاهلین نیستید')
    q = Human.objects.filter(id=human_id)
    if not q.exists():
        return HttpResponseBadRequest('کسی با این هویت وجود ندارد')
    else:
        relative = q.get()
        if relative.parent != request.user.account.human and request.user.account.human.spouse != relative:
            return HttpResponseBadRequest('این شخص خویشاوند شما نیست')
        else:
            relative.delete()
            return HttpResponse(status=200)


def login_view(request):
    error = None
    if request.POST:
        email = request.POST.get('email')
        password = request.POST.get('password')
        q = User.objects.filter(email=email)
        if not q.exists():
            error = 'هیچ حسابی با این ایمیل وجود ندارد'
        else:
            user = q.get()
            if not user.is_active:
                threading.Thread(target=send_activate_code, args=(request, user,)).start()
                info = 'کد فعال سازی برای ایمیل شما فرستاده شده است'
                return render(request, 'accounting/submit_activate.html', {'info': info})
            else:
                user = authenticate(request, username=user.username, password=password)

                if not user:
                    error = 'رمز وارد شده غلط است'
                else:
                    login(request, user)
                    return redirect('panel')
    return render(request, 'accounting/login.html', {'error': error})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


def activate(request):
    if request.POST:
        code = request.POST.get('code')
        q = TokenCode.objects.filter(code=code)
        if q.exists():
            token = q.first()
            account = token.account
            account.user.is_active = True
            account.user.save()
            for token in q:
                token.delete()
            return redirect('login')
        else:
            return render(request, 'accounting/submit_activate.html', {'error': 'چنین کد فعال سازی ای وجود ندارد'})
    return render(request, 'accounting/submit_activate.html')


def reset_password_view(request, code):
    pass


@login_required
def set_destination(request):
    if request.POST:
        destination = request.POST.get('return_destination')
        if [state[0] for state in Account.StateNames.choices].count(destination) is 0:
            return HttpResponseBadRequest('مقدار وارد شده صحیح نیست')
        request.user.account.return_destination = destination
        request.user.account.save()
        return HttpResponse(status=200)
    else:
        return HttpResponseBadRequest()


@csrf_exempt
@login_required
def delete_account(request):
    try:
        request.user.account.human.delete()
        request.user.account.delete()
        request.user.delete()
        return HttpResponse(status=200)
    except Exception as e:
        return HttpResponseBadRequest(str(e))
