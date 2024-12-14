import pytest
import requests

BASE_URL = 'https://todo-reminder-app-6343.onrender.com'  # Deployed URL

# Test: Add a task
def test_add_task():
    response = requests.post(f'{BASE_URL}/tasks', json={
        'title': 'Test Task',
        'description': 'This is a test task'
    })
    assert response.status_code == 201
    assert 'id' in response.json()
    assert response.json()['title'] == 'Test Task'


# Test: Get all tasks
def test_get_tasks():
    # Add a task first
    requests.post(f'{BASE_URL}/tasks', json={'title': 'Test Task 1', 'description': 'First test task'})
    requests.post(f'{BASE_URL}/tasks', json={'title': 'Test Task 2', 'description': 'Second test task'})
    response = requests.get(f'{BASE_URL}/tasks')
    assert response.status_code == 200
    assert len(response.json()) >= 2  # Ensure we have at least 2 tasks


# Test: Update a task
def test_update_task(client):
    # Add a task first and get the task ID dynamically
    response = client.post('/tasks', json={'title': 'Old Title', 'description': 'Old description'})
    task_id = response.json['id']  # Get the dynamically assigned task ID
    
    # Now use this task ID for the update
    response = client.put(f'/tasks/{task_id}', json={'title': 'Updated Title', 'description': 'Updated description'})
    assert response.status_code == 200
    assert response.json['title'] == 'Updated Title'


# Test: Delete a task
def test_delete_task(client):
    # Add a task first and get the task ID dynamically
    response = client.post('/tasks', json={'title': 'Delete Task', 'description': 'Task to delete'})
    task_id = response.json['id']  # Get the dynamically assigned task ID
    
    # Now use this task ID for the delete request
    response = client.delete(f'/tasks/{task_id}')
    assert response.status_code == 200
    assert response.json['message'] == 'Task deleted successfully'



# Test: Delete all tasks
def test_delete_all_tasks():
    # Add tasks
    requests.post(f'{BASE_URL}/tasks', json={'title': 'Task 1', 'description': 'First task'})
    requests.post(f'{BASE_URL}/tasks', json={'title': 'Task 2', 'description': 'Second task'})
    response = requests.delete(f'{BASE_URL}/tasks')
    assert response.status_code == 200
    assert response.json()['message'] == 'All tasks deleted successfully'


# Test: Get tasks when no tasks exist
def test_get_tasks_empty():
    response = requests.get(f'{BASE_URL}/tasks')
    assert response.status_code == 200
    assert len(response.json()) == 0


# Test: Invalid task ID on PUT request (Update)
def test_update_task_invalid_id():
    response = requests.put(f'{BASE_URL}/tasks/999', json={'title': 'New Title', 'description': 'New description'})
    assert response.status_code == 404
    assert 'error' in response.json()
    assert response.json()['error'] == 'Task not found'


# Test: Invalid task ID on DELETE request
def test_delete_task_invalid_id():
    response = requests.delete(f'{BASE_URL}/tasks/999')
    assert response.status_code == 404
    assert 'error' in response.json()
    assert response.json()['error'] == 'Task not found'


# Test: Invalid JSON data when adding a task
def test_add_task_invalid_json():
    response = requests.post(f'{BASE_URL}/tasks', json={'title': '', 'description': ''})  # Invalid empty task data
    assert response.status_code == 400
    assert 'error' in response.json()
    assert response.json()['error'] == 'Title is required'


# Test: Attempt to delete a task that has already been deleted
def test_delete_task_already_deleted():
    # First, create the task
    response = requests.post(f'{BASE_URL}/tasks', json={'title': 'Task to Delete', 'description': 'Delete this task'})
    task_id = response.json()['id']  # Dynamically get the task ID
    
    # Delete the task
    response = requests.delete(f'{BASE_URL}/tasks/{task_id}')
    assert response.status_code == 200  # First delete, should succeed
    assert response.json()['message'] == 'Task deleted successfully'
    
    # Attempt to delete the same task again, should return 404
    response = requests.delete(f'{BASE_URL}/tasks/{task_id}')  # Trying to delete it again
    assert response.status_code == 404  # Task no longer exists, so 404 is expected
    assert 'error' in response.json()
    assert response.json()['error'] == 'Task not found'
