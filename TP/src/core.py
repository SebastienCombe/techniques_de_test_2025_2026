def triangulate(points):
    """Fonction qui calcule la triangulation à partir d'une liste de points.

    On utilise une approche simple : on trie les points et on les relie au premier.
    """
    # On recupere le nombre de points
    n = len(points)

    # Gestion des cas limites
    if n < 3:
        return []

    if n == 3:
        # Si on a que 3 points, on retourne directement le triangle 0, 1, 2
        return [(0, 1, 2)]

    # Etape 1 : On doit garder les indices d'origine avant de trier
    # On va creer une liste temporaire avec (indice, point)
    points_avec_indices = []
    for i in range(n):
        points_avec_indices.append((i, points[i]))

    # Etape 2 : On trie les points
    # On trie selon les coordonnées (x, y) qui sont en position 1 dans notre tuple
    liste_triee = sorted(points_avec_indices, key=lambda x: x[1])

    # Etape 3 : Création des triangles
    resultat = []

    # On utilise le premier point trié comme point de reference (pivot)
    pivot = liste_triee[0]
    idx_pivot = pivot[0]

    # On parcourt le reste de la liste pour former des triangles en éventail
    # On va jusqu'à n-1 car on a besoin de paires de points
    for i in range(1, n - 1):
        # On recupere les deux points suivants dans la liste triée
        p1 = liste_triee[i]
        p2 = liste_triee[i+1]

        # On recupere leurs indices d'origine
        idx1 = p1[0]
        idx2 = p2[0]

        # On ajoute le triangle formé par (Pivot, Point A, Point B)
        # Un triangle est definit par les indices de ses sommets
        triangle = (idx_pivot, idx1, idx2)
        resultat.append(triangle)

    return resultat
