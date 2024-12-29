from django.shortcuts import render

from carsapp.models import Car
from brandsapp.models import Brand
# from posts.models import Post


def home(request,brand_slug=None):
    data = Car.objects.all()
    if brand_slug is not None:
        brand = Brand.objects.get(slug = brand_slug)
        data = Car.objects.filter(brand  = brand)
    brands = Brand.objects.all()
    # print(data)
    return render(request, 'home.html',{'data' : data, 'brands' : brands})