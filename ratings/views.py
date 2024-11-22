from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from .models import Rating, Review
from .forms import ReviewForm
from django.http import JsonResponse

#create the views here
def main_view(request):
    """ A view to display an image with the rating functionality and reviews """
    obj = Rating.objects.filter(score=0).order_by("?").first()
    print(obj)
    reviews = obj.reviews.all() if obj else []
    review_form = ReviewForm()  # Form to handle new reviews
    
    context = {
        'object': obj,
        'reviews': reviews,
        'review_form': review_form,
    }
    return render(request, 'ratings/main.html', context)

def create_review(request, image_id):
    """ A view to handle creating reviews """
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.image = Rating.objects.get(id=image_id)
            review.user = request.user  # Assuming the user is logged in
            review.save()
            messages.success(request, 'Review added successfully.')
        else:
            messages.error(request, 'Something went wrong. Please try again.')

    return redirect('main-view')



def rate_image(request):
    if request.method == 'POST':
        el_id = request.POST.get('el_id')
        val = request.POST.get('val')
        print(f"Received ID: {el_id}, Value: {val}")  # Debugging

        try:
            obj = Rating.objects.get(id=el_id)
            obj.score = val
            obj.save()
            return JsonResponse({'success':'true', 'score': val}, safe=False)
        except ObjectDoesNotExist:
            return JsonResponse({'success':'false','error': 'Rating does not exist'})
    return JsonResponse({'success': 'false', 'error': 'Invalid request method'})