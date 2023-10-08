from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Listing
from .choices import price_choices, bedroom_choices, state_choices

# Create your views here.

# pylint: disable=no-member  # Disable the Pylint warning about 'objects' not being a member


def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)
    paginator = Paginator(listings, 3)
    page_number = request.GET.get("page")
    paged_listings = paginator.get_page(page_number)

    context = {
        'listings': paged_listings,

    }
    return render(request, 'listings/listings.html', context)


def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    other_images = []
    # iterate over photo_1 up to but not including photo_7 (doesn't exist)
    # append the url, only if it exists on the object. We get a ValueError
    # if it doesn't. The try/except block helps us mitigate this while
    # still throwing errors for other unexpected problems.
    for n in range(1, 7):
        try:
            other_images.append(getattr(listing, f'photos_{n}').url)
        except ValueError:
            continue

    # We should now have a list with a variable length of 1-6 to pass
    # onto the Django template. Pass it along with the listing in the
    # context.
    context = {
        'listing': listing,
        'other_images': other_images
    }

    return render(request, 'listings/listing.html', context)


def search(request):
    queryset_list = Listing.objects.order_by('-list_date')
    # Keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(
                description__icontains=keywords)

    # Filter by exact city
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)

    # Filter by exact state
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list = queryset_list.filter(state__iexact=state)

    # Filter by max bedrooms
    if 'bedroom' in request.GET:
        bedroom = request.GET['bedroom']
        if bedroom:
            queryset_list = queryset_list.filter(bedroom__iexact=bedroom)

    # Filter by max price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price)

    context = {
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'listings': queryset_list,
        'values': request.GET,
    }
    return render(request, 'listings/search.html', context)
