from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.contrib import messages
import requests
from bs4 import BeautifulSoup

from auths.models import User


def verify_form(massarID, passsword):
    session = requests.Session()

    url_formulaire = 'https://massarservice.men.gov.ma/moutamadris/Account'

    response_formulaire = session.get(url_formulaire)
    soup = BeautifulSoup(response_formulaire.content, 'html.parser')

    token = soup.find('input', {'name': '__RequestVerificationToken'})['value']

    url_login = 'https://massarservice.men.gov.ma/moutamadris/Account'
    login_data = {
        '__RequestVerificationToken': token,
        'UserName': massarID,
        'Password': passsword
    }
    response_login = session.post(url_login, data=login_data)

    if response_login.status_code == 200 and "اسم المستخدم أو كلمة المرور غير صالحة" not in response_login.content.decode('utf-8'):
        return True
    else:
        return False

def get_name(massarID, passsword):
    session = requests.Session()

    url_formulaire = 'https://massarservice.men.gov.ma/moutamadris/Account'

    response_formulaire = session.get(url_formulaire)
    soup = BeautifulSoup(response_formulaire.content, 'html.parser')

    token = soup.find('input', {'name': '__RequestVerificationToken'})['value']

    url_login = 'https://massarservice.men.gov.ma/moutamadris/Account'
    login_data = {
        '__RequestVerificationToken': token,
        'UserName': massarID,
        'Password': passsword
    }
    response_login = session.post(url_login, data=login_data)

    if response_login.status_code == 200 and "اسم المستخدم أو كلمة المرور غير صالحة" not in response_login.content.decode('utf-8'):
        url_api = 'https://massarservice.men.gov.ma/moutamadris/TuteurEleves/GetInfoEleve'
        response_api = session.get(url_api, headers={'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3'})
        soup = BeautifulSoup(response_api.content, 'html.parser')
        dt_first_name = soup.find('dt', string='الإسم')
        dt_last_name = soup.find('dt', string='النسب')
        if dt_first_name:
            dd_name = dt_first_name.find_next('dd').text
            first_name = dd_name.split('(')[-1].split(')')[0].capitalize()
        else:
            first_name = ""
        if dt_last_name:
            dd_name = dt_last_name.find_next('dd').text
            last_name = dd_name.split('(')[-1].split(')')[0].capitalize()
        else:
            last_name = ""

    return(first_name, last_name)

def login_user(request):
    if request.method == "POST":
        massarID = request.POST.get("massarID")
        if "@taalim.ma" not in massarID:
            massarID += "@taalim.ma"
        password = request.POST.get("password")
        user = User.objects.filter(massarID=massarID).first()
        if user is not None or verify_form(massarID, password):


            if user is not None:
                username = user.username
                user = authenticate(request, username=username, password=password)
                login(request, user)
                print("done")
                messages.success(request, 'sucess')
            else:
                name = get_name(massarID, password)
                first_name = name[0]
                last_name = name[1]
                username = f"{first_name} {last_name}"
                if username.replace(" ", "") == "":
                    username = massarID.replace("@taalim.ma", "")
                user = User.objects.create_user(username=username, first_name= first_name, last_name=last_name, massarID=massarID, password=password)
                login(request, user)
                messages.success(request, 'sucess')

        else:
            messages.error(request, 'Invalid MassarID or password')
    return render(request, 'auths/login.html')