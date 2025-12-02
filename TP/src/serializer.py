import struct

def point_set_from_bytes(data: bytes) -> list[tuple[float, float]]:
    """Désérialise un PointSet binaire en liste de points (x, y)."""
    raise NotImplementedError("TODO")

def triangles_to_bytes(points: list[tuple[float, float]], triangles: list[tuple[int, int, int]]) -> bytes:
    """Sérialise les points et les indices de triangles en format binaire."""
    raise NotImplementedError("TODO")