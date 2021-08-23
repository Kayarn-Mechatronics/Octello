from django.shortcuts import render, redirect

# Create your views here.

class HomepageView:
    def home_page(request):
        return render(request, 'Index/Homepage.html')
           
class PricingView:
    def pricing_page(request):
        return render(request, 'Index/Pricing.html')