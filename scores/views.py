from datetime import datetime

from django.http import HttpResponse

from auths.utils import decrypt_password
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
def get_scores(massarID, password, method=0):
    session = requests.Session()

    url_formulaire = 'https://massarservice.men.gov.ma/moutamadris/Account'

    response_formulaire = session.get(url_formulaire)
    soup = BeautifulSoup(response_formulaire.content, 'html.parser')

    token = soup.find('input', {'name': '__RequestVerificationToken'})['value']

    url_login = 'https://massarservice.men.gov.ma/moutamadris/Account'
    login_data = {
        '__RequestVerificationToken': token,
        'UserName': massarID,
        'Password': password
    }

    response_login = session.post(url_login, data=login_data)

    if response_login.status_code == 200 and "اسم المستخدم أو كلمة المرور غير صالحة" not in response_login.content.decode(
            'utf-8'):
        print('Connexion réussie')
    else:
        quit(f'Échec de la connexion : {response_login.status_code}')
    url = 'https://massarservice.men.gov.ma/moutamadris/General/SetCulture?culture=fr'
    session.get(url)
    url_api = 'https://massarservice.men.gov.ma/moutamadris/TuteurEleves/GetBulletins'
    api_data = {
        "Annee": datetime.now().year  if 9 <= datetime.now().month <= 12 else datetime.now().year - 1,
        "IdSession": "1" if 9 <= datetime.now().month <= 12 or 1 <= datetime.now().month < 2 else "2"
    }
    response_api = session.post(url_api, data=api_data)
    html_content = response_api.content
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', {'class': 'table table-bordered grid-table'})
    headers = [th.text.strip() for th in table.find('thead').find_all('th')]
    rows = table.find('tbody').find_all('tr')
    notes = {}
    for row in rows:
        columns = row.find_all('td')
        subject = columns[0].text.strip()
        first_exam = float(columns[1].text.strip().replace(',', '.')) if columns[1].text.strip() else None
        second_exam = float(columns[2].text.strip().replace(',', '.')) if columns[2].text.strip() else None
        third_exam = float(columns[3].text.strip().replace(',', '.')) if columns[3].text.strip() else None
        fourth_exam = float(columns[4].text.strip().replace(',', '.')) if columns[4].text.strip() else None
        activities = float(columns[5].text.strip().replace(',', '.')) if columns[5].text.strip() else None
        notes[subject] = (first_exam, second_exam, third_exam, fourth_exam, activities)

    if method == 0:
        notes_c = []
        for matiere in notes:
            notes_i = [matiere] + list(notes[matiere])
            notes_c.append(notes_i)
        return notes_c, headers
    else:
        return notes

@login_required(login_url="auths:login")
def display_scores(request):
    user = request.user
    scores = get_scores(user.massarID, decrypt_password(user.displayed_password))
    headers = scores[1]
    scores = scores[0]

    return render(request, "scores/index.html", context={"scores":scores, "headers" : headers})
def count_final_score(scores, coefs):
    N = 0
    for subject in coefs:
        N += coefs[subject]
    note_final = 0
    for subject in coefs:
        note = scores[subject]
        i = 0
        final = 0
        for n in note:
            if n is not None:
                i += 1
                final += n

        if not final == 0:
            final *= coefs[subject]
            final /= i
        else:
            N -= coefs[subject]
        note_final += final
    note_final = note_final / N
    return note_final
from django.http import JsonResponse

@login_required(login_url="auths:login")
def count_score(request):
    user = request.user
    scores = get_scores(user.massarID, decrypt_password(user.displayed_password))[0]
    subjects = [pack[0] for pack in scores]

    if request.method == "POST":
        coefs = {subject: int(request.POST.get(subject)) for subject in subjects}
        scores = get_scores(massarID=request.user.massarID, password=decrypt_password(request.user.displayed_password), method=1)
        final_score = count_final_score(scores, coefs)
        print(final_score)

        return HttpResponse(f"""<div id="final-score" class="text-base leading-relaxed text-gray-500 dark:text-gray-400"><p>Votre moyenne générale actuelle est : <span class="md:text-blue-700 font-semibold">{round(final_score, 2)}</span></p> </div>""")

    return render(request, "scores/count_score.html", context={"subjects": subjects})
