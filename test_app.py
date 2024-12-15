import pytest
import requests

BASE_URL = 'https://todo-reminder-app-6343.onrender.com'  # Deployed URL

# Test: Add a task
def test_add_task():
    response = requests.post(f'{BASE_URL}/tasks', json={'title': 'Test Task', 'description': 'This is a test task'})
    
    if response.status_code != 201:
        print(f"Error: {response.status_code} - {response.text}")
    
    assert response.status_code == 201
    try:
        data = response.json()
        assert 'id' in data
        assert data['title'] == 'Test Task'
    except requests.exceptions.JSONDecodeError:
        print(f"Response content is not JSON: {response.text}")
        assert False  # Fail the test if the response is not JSON



# Test: Get all tasks
def test_get_tasks():
    # Add a task first
    requests.post(f'{BASE_URL}/tasks', json={'title': 'Test Task 1', 'description': 'First test task'})
    requests.post(f'{BASE_URL}/tasks', json={'title': 'Test Task 2', 'description': 'Second test task'})
    response = requests.get(f'{BASE_URL}/tasks')
    assert response.status_code == 200
    assert len(response.json()) >= 2  


# Test: Update a task
def test_update_task():
    # Add a task first and get the task ID dynamically
    response = requests.post(f'{BASE_URL}/tasks', json={'title': 'Old Title', 'description': 'Old description'})
    task_id = response.json()['id']
    response = requests.put(f'{BASE_URL}/tasks/{task_id}', json={'title': 'Updated Title', 'description': 'Updated description'})
    assert response.status_code == 200
    assert response.json()['title'] == 'Updated Title'


# Test: Delete a task
def test_delete_task():
    # Add a task first and get the task ID dynamically
    response = requests.post(f'{BASE_URL}/tasks', json={'title': 'Delete Task', 'description': 'Task to delete'})
    task_id = response.json()['id']
    response = requests.delete(f'{BASE_URL}/tasks/{task_id}')
    assert response.status_code == 200
    assert response.json()['message'] == 'Task deleted successfully'


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
    response = requests.post(f'{BASE_URL}/tasks', json={'title': '', 'description': ''})
    assert response.status_code == 400
    assert 'error' in response.json()
    assert response.json()['error'] == 'Title is required'


# Test: Attempt to delete a task that has already been deleted
def test_delete_task_already_deleted():
    response = requests.post(f'{BASE_URL}/tasks', json={'title': 'Task to Delete', 'description': 'Delete this task'})
    task_id = response.json()['id']
    response = requests.delete(f'{BASE_URL}/tasks/{task_id}')
    assert response.status_code == 200
    assert response.json()['message'] == 'Task deleted successfully'
    response = requests.delete(f'{BASE_URL}/tasks/{task_id}')  # Trying to delete it again
    assert response.status_code == 404
    assert 'error' in response.json()
    assert response.json()['error'] == 'Task not found'
