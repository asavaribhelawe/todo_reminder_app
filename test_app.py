import pytest
from app import app, db
from models import Task

@pytest.fixture(scope="module")  # This will run once per test module
def setup_database():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://todo_db_0js5_user:xzeCzmOpTM2O2YVCqHHcO9lT6agsHYWp@dpg-cteoqlt2ng1s738dfd30-a.oregon-postgres.render.com/todo_db_0js5'  # Using in-memory DB for tests
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()  # Create tables once at the start of the test suite
    yield db  # Provide the database to the tests
    with app.app_context():
        db.drop_all()  # Clean up the database after tests

@pytest.fixture
def client(setup_database):
    # Now we re-use the database setup from the fixture
    with app.test_client() as client:
        yield client


# Test: Add a task
def test_add_task(client):
    response = client.post('/tasks', json={
        'title': 'Test Task',
        'description': 'This is a test task'
    })
    assert response.status_code == 201
    assert 'id' in response.json
    assert response.json['title'] == 'Test Task'


# Test: Get all tasks
def test_get_tasks(client):
    # Add a task first
    client.post('/tasks', json={'title': 'Test Task 1', 'description': 'First test task'})
    client.post('/tasks', json={'title': 'Test Task 2', 'description': 'Second test task'})
    
    response = client.get('/tasks')
    assert response.status_code == 200
    assert len(response.json) >= 2  # Ensure we have at least 2 tasks


# Test: Update a task
def test_update_task(client):
    # Add a task first
    client.post('/tasks', json={'title': 'Old Title', 'description': 'Old description'})
    
    response = client.put('/tasks/1', json={'title': 'Updated Title', 'description': 'Updated description'})
    assert response.status_code == 200
    assert response.json['title'] == 'Updated Title'


# Test: Delete a task
def test_delete_task(client):
    # Add a task first
    client.post('/tasks', json={'title': 'Delete Task', 'description': 'Task to delete'})
    
    response = client.delete('/tasks/1')
    assert response.status_code == 200
    assert response.json['message'] == 'Task deleted successfully'


# Test: Delete all tasks
def test_delete_all_tasks(client):
    # Add tasks
    client.post('/tasks', json={'title': 'Task 1', 'description': 'First task'})
    client.post('/tasks', json={'title': 'Task 2', 'description': 'Second task'})
    
    response = client.delete('/tasks')
    assert response.status_code == 200
    assert response.json['message'] == 'All tasks deleted successfully'


# Test: Get tasks when no tasks exist
def test_get_tasks_empty(client):
    response = client.get('/tasks')
    assert response.status_code == 200
    assert len(response.json) == 0


# Test: Invalid task ID on PUT request (Update)
def test_update_task_invalid_id(client):
    response = client.put('/tasks/999', json={'title': 'New Title', 'description': 'New description'})
    assert response.status_code == 404
    assert 'error' in response.json
    assert response.json['error'] == 'Task not found'


# Test: Invalid task ID on DELETE request
def test_delete_task_invalid_id(client):
    response = client.delete('/tasks/999')
    assert response.status_code == 404
    assert 'error' in response.json
    assert response.json['error'] == 'Task not found'


# Test: Invalid JSON data when adding a task
def test_add_task_invalid_json(client):
    response = client.post('/tasks', json={'title': '', 'description': ''})  # Invalid empty task data
    assert response.status_code == 400
    assert 'error' in response.json
    assert response.json['error'] == 'Title is required'


# Test: Attempt to delete a task that has already been deleted
def test_delete_task_already_deleted(client):
    # First, create the task
    response = client.post('/tasks', json={'title': 'Task to Delete', 'description': 'Delete this task'})
    task_id = response.json['id']  # Dynamically get the task ID
    
    # Delete the task
    response = client.delete(f'/tasks/{task_id}')
    assert response.status_code == 200  # First delete, should succeed
    assert response.json['message'] == 'Task deleted successfully'
    
    # Attempt to delete the same task again, should return 404
    response = client.delete(f'/tasks/{task_id}')  # Trying to delete it again
    assert response.status_code == 404  # Task no longer exists, so 404 is expected
    assert 'error' in response.json
    assert response.json['error'] == 'Task not found'