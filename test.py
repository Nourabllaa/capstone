# reused and refactored code from trivia project 
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import * 

casting_assistant_token='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkE3QlE1eFRTMlZTVXVfR1ZNU0RhUiJ9.eyJpc3MiOiJodHRwczovL2Rldi1vaG91ZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAxNjk4YTYzYjJkMzQwMDY5ZDEyOWY3IiwiYXVkIjoibW92aWUiLCJpYXQiOjE2MTQ3OTY0OTgsImV4cCI6MTYxNDgwMzY5OCwiYXpwIjoiek1LVEl6Zm4ySHV2c1BpVVJDaURGV2w5WHhtaWNYYWQiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.nkSbAaAR-fnsrz5dLukl_uWnf8XCCml6k7ERiDmCPeTE_qJH6RW2QPEv5V2zGHMTNVAE8j9ntAOnOkoqnb8JcqMJw2ypiNMZwpYAmjeruK1a6m6OkcWd-UDhF7ZazvV8IbQXSz06ZyID6KB4OnyyIrV6PBSGiQa3LlrEIflFL7NKwqnL3P-PFazlfKvDr0rnxgQWFKTO8a6IsMZhCaKUYVEL1lPuhpvJ2d9pR8xCkavxgIM1-x4LXBTqOAwYhafQLiieJFNpASSOWSg4-DPMSvindGs56xMgXwhUyKYUhycsg_yNBhrgV-i0tQCuMnePFKiZ-ALn6a1YGqRsin8Gng'
casting_director_token='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkE3QlE1eFRTMlZTVXVfR1ZNU0RhUiJ9.eyJpc3MiOiJodHRwczovL2Rldi1vaG91ZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAwNTVkZDcxMzA5ZTMwMDY5YzRhYmFjIiwiYXVkIjoibW92aWUiLCJpYXQiOjE2MTQ3OTY2ODcsImV4cCI6MTYxNDgwMzg4NywiYXpwIjoiek1LVEl6Zm4ySHV2c1BpVVJDaURGV2w5WHhtaWNYYWQiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.WMgHCNMtQXi5GI11sgReP3KzMmF3vYTPsckA7HQmtq4QwKpeNOZzrm5v8PAIms2lGj5n5V_pYWxwtKYyjxOUtUB4eJ5Faf2TWALbsoKJ7dC4y81L7v4uQ1baSliP-3cRbGMMMfugA2qcschxAMdZ8dtz4dQIthT1cdQqYinW7MoQeX2TrQeOfxl0qLOEnxx0caijpKHx-ubPCTTrzW65cqr0dq88MDFhwj6NrSeBR-G5gjFSfB4_mr-zXk7j0jvJV5BGACJ9MKXfERJXofFjWaYsATbl9l4KJ9rkl_-PGpBY-0oWymF3WUI6g1ocFqicu63pb8LlDKhEYlH-yTvQyQ'
casting_producer_token='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InI3cERfUk9kZS1jOXEzX3FRVVFJVSJ9.eyJpc3MiOiJodHRwczovL2F1dGgtZXgudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwMTg1NjVmODA0ZGVjMDA2YTg0YmNjMyIsImF1ZCI6ImNhc3RpbmdfYWdlbmN5IiwiaWF0IjoxNjE1ODA3MTc3LCJleHAiOjE2MTU4OTM1NzcsImF6cCI6IkcxVlpZZlpPRGh1d3dITU1IR0JOUGZjY0lpZlJJN25FIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.KY2xx5Uky4yecEloQuYCqOiYW1jjY8ZiSCtaRnYSFyeq8Z0-VOIqkrFrkN6sHwzHIb23mY9AnycBrJ1VD-tKFlPdnHWt14MscNV1xMmEjC3SvTd_xlYj_iBdbMqfT_5CTu_DqpFZXlxfGuKtkCEHOeqOd0DbTkumavRCRTdc5RcazLpcmH8YqrFz_z08mRZ2LpGvRT6ZeAo2bKqdc5jS8O6bSbpSNDg6YTKD_BzcYeWKgC_pcLTDPRS8KFKjyF6T90DB7uVkjU-1M2wyUQPFw_4zD0jol5KImzlcKVRq5j4tHqozKzPGNioMpbShtbANemuHIQdVBmwABXvb10KEaQ'
class AppTest(unittest.TestCase):
    """Setup test suite for the routes"""
    def setUp(self):
        """Setup application """
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "sample_heroku"
        self.database_path = 'postgresql://noura.@localhost:5432/sample_heroku'
        setup_db(self.app, self.database_path)
    def tearDown(self):
        """Executed after each test"""
        pass
    def test_create_new_actor(self):
        new_actor = {
            "name": "ohoud",
            "age": 25,
            "gender": "female"
        }
        res = self.client().post(
            '/actors',
            headers={"Authorization": "Bearer " + casting_producer_token},
            json=new_actor
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
# Make the tests executable
if __name__ == "__main__":
        unittest.main()
