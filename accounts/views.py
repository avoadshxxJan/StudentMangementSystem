from django.shortcuts import render


def home_view(request):
    """
    Landing page showcasing EduTrack system status, module architecture,
    access control rules, and illustrative yearly academic progress.
    """
    return render(request, 'home.html')
