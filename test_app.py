import pytest
import os
from app import app,init_db

#Define the name for our temporary test database
TEST_DB='test.db'

@pytest.fixture
def client():
    #1. Set up a temporary db for the tests
    #This tells the app use our temporary db file
    original_db_file=app.config.get('DATABASE','notes.db') #Store original for safety
    app.config['DATABSE']=TEST_DB
    app.config['TESTING']=True

    #Point the global DB_FILE in app.py to our test database
    #This is a key step to make sure the appp uses the right DB during tests
    import app as main_app
    main_app.DB_FILE=TEST_DB

    #2.Initialise db with our table
    with app.app_context():
        init_db()
    #3 Yield test client for the test functions to use
    with app.test_client() as client:
        yield client
    
    #4 Teardown: clean up by removing db file after the test
    os.remove(TEST_DB)

    #Restore original settings
    main_app.DB_FILE=original_db_file
    app.config['DATABASE']=original_db_file


def test_health_check(client):
    """Test the health check endpoint."""
    response=client.get('/health') 
    assert response.status_code == 200
    assert response.data == b'OK'

def test_get_notes_initially_empty(client):
    """Test that GET /notes returns an empty list initially."""
    response=client.get('/notes') 
    assert response.status_code == 200
    assert response.json == []