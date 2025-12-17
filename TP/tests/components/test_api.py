import requests_mock
import requests
import src.core
import src.serializer

# URL qu'on va utiliser partout
PSM_URL = "http://point-set-manager:8080"

def test_nominal_case(client, sample_point_set_bytes, monkeypatch):
    """Test du cas normal."""
    id_test = "123"

    # On remplace la vraie fonction de triangulation par une fausse
    # pour ne pas tester l'algo ici, juste l'API.
    def faux_calcul(points):
        return [(0, 1, 2)]

    # On applique le patch sur le module core
    monkeypatch.setattr(src.core, "triangulate", faux_calcul)

    # On utilise requests_mock pour simuler le serveur en face
    with requests_mock.Mocker() as m:
        # On dit : si on appelle cette URL, renvoie ces données binaires
        target = PSM_URL + "/point_sets/" + id_test
        m.get(target, content=sample_point_set_bytes, status_code=200)

        # On appelle notre API
        response = client.get("/triangulation/" + id_test)

        # On verifie qu'on a bien un code 200 et des données
        assert response.status_code == 200
        assert len(response.data) > 0

def test_psm_not_found(client, monkeypatch):
    """Test si le PointSetManager ne trouve pas l'ID (404)."""
    id_test = "999"

    # On patche l'algo pour renvoyer vide au cas ou
    monkeypatch.setattr(src.core, "triangulate", lambda p: [])

    with requests_mock.Mocker() as m:
        target = PSM_URL + "/point_sets/" + id_test
        m.get(target, status_code=404)

        response = client.get("/triangulation/" + id_test)
        # On accepte 404 ou 502 selon comment c'est géré
        assert response.status_code in [404, 502]

def test_psm_connection_error(client):
    """Test si le PointSetManager est éteint (Erreur reseau)."""
    id_test = "123"

    with requests_mock.Mocker() as m:
        # On simule une erreur de connexion
        target = PSM_URL + "/point_sets/" + id_test
        m.get(target, exc=requests.exceptions.ConnectionError)

        response = client.get("/triangulation/" + id_test)
        # On doit recevoir une erreur 502 (Bad Gateway)
        assert response.status_code == 502

def test_bad_data_received(client):
    """Test si le PointSetManager renvoie n'importe quoi."""
    id_test = "123"

    with requests_mock.Mocker() as m:
        target = PSM_URL + "/point_sets/" + id_test
        # On renvoie du texte au lieu du binaire attendu
        m.get(target, content=b'MAUVAIS_FORMAT', status_code=200)

        response = client.get("/triangulation/" + id_test)
        # Ça doit planter ou renvoyer une erreur
        assert response.status_code in [200, 500]

def test_algo_bug(client, sample_point_set_bytes, monkeypatch):
    """Test si l'algo de triangulation plante (Exception)."""
    id_test = "123"

    # On definit une fonction qui plante volontairement
    def algo_qui_plante(points):
        raise ValueError("Bug dans l'algo !")

    monkeypatch.setattr(src.core, "triangulate", algo_qui_plante)

    with requests_mock.Mocker() as m:
        target = PSM_URL + "/point_sets/" + id_test
        m.get(target, content=sample_point_set_bytes, status_code=200)

        response = client.get("/triangulation/" + id_test)
        # Erreur interne du serveur
        assert response.status_code == 500

def test_psm_server_error(client):
    """Test si le PointSetManager renvoie une erreur 500."""
    id_test = "error"

    with requests_mock.Mocker() as m:
        target = PSM_URL + "/point_sets/" + id_test
        m.get(target, status_code=500)

        response = client.get("/triangulation/" + id_test)
        assert response.status_code == 502
        # On verifie qu'on a bien notre message d'erreur
        assert b"Error from PointSetManager" in response.data

def test_serializer_crash(client, sample_point_set_bytes, monkeypatch):
    """Test critique : Si le serializer plante completement."""
    id_test = "crash"

    # On remplace la fonction de deserialisation par une qui lance une exception
    def serializer_casse(data):
        raise Exception("Gros plantage")

    monkeypatch.setattr(src.serializer, "point_set_from_bytes", serializer_casse)

    with requests_mock.Mocker() as m:
        target = PSM_URL + "/point_sets/" + id_test
        m.get(target, content=sample_point_set_bytes, status_code=200)

        response = client.get("/triangulation/" + id_test)
        assert response.status_code == 500
        assert b"Invalid PointSet data" in response.data
