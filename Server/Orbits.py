import os
import numpy as np
import configparser
import requests
import json

# Configuration des corps
bodies = {}

# Chargement des fichiers de configuration
config_files = [f for f in os.listdir('./Data/') if f.endswith('.cfg')]
for filename in config_files:
    config = configparser.ConfigParser()
    config.read('./Data/' + filename)
    name = config['Body']['name']
    mass = float(config['Properties']['mass'])
    radius = float(config['Properties']['radius'])

    orbit = {
        'semiMajorAxis': float(config['Orbit']['semiMajorAxis']),
        'eccentricity': float(config['Orbit']['eccentricity']),
        'inclination': float(config['Orbit']['inclination']),
        'meanAnomalyAtEpochD': float(config['Orbit']['meanAnomalyAtEpochD']),
        'longitudeOfAscendingNode': float(config['Orbit']['longitudeOfAscendingNode']),
        'argumentOfPeriapsis': float(config['Orbit']['argumentOfPeriapsis'])
    }
    rotation_period = float(config['Properties']['rotationPeriod'])
    albedo = float(config['Properties']['albedo'])
    bodies[name] = {
        'mass': mass,
        'radius': radius,
        'orbit': orbit,
        'rotation_period': rotation_period,
        'albedo': albedo,
        'position': np.zeros(3),
        'velocity': np.zeros(3),
        'acceleration': np.zeros(3),
        'rotation': np.eye(3)
    }

# Initialisation des variables
timestep = 60 * 60  # Une heure
num_steps = 24 * 365 * 10  # 10 ans
time = np.arange(0, num_steps*timestep, timestep)

# Initialisation des positions et vitesses initiales
for body in bodies.values():
    orbit = body['orbit']
    a = orbit['semiMajorAxis']
    e = orbit['eccentricity']
    i = orbit['inclination']
    M0 = orbit['meanAnomalyAtEpochD']
    omega = orbit['argumentOfPeriapsis']
    Omega = orbit['longitudeOfAscendingNode']
    mu = 6.67430e-11 * bodies['Sun']['mass']
    E0 = M0 + e*np.sin(M0)
    x0 = a*(np.cos(E0) - e)
    y0 = a*np.sqrt(1 - e**2) * np.sin(E0)
    r0 = np.array([x0, y0, 0])
    if a != 0:
        v0 = np.sqrt(mu/a) / (1 - e*np.cos(E0)) * np.array([-np.sin(E0), np.sqrt(1 - e**2)*np.cos(E0), 0])
    else:
        v0 = np.array([0, 0, 0])
    R = np.array([
        [np.cos(omega)*np.cos(Omega) - np.sin(omega)*np.sin(Omega)*np.cos(i),
         -np.sin(omega)*np.cos(Omega) - np.cos(omega)*np.sin(Omega)*np.cos(i),
         np.sin(i)*np.sin(Omega)],
        [np.cos(omega)*np.sin(Omega) + np.sin(omega)*np.cos(Omega)*np.cos(i),
         -np.sin(omega)*np.sin(Omega) + np.cos(omega)*np.cos(Omega)*np.cos(i),
            -np.sin(i)*np.cos(Omega)],
        [np.sin(omega)*np.sin(i), np.cos(omega)*np.sin(i), np.cos(i)]
    ])

    body['position'] = np.dot(R, r0)
    body['velocity'] = np.dot(R, v0)

# Calcul des positions et vitesses
for t in time:
    # Calcul des accélérations
    for body in bodies.values():
        body['acceleration'] = np.zeros(3)
    for body1 in bodies.values():
        for body2 in bodies.values():
            if body1 != body2:
                r = body2['position'] - body1['position']
                body1['acceleration'] += -6.67430e-11 * body2['mass'] / np.linalg.norm(r)**3 * r

    # Calcul des positions et vitesses
    for body in bodies.values():
        body['position'] += body['velocity'] * timestep
        body['velocity'] += body['acceleration'] * timestep

# Calcul des angles de rotation
for body in bodies.values():
    body['rotation'] = np.eye(3)
    body['rotation'][0, 0] = np.cos(2*np.pi*time/body['rotation_period'])[0]
    body['rotation'][0, 1] = -np.sin(2*np.pi*time/body['rotation_period'])[0]
    body['rotation'][1, 0] = np.sin(2*np.pi*time/body['rotation_period'])[0]
    body['rotation'][1, 1] = np.cos(2*np.pi*time/body['rotation_period'])[0]

# Envoi des données au serveur
for t in time:
    data = {}
    for name, body in bodies.items():
        data[name] = {
            'position': body['position'],
            'velocity': body['velocity'],
            'acceleration': body['acceleration'],
            'rotation': body['rotation']
        }
    """s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 12345))
    s.sendall(bytes(str(data), 'utf-8'))
    s.close()
"""
    print(data)
    # Enregistrer les données en packet JSON
    with open('Data/Orbits.json', 'w') as f:
        json.dump(data, f)
    # Envoyer le packet JSON au serveur
    r = requests.post('http://localhost:12345', json=data)
    print(r.status_code)

