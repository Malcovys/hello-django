from django.http import HttpResponse
from listing.models import Band
from django.shortcuts import render

def hello(request):
    band = Band.objects.all()
    return HttpResponse(f"""
        <h1>Band List</h1>
        <p>Group préférés:</p>
        <ul>
            <li>{band[0].name}</li>
            <li>{band[1].name}</li>
            <li>{band[2].name}</li>                
        </ul>
    """)