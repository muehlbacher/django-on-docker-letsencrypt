import random
import json
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from .algorithms.particle import ParticleAlgo, Point
from django.contrib.sessions.models import Session
from .utils import * 

# Initialize the particle algorithm
def get_particle_algo(request):
    if 'particle' not in request.session:
        print("New Particle")
        particle = None
        particle = ParticleAlgo(300, width=800, height=600)
        particle.create_particles()
        #image = get_image('static/test.png')
        image = get_image('mediafiles/penguin_in_new_york.webp')
        particle.set_color(image)
        #print(particle.particles)
        request.session['particle'] = particle.to_json()


    print("Before first request...")
    return request.session['particle']

def index(request):
    Session.objects.all().delete()

    particle = None
    #request.session['particle'] = None  
    # Generate random coordinates
    print("First index call")
    particle = get_particle_algo(request)

    particle = ParticleAlgo.from_json(particle)

    if request.method == 'POST':
        gbestx = request.POST.get('gbestx', 300)
        gbesty = request.POST.get('gbesty', 500)
        print("GBEST:")
        print(gbesty)
        gbestx = int(gbestx) if gbestx.isdigit() else 300
        gbesty = int(gbesty) if gbesty.isdigit() else 300
        particle.gbest = Point(gbestx, gbesty)

    print(particle)
    #particle = ParticleAlgo.from_json(particle)
    #particle.create_particles()
    points = []
    for part in particle.particles:
        points.append({'x': part.x, 'y': part.y, 'size': 3, 'color': part.color})
    #points = [{'x': random.randint(0, 800), 'y': random.randint(0, 600), 'size': 10} for _ in range(5)]
    points_json = json.dumps(points)
    print("Before render...")
    request.session['particle'] = particle.to_json()
    #print(request.session['particle'])
    #print(points_json)
    return render(request, 'index.html', {'points': points_json, 'media_url': settings.MEDIA_URL})


def get_new_coordinates(request):
    print("Get new Coordinates...")
    particle = get_particle_algo(request)
    particle = ParticleAlgo.from_json(particle)
    print(particle.gbest)
    #print(particle.particles)
    particle.update()
    points = []
    for part in particle.particles:
        points.append({'x': part.x, 'y': part.y, 'size': 3, 'color': part.color})
    request.session['particle'] = particle.to_json()
    #points_json = [{'x': random.randint(0, 800), 'y': random.randint(0, 600), 'size': 10} for _ in range(5)]
    return JsonResponse({'points': points})