import pytest
import struct
from src.app import create_app

@pytest.fixture
def client():
    """Crée un client de test Flask."""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def sample_point_set_bytes():
    """
    Crée un binaire valide pour 3 points formant un triangle rectangle.
    Format: 
    - Count (4 bytes, unsigned long)
    - Point 1 (X, Y - 8 bytes)
    - Point 2 ...
    """
    count = 3
    p1 = (0.0, 0.0)
    p2 = (1.0, 0.0)
    p3 = (0.0, 1.0)
    
    header = struct.pack('<L', count)
    body = struct.pack('<ff', *p1) + struct.pack('<ff', *p2) + struct.pack('<ff', *p3)
    return header + body