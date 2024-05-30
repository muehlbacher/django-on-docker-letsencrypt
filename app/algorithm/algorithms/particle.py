
import random
import json
from dataclasses import dataclass, asdict

@dataclass
class Point:
    x: float
    y: float

    def to_dict(self):
        return asdict(self)
    
    @staticmethod
    def from_dict(data):
        return Point(x=data['x'], y=data['y'])


@dataclass
class Particle:
    x: float
    y: float
    fitness: float
    pi: Point
    r1: float = 0.01
    r2: float = 0.01
    vx: float = 0
    vy: float = 0
    color: tuple = (0,255,0)

    def to_dict(self):
        data = asdict(self)
        data['pi'] = self.pi.to_dict()  # Serialize the nested Point
        return data

    @staticmethod
    def from_dict(data):
        return Particle(
            x=data['x'],
            y=data['y'],
            fitness=data['fitness'],
            pi=Point.from_dict(data['pi']),
            r1=data['r1'],
            r2=data['r2'],
            vx=data['vx'],
            vy=data['vy'],
            color=data['color']
        )

class ParticleAlgo:
    def __init__(self, n: int, width: int, height: int, particles = None, gbest = None):
        self.n = n
        self.particles = []
        if particles:
            self.particles = particles
        self.width = width
        self.height = height
        if gbest:
            self.gbest = gbest
        else:
            self.gbest = Point(100,100)

    def to_json(self):
        # Serialize the object manually
        return json.dumps({
            'n': self.n,
            'width': self.width,
            'height': self.height,
            'particles': [particle.to_dict() for particle in self.particles],
            'gbest': self.gbest.to_dict()
        })

    @staticmethod
    def from_json(json_str):
        data = json.loads(json_str)
        particles = [Particle.from_dict(p) for p in data['particles']]
        gbest = Point.from_dict(data['gbest'])
        return ParticleAlgo(
            n=data['n'],
            width=data['width'],
            height=data['height'],
            particles=particles,
            gbest=gbest
        )

    def fitness_function_old(self, position):
        return sum(x**2 for x in position)
    
    def fitness_function(self, position):
        x = position[0]
        y = position[1]
        return (x - self.gbest.x)**2 + (y - self.gbest.y)**2
    
    def fitness_function_old(self, position):
        x = position[0]
        y = position[1]
        return (x - 30) **2 + (y - 30) **2
    
    def determine_g_best(self):
        self.gbest_fitness = self.fitness_function((self.gbest.x, self.gbest.y))
        #for particle in self.particles:
        #    fitness = self.fitness_function((particle.x, particle.y))
        #    if fitness < self.gbest_fitness:
        #        self.gbest_fitness = fitness
        #        self.gbest.x = particle.x
        #        self.gbest.y = particle.y
    
    def create_particles(self):
        self.particles = []
        for i in range(self.n):
            x = random.randint(0, self.width-1)
            y = random.randint(0, self.height-1)
            particle = Particle(x=x, 
                                y=y,
                                fitness = self.fitness_function((x,y)),
                                pi=Point(x,y),
                                r1 = random.uniform(0,0.2),
                                r2 = random.uniform(0,0.2)
                        )
            
            self.particles.append(particle)

    def calculate_velocity(self, particle: Particle):
        #r1 = particle.r1
        #r2 = particle.r2
        r1 = random.uniform(0,0.0001)
        r2 = random.uniform(0,0.0001)
        particle.vx = particle.vx  + 0.01*r1*(particle.pi.x - particle.x) + 100*r2 * (self.gbest.x - particle.x)
        particle.vy = particle.vy  + 0.01*r1*(particle.pi.y - particle.y) + 100*r2 * (self.gbest.y - particle.y)
    
    def update_position(self, particle: Particle):
        particle.x = particle.x + particle.vx
        particle.y = particle.y + particle.vy

        # 0 < x < self.width
        particle.x = min(self.width, particle.x)
        particle.x = max(0, particle.x)

        #0 < y < self.height
        particle.y = min(self.height, particle.y)
        particle.y = max(0, particle.y)

    
    def measure_fitness(self, particle:Particle):
        return self.fitness_function((particle.x, particle.y))

    def update(self):
        for particle in self.particles:
            #calculate velocity (8.1)
            self.calculate_velocity(particle)
            #update position (8.2)
            self.update_position(particle)
            #measure fitness of new location
            new_fitness = self.measure_fitness(particle)
            particle.fitness = min(particle.fitness, new_fitness)

        #find particle with highest fitness
        self.determine_g_best()

    def set_color(self, image):
        resized_image = image.resize((self.width, self.height))

        for particle in self.particles:
            try:
                particle.color = resized_image.getpixel((particle.x, particle.y))
            except IndexError as e:
                print("ERROR!!!")
                print(f"X:{particle.x}, Y:{particle.y}")

        
