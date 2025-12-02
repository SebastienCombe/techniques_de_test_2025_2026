import pytest
import requests_mock
import src.core

def test_get_triangulation_nominal(client, sample_point_set_bytes, monkeypatch):
    """
    Scénario complet avec ISOLATION :
    1. Le client appelle GET /triangulation/123
    2. Le PointSetManager est MOCKÉ (via requests_mock) -> On simule la donnée entrante.
    3. L'algo de triangulation est PATCHÉ (via monkeypatch) -> On simule le calcul.
    """
    point_set_id = "123"
    psm_url = "http://point-set-manager:8080"

    # On crée une fausse fonction de triangulation
    def mock_triangulate(points):
        # On renvoie un triangle "bidon" mais valide pour la suite du code
        return [(0, 1, 2)]

    # On applique le patch
    monkeypatch.setattr(src.core, "triangulate", mock_triangulate)

    with requests_mock.Mocker() as m:
        # On mocke la réponse du PointSetManager (Comme avant)
        m.get(f"{psm_url}/point_sets/{point_set_id}", 
              content=sample_point_set_bytes, 
              status_code=200)
        
        # Appel à l'API
        response = client.get(f"/triangulation/{point_set_id}")
        
        # Vérifications
        assert response.status_code == 200
        assert len(response.data) > 0

def test_get_triangulation_psm_error(client, monkeypatch):
    """
    Si le PointSetManager renvoie 404, on doit renvoyer une erreur.
    Ici, monkeypatch est optionnel car on s'attend à échouer AVANT le calcul,
    mais c'est une bonne pratique de l'ajouter pour garantir l'isolation.
    """
    point_set_id = "999"
    psm_url = "http://point-set-manager:8080"
    
    monkeypatch.setattr(src.core, "triangulate", lambda p: [])

    with requests_mock.Mocker() as m:
        m.get(f"{psm_url}/point_sets/{point_set_id}", status_code=404)
        
        response = client.get(f"/triangulation/{point_set_id}")
        assert response.status_code in [404, 502]