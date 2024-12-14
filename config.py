import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://todo_db_0js5_user:xzeCzmOpTM2O2YVCqHHcO9lT6agsHYWp@dpg-cteoqlt2ng1s738dfd30-a.oregon-postgres.render.com/todo_db_0js5'
