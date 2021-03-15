import os
import json
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_cors import CORS
from models import *
from auth import *


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  app.secret_key = os.getenv('SECRET')
  setup_db(app)
  CORS(app)


  @app.after_request
  def after_request(response):
      response.headers.add(
          'Access-Control-Allow-Headers',
          'Content-Type,Authorization,true')
      response.headers.add(
          'Access-Control-Allow-Methods',
          'GET,PATCH,POST,DELETE,OPTIONS')
      return response
  '''

  Routes 


  ''' 
  @app.route('/')
  def homepage():
    return jsonify({
      'Message': 'Welcome to Casting Agency'
        })


  '''
    GET/Actors 
      return all actors
      it require the 'get:actors' permission
      returns status code 200 and json {"success": True, "actors": actors_list}
  '''

  @app.route('/actors', methods=['GET'])
  @requires_auth('get:actors')
  def get_actors_detail(payload):
      try:
          actors = Actor.query.order_by(Actor.id).all()

          actors_list = []
          for actor in actors:
              actors_list.append(actor.format())

          return jsonify({
              'success': True,
              'actors': actors_list,
          }), 200
      except:
          abort(404)
  
  '''
  GET/Movies 
    return all movies
    it require the 'get:movies' permission
    returns status code 200 and json {"success": True, "movie": movies_list}
  '''
  @app.route('/movies', methods=['GET'])
  @requires_auth('get:movies')
  def get_movies_detail(payload):
      try:
          movies = Movie.query.order_by(Movie.id).all()

          movies_list = []
          for movie in movies:
              movies_list.append(movie.format())

          return jsonify({
              'success': True,
              'movies': movies_list,
          }), 200
      except:
          abort(404)

  '''
   GET/Movie
    return movie with movie_id
    it require the 'get:movies' permission
    returns status code 200 and json {"success": True, "movie": movie}
'''


  @app.route('/movies/<int:movie_id>', methods=['GET'])
  @requires_auth('get:movies')
  def get_movies(payload, movie_id):

      if not movie_id:
          abort(400)

      movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

      if not movie:
          abort(404)

      return jsonify({
          'success': True,
          'movie': [movie.format()]
      }), 200


  '''
    GET/actor 
      return actor with actor_id
      requires the 'get:actors' permission
      returns status code 200 and json {"success": True, "actor": actor}
'''

  @app.route('/actors/<int:actor_id>', methods=['GET'])
  @requires_auth('get:actors')
  def get_actor(payload, actor_id):

        if not actor_id:
            abort(400)

        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if not actor:
            abort(404)

        return jsonify({
            'success': True,
            'actor': [actor.format()]
        }), 200
  '''
    PATCH/actors/<actor_id> 
      requires the 'patch:actors' permission
      update actor row with id actor_id
      returns status code 200 and json {"success": True, "actor": actor}
      return jsonify({'success': True,"updated": myActor.id,
      "actor": [myActor.format()]})
'''


  @app.route('/actors/<int:actor_id>/', methods=['PATCH'])
  @requires_auth('patch:actors')
  def update_actor(payload, id):

    body=request.get_json()
   
    try:
       myActor = Actor.query.filter(Actor.id == id).one_or_none()
       if myActor is None:
          abort(404)
       if not body:
          abort(400)

       title = body.get('name', myActor.name)
       age = body.get('age', myActor.age)
       gender = body.get('gender', myActor.gender)
       
       # get updated values from body
       # Update with new values
       if 'name' in body :
          myActor.name = name
       if 'age' in body:
         myActor.age = age

       if 'gender' in body:
         myActor.gender = gender
       myActor.update()

      # return result 
       return jsonify({
         'success': True,
         'updated': myActor.id,
         'actor': myActor.format()
         }), 200
    except:
      abort(422)

   
    

  '''
      PATCH/movies/<movie_id>
        requires the 'patch:movies' permission
        update actor row with id movie_id
        returns status code 200 and json {"success": True, "movies": movies}
        return jsonify({'success': True,"updated": myActor.id,
        "actor": [myMovies.format()]})
'''

  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def update_movies(payload, movie_id):
    body=request.get_json()
   
    try:
       myMovie = Movie.query.filter(Movie.id == id).one_or_none()
       if myMovie is None:
          abort(404)
       if not body:
          abort(400)

       title = body.get('title', myMovie.title)
       release = body.get('release', myMovie.release)
    # get updated values from body
        # Update with new values
       if 'title' in body :
          myMovie.title = title
          #myMovie.title = body.get('title')

       if 'release' in body:
        myMovie.release = release
        #myMovie.release = body.get('release')
    
        myMovie.update()

        # return result 
        return jsonify({
            'success': True,
            'updated': myMovie.id,
            'movie': myMovie.format()
        }), 200
    except:
      abort(422)

    
 
  

  '''
    POST/actors
      create a new row in the movie table
      requires the 'post:actors' permission
      returns status code 200 and json {"success": True, "actor": id}
'''
  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def post_actor(payload):
      try:
        body = request.get_json()
        if(body is None):
          abort(404)

        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)
      
        new_actor = Actor(
          name=name,
          age=age,
          gender=gender
          )
        
        new_actor.create()

        return jsonify({
          'success': True,
          'actor': new_actor.id,
          }), 201
      except:
          abort(422)
          

  '''
    POST/movies
      create a new row in the movies table
      requires the 'post:movies' permission
      returns status code 200 and json {"success": True, "movie": id}
'''

  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def post_movies(payload):
      try:
        body = request.get_json()

        if(body is None):
          abort(404) 
        
        title= body.get('title', None)
        release = body.get('release', None)

        new_movie = Movie(title = title, release=release)
        new_movie.create()

        return jsonify({
          'success': True,
          'movie': new_movie.id,
          }), 201
      except:
          abort(422)
  

  '''
   DELETE /actors/<id>
    where <id> is the existing model id
    responds with a 404 error if <id> is not found
    deletes the corresponding row for <id>
    requires the 'delete:actors' permission
    returns status code 200 and json {"success": True, "delete": id }
'''


  @app.route('/actors/<int:id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(payload, id):
      try:
        myActor=Actor.query.filter(Actor.id==id).one_or_none()
        if myActor is None:
            abort(404)
        else:
          myActor.delete()
          return jsonify({
              'success': True,
              'delete': id,
          }), 200

      except:
          abort(422)


  '''
  DELETE /movies/<id>
    where <id> is the existing model id
    responds with a 404 error if <id> is not found
    deletes the corresponding row for <id>
    requires the 'delete:movies' permission
    returns status code 200 and json {"success": True, "delete": id }
  '''


  @app.route('/movies/<int:id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(payload, id):
    try:
      myMovie=Movie.query.filter(Movie.id==id).one_or_none()
      if myMovie is None:
        abort(404)
      else:
        myMovie.delete()
        return jsonify({
          'success': True ,
          'delete': id 
        }),200
    except:
      abort(422)
 


  '''

    Error Handlers

    '''

  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          'success': False,
          'error': 400,
          'message': 'Bad Request'
      }), 400
  
  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          'success': False,
          'error': 404,
          'message': 'Not Found'
      }), 404

  @app.errorhandler(422)
  def unprocesable_entity(error):
      return jsonify({
          'success': False,
          'error': 422,
          'message': 'Unprocessable Entity'
      }), 422

  @app.errorhandler(500)
  def internal_server_error(error):
      return jsonify({
          'success': False,
          'error': 500,
          'message': 'Internal Server Error'
      }), 500

  @app.errorhandler(AuthError)
  def authentification_failed(AuthError):
      return jsonify({
          "success": False,
          "error": AuthError.status_code,
          "message": AuthError.error['description']
      }), AuthError.status_code

  return app

app = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)