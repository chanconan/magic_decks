from uuid import uuid4
from urllib.parse import urlparse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST, require_http_methods
from django.shortcuts import render
from django.http import JsonResponse
from scrapyd_api import ScrapydAPI
from decks.models import ScrapyItem

# connect scrapyd service
scrapyd = ScrapydAPI('http://localhost:6800')

def is_valid_url(url):
    validate = URLValidator()
    try:
        validate(url) # check if url format is valid
    except ValidationError:
        return False

    return True


# Create your views here.
def index(request):
    return render(request, "index.html")

@require_http_methods(['POST', 'GET']) # only get and post
def crawl(request):
    #Create a new crawling request
    if request.method == 'POST':
        url = request.POST.get('url', None) #need to determine how Scrapy works. Only have to use mtgtop8 website

        if not url:
            return JsonResponse({'error': 'Missing  args'})
        
        if not is_valid_url(url):
            return JsonResponse({'error': 'Not a valid URL'})
        
        domain = urlparse(url).netloc
        unique_id = str(uuid4()) # create a unique ID. 
        settings = {
            'unique_id': unique_id, # unique ID for each record for DB
            'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        }

        task = scrapyd.schedule('default', 'icrawler', 
            settings=settings, url=url, domain=domain)

        return JsonResponse({'task_id': task, 'unique_id': unique_id, 'status': 'started' })
    
    elif request.method == 'GET':
        task_id = request.GET.get('task_id', None)
        unique_id = request.GET.get('unique_id', None)

        if not task_id or not unique_id:
            return JsonResponse({'error': 'Missing args'})

        status = scrapyd.job_status('default', task_id)
        if status == 'finished':
            try:
                # this is the unique_id that we created even before crawling started.
                item = ScrapyItem.objects.get(unique_id=unique_id) 
                return JsonResponse({'data': item.to_dict['data']})
            except Exception as e:
                return JsonResponse({'error': str(e)})
        else:
            return JsonResponse({'status': status})