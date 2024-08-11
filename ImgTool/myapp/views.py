import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from PIL import Image
import pilgram
import requests


# Create your views here.

def home(request):
    return render(request,'home.html')

def about(request):
    return render(request,'about.html')

def cats(request):
    return render(request,'cats.html')

def Dogs(request):
    return render(request,'Dogs.html')

def image_filter(request):
    return render(request,'image_filter.html')


def cataas(request, tag=None, text=None, fontSize=None, fontColor=None):
    # Base URL for Cataas API
    base_url = "https://cataas.com/cat"

    if tag:
        # Handle /cat/:tag
        url = f"{base_url}/{tag}"
    elif text and fontSize and fontColor:
        # Handle /cat/says/:text?fontSize=:size&fontColor=:color
        url = f"{base_url}/says/{text}?fontSize={fontSize}&color={fontColor}"
    elif text:
        # Handle /cat/says/:text
        url = f"{base_url}/says/{text}"
    else:
        # Handle /cat and /cat/gif
        url = f"{base_url}/gif" if request.path.endswith("gif/") else base_url

    # Fetch the image from the Cataas API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        return HttpResponse(response.content, content_type="image/jpeg")
    else:
        return HttpResponseBadRequest("Invalid request or Cat not found")

def random_dog(request):
    # URL for random dog image
    url = "https://dog.ceo/api/breeds/image/random"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        image_url = response.json().get('message')
        return HttpResponse(f"<img src='{image_url}' alt='Random Dog Image'>")
    else:
        return HttpResponseBadRequest("Failed to fetch the dog image")

def random_dog_by_breed(request, breed):
    # URL for random dog image by breed
    url = f"https://dog.ceo/api/breed/{breed}/images/random"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        image_url = response.json().get('message')
        return HttpResponse(f"<img src='{image_url}' alt='Random Dog Image of {breed}'>")
    else:
        return HttpResponseBadRequest("Failed to fetch the dog image or breed not found")
    

def image_filter_view(request):
    filters = pilgram.__all__  # Get all Pilgram filters

    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        image = Image.open(image_file)

        filter_name = request.POST.get('filter')

        if filter_name and hasattr(pilgram, filter_name):
            filter_function = getattr(pilgram, filter_name)
            filtered_image = filter_function(image)
        else:
            filtered_image = image

        # Define path for saving the filtered image
        filtered_image_name = 'filtered_image.jpg'
        filtered_image_path = os.path.join(settings.MEDIA_ROOT, filtered_image_name)
        filtered_image.save(filtered_image_path)

        # Redirect to the view that displays the filtered image
        return redirect('display_filtered_image', image_name=filtered_image_name)

    return render(request, 'image_filter.html', {
        'filters': filters,
    })

def display_filtered_image(request, image_name):
    image_url = os.path.join(settings.MEDIA_URL, image_name)
    return render(request, 'display_image.html', {'image_url': image_url})