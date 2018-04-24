from django.shortcuts import render,  HttpResponse

def home(request):

	return render(request, 'food_app/index.html')

def process(request):

	if request.method == "POST":

		return render(request, 'food_app/stage.html')