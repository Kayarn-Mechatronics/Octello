from django.shortcuts import render

# Create your views here.
class DashboardView:
    def main_dashboard(request):
        return render(request, "DashboardApp/Base.html")