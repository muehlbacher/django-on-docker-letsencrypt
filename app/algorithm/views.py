import random
import json
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from .algorithms.particle import ParticleAlgo, Point
from django.contrib.sessions.models import Session
from django.core.files.storage import FileSystemStorage

from .utils import * 

# Initialize the particle algorithm
def get_particle_algo(request):
    if 'particle' not in request.session:
        print("New Particle")
        particle = None
        particle = ParticleAlgo(300, width=800, height=600)
        particle.create_particles()
        image = get_image('mediafiles/penguin_in_new_york.webp')
        particle.set_color(image)
        request.session['particle'] = particle.to_json()
    print("Before first request...")
    return request.session['particle']

def index(request):
    Session.objects.all().delete()

    particle = None
    # Generate random coordinates
    print("First index call")
    particle = get_particle_algo(request)

    particle = ParticleAlgo.from_json(particle)
    file_name = 'penguin_in_new_york.webp' 
    if request.method == 'POST':
        gbestx = request.POST.get('gbestx', 300)
        gbesty = request.POST.get('gbesty', 500)
        print("GBEST:")
        print(gbesty)
        gbestx = int(gbestx) if gbestx.isdigit() else 300
        gbesty = int(gbesty) if gbesty.isdigit() else 300
        particle.gbest = Point(gbestx, gbesty)

        file_name = request.POST.get('imagename', 'penguin_in_new_york.webp')
        if file_name != "":
            image = get_image('mediafiles/' + file_name)
            particle.set_color(image)
        #image = get_image('mediafiles/' + file_name)
        print("FILENAME:")
        print(file_name)

    print(particle)
    points = []
    for part in particle.particles:
        points.append({'x': part.x, 'y': part.y, 'size': 3, 'color': part.color})
    points_json = json.dumps(points)
    print("Before render...")
    request.session['particle'] = particle.to_json()
    return render(request, 'index.html', {'points': points_json, 'media_url': settings.MEDIA_URL, 'image_name': file_name})


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