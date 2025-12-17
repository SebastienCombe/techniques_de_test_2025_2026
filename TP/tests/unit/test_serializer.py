import struct
import src.serializer as serializer

def test_lecture_normale(sample_point_set_bytes):
    """Test basique.

    On donne des données valides (via la fixture).
    On recupere des points.
    """
    points = serializer.point_set_from_bytes(sample_point_set_bytes)

    # On doit avoir 3 points
    assert len(points) == 3
    # Verification des valeurs
    assert points[0] == (0.0, 0.0)
    assert points[2] == (0.0, 1.0)

def test_lecture_vide():
    """Test avec 0 points."""
    # On cree un header binaire qui dit "0 points"
    data = struct.pack('<L', 0)
    points = serializer.point_set_from_bytes(data)

    # La liste doit etre vide
    assert len(points) == 0

def test_fichier_coupe_court():
    """Si le fichier est trop petit meme pour le header."""
    # Juste 2 octets au lieu de 4
    assert serializer.point_set_from_bytes(b'\x00\x01') == []

def test_point_coupe_en_deux():
    """Important pour le coverage.

    On dit qu'il y a 1 point.
    Mais on ne donne que la moitié des données (4 octets au lieu de 8).
    Cela teste le 'if len(chunk) < 8' dans la boucle.
    """
    # Header : 1 point
    header = struct.pack('<L', 1)
    # Body : Un float (4 octets)
    body_incomplet = struct.pack('<f', 10.5)

    data = header + body_incomplet

    # La fonction doit voir que le point est incomplet et ne pas l'ajouter
    points = serializer.point_set_from_bytes(data)
    assert points == []

def test_ecriture_format():
    """Vérifie que la sortie binaire des triangles respecte le format."""
    points = [(0,0), (1,0), (0,1)]
    triangles = [(0, 1, 2)]

    result = serializer.triangles_to_bytes(points, triangles)

    # Calcul de la taille attendue :
    # Header points :
    # (4) + 3 points * 8 (24) + Header triangles (4) + 1 triangle * 12 (12)
    # Total = 44 octets
    assert len(result) == 44

    # On verifie manuellement que le header des triangles est bon
    # Il commence à l'octet 28 (4 + 24)
    tri_header = result[28:32]
    num_tri = struct.unpack('<L', tri_header)[0]
    assert num_tri == 1
