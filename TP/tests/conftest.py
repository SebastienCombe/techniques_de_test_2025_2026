import pytest
import struct
from src.app import create_app

@pytest.fixture
def client():
    """Fixture pour initialiser le client de test Flask.

    C'est executé avant chaque test qui demande l'argument 'client'.
    """
    app = create_app()
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

@pytest.fixture
def sample_point_set_bytes():
    """Fixture qui genere un binaire valide avec 3 points.

    Ça evite de devoir recoder le struct.pack dans chaque fichier de test.
    """
    nb_points = 3
    # Un triangle rectangle simple
    p1 = (0.0, 0.0)
    p2 = (1.0, 0.0)
    p3 = (0.0, 1.0)

    # 1. Le header (nombre de points)
    data = struct.pack('<L', nb_points)

    # 2. Les points (float x, float y)
    # On ajoute les octets les uns à la suite des autres
    data = data + struct.pack('<ff', p1[0], p1[1])
    data = data + struct.pack('<ff', p2[0], p2[1])
    data = data + struct.pack('<ff', p3[0], p3[1])

    return data
