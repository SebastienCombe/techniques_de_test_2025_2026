import src.core as core

def test_triangle_simple():
    """Test basique : 3 points doivent faire 1 triangle."""
    # 3 points en triangle rectangle
    points = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]

    resultat = core.triangulate(points)

    # On doit avoir exactement un triangle
    assert len(resultat) == 1

    # Le triangle doit contenir les indices 0, 1 et 2
    triangle = resultat[0]
    # On verifie que les indices sont bien ceux des points donnés
    assert 0 in triangle
    assert 1 in triangle
    assert 2 in triangle

def test_forme_carre():
    """4 points doivent être coupés en 2 triangles."""
    points = [(0,0), (1,0), (1,1), (0,1)]
    resultat = core.triangulate(points)

    # Avec 4 points, on s'attend a 2 triangles (N-2)
    assert len(resultat) == 2

def test_pas_assez_de_points():
    """Test des cas limites (moins de 3 points)."""
    # Liste vide
    assert core.triangulate([]) == []

    # 2 points (pas assez pour faire un triangle)
    assert core.triangulate([(0,0), (1,1)]) == []
