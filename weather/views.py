from django.shortcuts import render
import requests
from .forms import CityForm
# Create your views here.

def get_weather(request):
    form = CityForm()
    weather_data = {
        'city': 'Kigali',
        'country' :'Rwanda',
        'temperature': 13,
        'humidity' : 30,
        'description': 'Mostly Cloudy',
        'icon': "{% static 'assets/icons8-partly-cloudy-day-96.png' %}",
    }

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            api_key = 'f19129b99e2242a6bd1144418242809'
            url = 'http://api.weatherapi.com/v1/current.json'
            data = {
                "key": api_key,
                "q": city
            }
            reponse = requests.post(url=url, data=data)
            if reponse.status_code == 200:
                result = reponse.json()
                weather_data = {
                    'city': result["location"]["name"],
                    'country' : result['location']['country'],
                    'temperature': result["current"]['temp_c'],
                    'humidity' : result['current']['humidity'],
                    'description': result["current"]["condition"]["text"],
                    'icon': result["current"]["condition"]["icon"]
                }
            else:
                weather_data = {'error' : 'City not found'}
    return render(request, 'weather.html', {'form': form, 'weather_data': weather_data})