import json
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from datetime import datetime
from model.geoguessrs import Geoguessr

geoguessr_api = Blueprint("geoguessr_api", __name__, 
                         url_prefix='/api/geoguessr')

api = Api(geoguessr_api)

class GeoguessrAPI:
    class GeoguessrCR(Resource):
        def post(self):
            body = request.get_json()

            username = body.get('username')
            if username is None or len(username) <= 0:
                return {'message': 'username missing'}, 210

            # Change later to exclude negative scores
            score = body.get('score')
            if score is None or int(score) <= 0:
                return {'message': 'Score does not exist, is missing, or is invalid'}, 210

            game_datetime = body.get('game_datetime')

            uo = Geoguessr(
                username=username,
                score=score)

            
            if game_datetime is not None:
                try:
                    uo.dos = datetime.strptime(game_datetime, '%m-%d-%Y').date()
                except ValueError:
                    return {'message': 'Invalid date format. Must be mm-dd-yyyy'}, 210

            user = uo.create()
            if user:
                return jsonify(user.make_dict())
            return {'message': 'Failed to create user'}, 210

        def get(self):
            geoguessrs = Geoguessr.query.all()
            json_ready = [user.make_dict() for user in geoguessrs]
            return jsonify(json_ready)


    api.add_resource(GeoguessrCR, '/')
