from django.shortcuts import render
from django.views.generic import DetailView
from . import forms
from . import models
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.


class DetailCarView(DetailView):
    model = models.Car
    pk_url_kwarg = 'id'
    template_name = 'car_details.html'
    
    def post(self, request, *args, **kwargs):
        comment_form = forms.CommentForm(data=self.request.POST)
        car = self.get_object()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.car = car
            new_comment.save()
        return self.get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car = self.object 
        comments = car.comments.all()
        comment_form = forms.CommentForm()
        
        context['comments'] = comments
        context['comment_form'] = comment_form
        return context
    

@login_required
def buy_car(request, car_id):
    car = get_object_or_404(models.Car, id=car_id)

    if car.quantity > 0:
        # Create an order for the authenticated user
        models.Order.objects.create(user=request.user, car=car)
        # Reduce the car quantity by 1
        car.quantity -= 1
        car.save()
        messages.success(request, f"You have successfully purchased {car.name}.")
    else:
        messages.error(request, f"Sorry, {car.name} is out of stock.")

    return redirect('profile')  