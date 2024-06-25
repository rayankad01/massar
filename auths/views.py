from datetime import datetime
from auths.utils import encrypt_password
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
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

def get_class(massarID, passsword):
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
        url_api_change_langage = 'https://massarservice.men.gov.ma/moutamadris/General/SetCulture?culture=fr'
        session.get(url_api_change_langage)
        url_api = 'https://massarservice.men.gov.ma/moutamadris/TuteurEleves/GetBulletins'

        api_data = {
            "Annee": datetime.now().year if 9 <= datetime.now().month <= 12 else datetime.now().year-1  ,
            "IdSession":"1" if 9 <= datetime.now().month <= 12 or 1 <= datetime.now().month < 2 else "2"
        }
        print(api_data)

        response_api = session.post(url_api, data=api_data)
        html_content = response_api.content
        soup = BeautifulSoup(html_content, 'html.parser')
        dt_classe = soup.find('dt', string='Niveau')
        if dt_classe:
            classe = dt_classe.find_next('dd').text
            return classe

def login_user(request):
    if request.method == "POST":
        massarID = request.POST.get("massarID")
        if "@taalim.ma" not in massarID:
            massarID += "@taalim.ma"
        password = request.POST.get("password")
        user = User.objects.filter(massarID=massarID).first()
        if user is not None or verify_form(massarID, password):


            if user is not None:
                classe = get_class(massarID, password)
                username = user.username
                user = authenticate(request, username=username, password=password)
                if user:
                    user.classe = classe
                    print(classe)
                    user.save()
                    login(request, user)
                    print("done")
                    messages.success(request, 'Vous avez été connécté avec succès')
                    return redirect("scores:display")
                else:
                    messages.error(request, 'MassarID ou mot de passe invalide, veuillez réessayer')
            else:
                name = get_name(massarID, password)
                first_name = name[0]
                last_name = name[1]
                username = f"{first_name} {last_name}"
                if username.replace(" ", "") == "":
                    username = massarID.replace("@taalim.ma", "")
                classe = get_class(massarID, password)
                print(classe)
                user = User.objects.create_user(username=username, first_name= first_name, last_name=last_name, massarID=massarID, classe=classe, password=password, displayed_password = encrypt_password(password))
                login(request, user)
                classe = get_class(massarID, password)
                user.classe = classe
                messages.success(request, 'Le compte MassarPlus a été créé avec succès')
                return redirect("scores:display")

        else:
            messages.error(request, 'MassarID ou mot de passe invalide, veuillez réessayer')
    return render(request, 'auths/login.html')