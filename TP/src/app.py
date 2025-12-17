from flask import Flask, Response
import os
import requests
# On importe les modules entiers, c'est plus clair
import src.serializer as serializer
import src.core as core

def create_app(test_config=None):
    """Fonction factory pour créer l'app Flask."""
    app = Flask(__name__)

    # Récupération de l'URL du manager dans les variables d'env
    app.config['PSM_URL'] = os.environ.get('PSM_URL', 'http://point-set-manager:8080')

    @app.route('/triangulation/<id>', methods=['GET'])
    def calcul_triangulation(id):
        # Appel au service PointSetManager
        # On construit l'URL avec des +
        base_url = app.config['PSM_URL']
        target_url = base_url + "/point_sets/" + id

        try:
            r = requests.get(target_url)
        except Exception as e:
            # Si on arrive pas a joindre le serveur
            print("Erreur connexion PSM: " + str(e))
            return "PointSetManager unavailable", 502

        # Gestion des erreurs HTTP du manager
        if r.status_code == 404:
            return "PointSet not found", 404

        if r.status_code != 200:
            return "Error from PointSetManager", 502

        # Traitement des données
        # Etape A : Deserialisation
        try:
            points = serializer.point_set_from_bytes(r.content)
        except Exception:
            # Si le format binaire n'est pas bon
            return "Invalid PointSet data", 500

        # Etape B : Calcul de triangulation
        try:
            triangles = core.triangulate(points)
        except Exception:
            # Si l'algo plante
            return "Triangulation failed", 500

        # Etape C : Serialisation du resultat
        resultat_binaire = serializer.triangles_to_bytes(points, triangles)

        # On renvoie la reponse avec le bon type MIME
        return Response(resultat_binaire,
        mimetype='application/octet-stream',
        status=200)

    return app

if __name__ == '__main__':   # pragma: no cover
    app = create_app()       # pragma: no cover
    app.run(host='0.0.0.0', port=5000) # pragma: no cover
