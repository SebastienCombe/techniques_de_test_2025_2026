import pytest
import struct
from src.serializer import point_set_from_bytes, triangles_to_bytes

def test_point_set_from_bytes_nominal(sample_point_set_bytes):
    """Test nominal : on doit récupérer 3 points corrects."""
    points = point_set_from_bytes(sample_point_set_bytes)
    assert len(points) == 3
    assert points[0] == (0.0, 0.0)
    assert points[2] == (0.0, 1.0)

def test_point_set_from_bytes_empty():
    """Test limite : 0 points."""
    data = struct.pack('<L', 0)
    points = point_set_from_bytes(data)
    assert len(points) == 0

def test_triangles_to_bytes_format():
    """Vérifie que la sortie binaire des triangles respecte le format."""
    points = [(0,0), (1,0), (0,1)]
    triangles = [(0, 1, 2)]
    
    result = triangles_to_bytes(points, triangles)
    
    assert len(result) == 44
    
    tri_header = result[28:32]
    num_tri = struct.unpack('<L', tri_header)[0]
    assert num_tri == 1