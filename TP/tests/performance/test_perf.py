import time
import random
import struct
import src.serializer as serializer
import src.core as core

def generer_binaire_random(n=10000):
    """Fonction utilitaire pour créer un faux PointSet binaire avec N points.

    On le fait a la main pour ne pas utiliser le serializer dans la generation.
    """
    points = []
    # On genere des coordonnees au hasard
    for i in range(n):
        x = random.random() * 1000.0
        y = random.random() * 1000.0
        points.append((x, y))

    # On construit le binaire manuellement
    buffer = bytearray()

    # Header : nombre de points
    buffer.extend(struct.pack('<L', n))

    # Corps : les points
    for p in points:
        buffer.extend(struct.pack('<ff', p[0], p[1]))

    return bytes(buffer)

def test_performance_gros_volume():
    """Test de charge avec 10 000 points.

    On verifie que tout le processus prend moins de 2 secondes.
    """
    NB_POINTS = 10000
    print(f"\nPreparation de {NB_POINTS} points...")

    # Generation des donnees (hors du temps mesuré)
    raw_data = generer_binaire_random(NB_POINTS)

    print("Debut du chrono...")
    # --- DEBUT CHRONO ---
    start = time.time()

    # 1. Lecture du binaire
    liste_points = serializer.point_set_from_bytes(raw_data)

    # 2. Calcul triangulation
    triangles = core.triangulate(liste_points)

    end = time.time()
    # --- FIN CHRONO ---

    duree = end - start

    print("Temps ecoulé : " + str(duree) + " secondes")
    print("Nombre de triangles : " + str(len(triangles)))

    # Verification de la perf
    # L'algo doit etre rapide (moins de 2s)
    assert duree < 2.0
