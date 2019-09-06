from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests, json
from forms.forms import UploadForm
from django.core.files.storage import FileSystemStorage

# Create your views here.
def test(request):
    """ Exemple de page non valide au niveau HTML pour que l'exemple soit concis """
    return HttpResponse("""
        <h1>Bienvenue Statfive !</h1>
        <p>Les stats comme sur FIFA !</p>
    """)

def login(request):
    return render(request, 'panel/login.html', {'data': 'Register pour un Five'})


def panel(request):
    return render(request, 'panel/panel.html', {'data': 'Bonjour'})

def upload(request):
    response = ""
    url = "http://163.5.245.188:5000/video"
    if request.method == 'POST':
        if request.FILES['video'] and request.POST['teamA'] and request.POST['teamB']:
            video1 = request.FILES['video']
            teamA =  request.POST['teamA']
            teamB =  request.POST['teamB']
            video = {'video': video1}
            data = {'teamA':teamA, 'teamB': teamB}
            requests.post(url,files=video, data=data)
            response = "Le fichier a été upload"
            return render(request, 'panel/upload.html', {'data': response})
        else:
            response = "Rien de posté"
            return render(request, 'panel/upload.html', {'data': response})
    else:
        return render(request, 'panel/upload.html', {'data': response})