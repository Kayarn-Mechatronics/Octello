from django.shortcuts import render

# Create your views here.
class WizzardsListView:
    def wizzards_list(request):
        return render(request, 'WizzardApp/Wizzards-list.html')