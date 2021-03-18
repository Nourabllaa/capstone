
# reused and refactored code from trivia project 
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import * 




class CastingAgencyTestCase(unittest.TestCase):
    # This class represents the Casting Agency test case

    def setUp(self):
       # Define test variables and initialize app.
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "agency"
        self.database_path = 'postgresql://noura.@localhost:5432/agency'
        setup_db(self.app, self.database_path)

        self.new_actor = {
            'name': 'Noura  ',
            'age': 22,
            'gender': 'Female'
        }
        self.new_movie = {
            'title': ' A day of a Life ',
            'release': '2020-5-14'

        }
        self.edit_movie = {
            'title': ' doooooooooonnnnnnneeee ',
            'release': '2020-5-14'
        }
        self.new_actor = {
            'name': 'Saja  ',
            'age': 22,
            'gender': 'Female'
        }


        # retrive users tokens from .setuu.sh file and create headers 
        self.casting_assistant_token = {
            "Authorization": "Bearer " + os.getenv('CASTING_ASSISTANT_TOKEN') }
        self.casting_director_token = {
            "Authorization": "Bearer " + os.getenv('CASTING_DIRECTOR_TOKEN') }
        self.executive_producer_token = {
            "Authorization": "Bearer " + os.getenv('EXEUTIVE_PRODUCER_TOKEN') }


    '''  
    binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all() 
    '''
    # Executed after reach test 
    def tearDown(self):
        pass

    '''
    requirement:
    One test for success behavior of each endpoint 
    One test for error behavior of each endpoint
    At least two tests of RBAC for each role 
    '''

    '''
    Get Actor

    - all actors
    success behavior : test_get_all_actors
    error behavior:

    -specific actor
    success behavior : get_specific_actor
    error behavior: test_404_get_specific_actor
    

    '''
    

    def test_get_all_actors(self):
        res = self.client().get('/actors', headers=self.casting_assistant_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
    
    '''
    def test_404_get_all_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404) 
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')
        '''

    def test_get_specific_actor(self):
        # database must contain actor with id=1 
        res = self.client().get('/actors/94', headers=self.casting_assistant_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
    
    def test_404_get_specific_actor(self):
        res = self.client().get('/actors/200', headers=self.casting_assistant_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404) 
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')


   
    '''
    Get Movies

    - all movies
    success behavior : test_get_all_movies
    error behavior:

    -specific movie
    success behavior : get_specific_movie
    error behavior: test_404_get_specific_movie
    '''
    

    def test_get_all_movies(self):
        res = self.client().get('/movies', headers=self.casting_assistant_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
    
    '''
    def test_404_get_all_movies(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404) 
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')
        '''

    def test_get_specific_movie(self):
        # database must contain movie with id=1 
        res = self.client().get('/movies/91', headers=self.casting_assistant_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
    
    def test_404_get_specific_movie(self):
        res = self.client().get('/movies/100', headers=self.casting_assistant_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404) 
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')
    

    '''
    Post Actor 
    success behavior : test_post_actor
    error behavior: test_404_post_actor
    '''


    def test_post_actor(self):
        results = self.client().post('/actors',  headers=self.casting_director_token ,json=self.new_actor) 
        data = json.loads(results.data)

        self.assertEqual(results.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue('actor')
    
    def test_422_post_actor(self):
        results = self.client().post('/actors',json={'release': '2020-5-14'}, headers=self.casting_director_token)
        data = json.loads(results.data)

        self.assertEqual(results.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')
    

    '''
    Post Movie 
    success behavior : test_post_movie
    error behavior: test_404_post_movie
    '''


    def test_post_movie(self):
        results = self.client().post('/movies', json=self.new_movie, headers=self.executive_producer_token)
        data = json.loads(results.data)
        self.assertEqual(results.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue('movie')
    
    def test_404_post_movie(self):
        results = self.client().post('/movies',json={}, headers=self.executive_producer_token)
        data = json.loads(results.data)

        self.assertEqual(results.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')
   


    '''
    Delete Actor 
    success behavior : test_delete_actor
    error behavior: test_403_auth_forbidden_delete_actor
    '''


    def test_delete_actor(self):
        res = self.client().delete('/actors/130', headers=self.executive_producer_token)
        data = json.loads(res.data)
        actor = Actor.query.filter(id==130).one_or_none()
        self.assertEqual(res.status_code, 200) 
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 130)
    


    def test_403_auth_forbidden_delete_actor(self):
        res = self.client().delete('/actors/200', headers=self.casting_assistant_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403) 
        self.assertEqual(data['success'], False)
        
    
    

    '''
    Delete Movie 
    success behavior : test_delete_movie
    error behavior: test_403_auth_forbidden_delete_movie
    '''


    def test_delete_movie(self):
        res = self.client().delete('/movies/127', headers=self.executive_producer_token)
        data = json.loads(res.data)
        movie = Movie.query.filter(Movie.id == 127).one_or_none()
        self.assertEqual(res.status_code, 200) 
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 127)
    

    def test_403_auth_forbidden_delete_movie(self):
        res = self.client().delete('/movies/91', headers=self.casting_assistant_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

  
 # test code 
    def test_patch_movie(self):
        myMovie = Movie(title='capstone', release='2020-1-1')
        myMovie.create()
        movie_id = myMovie.id
        edit_movie = {
            'title': 'capstone2',
            'release': '2021-1-1'
        }
        response = self.client().patch(f'/movies/{movie_id }', headers=self.executive_producer_token, json=edit_movie)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        # need to add 
        
        
    def test_404_patch_movie(self):
        edit_movie = {
            'title': 'capstone2',
            'release': '2021-1-1'
        }
        response = self.client().patch('/movies/2000',headers=self.executive_producer_token, json=edit_movie)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        # need to add 
        

    def test_patch_actor(self):
        act = Actor(name='ahmad',age=50,gender='male')
        act.create()
        actor_id = act.id

        edit_actor1 = {
            'name': 'name2',
            'age': 34,
            'gender': 'Female'
        }
        response = self.client().patch(f'/actors/{actor_id }',headers=self.executive_producer_token, json=edit_actor1)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

        
    def test_404_patch_actor(self):
        edit_actor = {
            'name': 'Noura ',
            'age': 21,
            'gender': 'Female'
        }
        response = self.client().patch('/actors/2000',headers=self.executive_producer_token, json=edit_actor)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        # need to add 

    

   
    
  
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()