from django.shortcuts import render

def privacy_policy(request):
    return render(request, "info/privacy_policy.html")
