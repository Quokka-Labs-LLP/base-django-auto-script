def create_env(path, celery, redis, database):
    env_content = """SECRET_KEY="django-insecure-50@nnbdvqyd+8f&5-rks^al40elqfm@)l@sv^ye6am2h&=9^a2"

DEBUG='True'

ALLOWED_HOSTS='*'

CORS_ALLOW_ALL_ORIGINS='True'
CORS_ALLOWED_ORIGINS='http://localhost:8000'
"""
    if celery.lower() == 'y':
        env_content = env_content + '\nCELERY_BROKER_URL="redis://127.0.0.1:6379/2"\n'

    if redis.lower() == 'y':
        env_content = env_content + '\nCACHE_BROKER_URL="redis://127.0.0.1:6379/1"\n'

    if database == 1:
        env_content = env_content + """\nDB_USER='root'
DB_HOST='localhost'
DB_PASSWORD='null'
DB_NAME='rql'
DB_PORT='3306'\n
"""

    elif database == 2:
        env_content = env_content + """\nDB_USER='root'
DB_HOST='localhost'
DB_PASSWORD='null'
DB_NAME='rql'
DB_PORT='5432'\n
"""

    elif database == 3:
        env_content = env_content + """\nDB_NAME='rql'
DB_HOST='localhost'
DB_PORT='27017'\n
"""

    with open(path, 'w') as file:
        file.write(env_content)
