from django.shortcuts import render


def home_view(request):
    """
    Public landing page for EduTrack.
    Renders Phase 1 informational overview of the institutional platform.
    """
    return render(request, 'pages/home.html')
