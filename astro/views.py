from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from astro.admin import Prev30
import json
import requests


def home(request):
    carousel = {
        'image': '',
        'caption_title': '',
        'caption_info': ''
    }
    carousels = [{
        'image': 'images/im1.jpg',
        'caption_title': 'We are Astro Club,VNIT',
        'caption': 'Are you one of those Space buffs? Wanna hone you amateur skills in Astronomy? Look no'
                   ' further you have reached your destination! Welcome to Astro Club VNIT!'
    }, {
        'image': 'images/im2.jpg',
        'caption_title': 'Sky is the limit',
        'caption': 'Have a look at this beautiful image🤩, capturing the Star trails, taken by our club '
                   'member Ojas Sharma.'
    },
        {
            'image': 'images/im4.jpg',
            'caption_title': '',
            'caption': 'Astronomy Club of VNIT, Ashlesha invites you to gaze upon the heavens and beyond and see'
                       ' the unfolding of the cosmic miracle.'
        }
    ]
    context = {
        'carousels': carousels
    }
    context['carousels'][0]['active'] = 'active'
    return render(request, 'index.html', context)


def about(request):
    carousel = {
        'image': '',
        'caption_title': '',
        'caption_info': ''
    }
    context = {
        'carousels': [
            {
                'image': 'images/about 1.jpg',
                'caption_title': '',
                'caption_info': ''
            },
            {
                'image': 'images/about 2.jpg',
                'caption_title': '',
                'caption_info': ''
            }
            ,
            {
                'image': 'images/about 3.jpg',
                'caption_title': '',
                'caption_info': ''
            }
            ,
            {
                'image': 'images/about 4.jpg',
                'caption_title': '',
                'caption_info': ''
            }
            ,
            {
                'image': 'images/about 5.jpg',
                'caption_title': '',
                'caption_info': ''
            }
        ]
    }
    context['carousels'][0]['active'] = 'active'
    return render(request, 'about.html', context)


def events(request):
    event = {
        'title': '',
        'description': '',  # can use basic html here
        'main_link_desc': '',
        'main_link': '',  # write if any else blank
        'additional links': [

        ]  # has  dicts of format {'description' : '','link_addr' :''}

    }
    context = {
        'events': []
    }
    context['events'].append({
        'title': 'Astro Quiz',
        'description': 'We are organising a quiz for astro-geeks !!! <br> It will contain 50 Questions <br> '
                       'time duration is 50 min.<br>Tighten your knowledge up for the same !!',
        'main_link_desc': 'Apply here',
        'main_link': 'https://www.google.com',
        'additional_links': [
            {'desc': 'Additional link one', 'link': 'https://www.facebook.com'},
            {'desc': 'Additional link two', 'link': 'https://www.facebook.com'}

        ]

    })
    context['events'].append({
        'title': 'Astro Quiz',
        'description': 'We are organising a quiz for astro-geeks !!! <br> It will contain 50 Questions <br> '
                       'time duration is 50 min.<br>Tighten your knowledge up for the same !!',
        'main_link_desc': 'Apply here',
        'main_link': 'https://www.google.com',
        'additional_links': [
            {'desc': 'Additional link one', 'link': 'https://www.facebook.com'},
            {'desc': 'Additional link two', 'link': 'https://www.facebook.com'}

        ],
    })

    if len(context['events']) != 0:
        context['events'][0]['active'] = 'active'
        return render(request, 'events.html', context)
    else:
        return render(request, 'noevents.html')


def other_sources(request):
    context = {

    }
    return render(request, 'otherSources.html', context)


def apod(request):
    api_url = 'https://api.nasa.gov/planetary/apod'
    my_key = 'gE4OwsHm4NSF3efofSsGRvxcJeT3abrR05xk3Usd'
    context = {
        'prev_30': [],  # array of objects of the form img_info
        'active': ''
    }
    if len(Prev30.objects.all()) == 0 or len(
            Prev30.objects.all().filter(date=datetime.today().strftime('%Y-%m-%d'))) == 0:
        todays_date = (datetime.today()-timedelta(days=1)).strftime('%Y-%m-%d')
        date_month_before = (datetime.today() - timedelta(days=29)).strftime('%Y-%m-%d')
        print(date_month_before,todays_date)
        response = requests.get(f'{api_url}?start_date={date_month_before}&end_date={todays_date}&api_key={my_key}')
        context['prev_30'] = json.loads(response.text)[::-1]
        print(type(context['prev_30']))
        print(context['prev_30'])
        for i in context['prev_30']:
            entry = Prev30()
            print(i)
            entry.url = i['url']
            entry.date = i['date']
            entry.title = i['title']
            entry.explanation = i['explanation']
            entry.save()

    else:
        todays_date = datetime.today()-timedelta(days=1)
        for day_back in range(0, 30):
            entry = Prev30.objects.all().get(date=(todays_date - timedelta(day_back)).strftime('%Y-%m-%d'))
            new_context_data = dict()
            new_context_data['url'] = entry.url
            new_context_data['date'] = entry.date
            new_context_data['title'] = entry.title
            new_context_data['explanation'] = entry.explanation
            context['prev_30'].append(new_context_data)
    context['prev_30'][0]['active'] = 'active'
    return render(request, 'apod.html', context)