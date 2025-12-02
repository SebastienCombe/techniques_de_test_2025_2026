from flask import Flask, request, Response
import os
from src.serializer import point_set_from_bytes, triangles_to_bytes
import src.core as core
import requests

def create_app(test_config=None):
    app = Flask(__name__)
    
    # URL du PointSetManager (configurable via env)
    app.config['PSM_URL'] = os.environ.get('PSM_URL', 'http://point-set-manager:8080')

    @app.route('/triangulation/<point_set_id>', methods=['GET'])
    def get_triangulation(point_set_id):
        # 1. Récupérer le PointSet auprès du PointSetManager
        psm_url = app.config['PSM_URL']
        try:
            resp = requests.get(f"{psm_url}/point_sets/{point_set_id}")
        except requests.exceptions.RequestException:
            return "PointSetManager unavailable", 502

        if resp.status_code == 404:
            return "PointSet not found", 404
        
        if resp.status_code != 200:
            return "Error from PointSetManager", 502

        # 2. Désérialiser les points (Binaire -> Liste)
        try:
            points = point_set_from_bytes(resp.content)
        except Exception:
            return "Invalid PointSet data", 500

        # 3. Calculer la triangulation (Liste -> Liste)
        try:
            triangles = core.triangulate(points)
        except Exception:
            return "Triangulation failed", 500

        # 4. Sérialiser le résultat (Liste -> Binaire)
        result_bytes = triangles_to_bytes(points, triangles)

        return Response(result_bytes, mimetype='application/octet-stream', status=200)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)