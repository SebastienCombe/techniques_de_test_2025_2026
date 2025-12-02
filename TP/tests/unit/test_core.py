from src.core import triangulate

def test_triangulate_simple_triangle():
    """3 points non alignés doivent former 1 triangle."""
    points = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    triangles = triangulate(points)
    
    assert len(triangles) == 1
    # Le triangle doit référencer les indices 0, 1, 2
    t = triangles[0]
    assert set(t) == {0, 1, 2}

def test_triangulate_square():
    """4 points en carré doivent former 2 triangles."""
    points = [(0,0), (1,0), (1,1), (0,1)]
    triangles = triangulate(points)
    
    assert len(triangles) == 2