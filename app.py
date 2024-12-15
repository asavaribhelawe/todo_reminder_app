from flask import Flask, jsonify, render_template
from models import db
from config import Config
import routes
from routes import add_task, get_tasks, update_task, delete_task, delete_all_tasks

# Initialize the app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database
db.init_app(app)

# Define routes
@app.route('/')
def home():
    return render_template('index.html')  # Renders the frontend HTML page

app.add_url_rule('/tasks', 'add_task', routes.add_task, methods=['POST'])
app.add_url_rule('/tasks', 'get_tasks', routes.get_tasks, methods=['GET'])
app.add_url_rule('/tasks/<int:id>', 'update_task', routes.update_task, methods=['PUT'])
app.add_url_rule('/tasks/<int:id>', 'delete_task', routes.delete_task, methods=['DELETE'])
app.add_url_rule('/tasks', 'delete_all_tasks', routes.delete_all_tasks, methods=['DELETE'])

if __name__ == '__main__':
    # Create the database tables if they don't exist
    with app.app_context():
        db.create_all()

    # Run the application
    app.run(debug=True)
