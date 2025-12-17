import struct

def point_set_from_bytes(data):
    """Fonction pour lire les points depuis le format binaire.

    Renvoie une liste de tuples (x, y).
    """
    res = []
    cursor = 0

    # On met tout dans un try pour eviter que ca plante si les données sont mauvaises
    try:
        # On recupere le nombre de points (4 premiers octets)
        nb_points = struct.unpack('<L', data[0:4])[0]
        cursor = 4

        # 2. On boucle pour recuperer chaque point
        for i in range(nb_points):
            # Chaque point fait 8 octets (2 float de 4 octets)
            chunk = data[cursor : cursor + 8]

            # Si le morceau est trop petit, c'est que le fichier est corrompu
            if len(chunk) < 8:
                break

            valeurs = struct.unpack('<ff', chunk)
            x = valeurs[0]
            y = valeurs[1]

            res.append((x, y))
            cursor += 8

    except Exception:
        # En cas de probleme de lecture on renvoie une liste vide
        return []

    return res

def triangles_to_bytes(points, triangles):
    """Transforme la liste de points et triangles en format binaire.

    Format specifié dans le sujet.
    """
    output = bytearray()

    # --- Partie Points --- #
    nb_points = len(points)
    # On ecrit la taille
    output.extend(struct.pack('<L', nb_points))

    # On ecrit les coordonnées
    for p in points:
        output.extend(struct.pack('<ff', p[0], p[1]))

    # --- Partie Triangles --- #
    nb_triangles = len(triangles)
    output.extend(struct.pack('<L', nb_triangles))

    # On ecrit les indices des triangles
    for t in triangles:
        # On ecrit les 3 indices des sommets (3 unsigned long)
        output.extend(struct.pack('<LLL', t[0], t[1], t[2]))

    return bytes(output)
