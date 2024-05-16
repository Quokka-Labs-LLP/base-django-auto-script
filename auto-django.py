import subprocess
import sys
import os
import shutil
from scripts.celery_script import create_celery
from scripts.exceptions_script import create_exceptions
from scripts.utils_script import create_utils
from scripts.settings_script import create_settings
from scripts.logger_middleware_script import create_logger_middleware
from scripts.project_init_script import create_project_init
from scripts.create_env_script import create_env


def settingup_django(project_name, database, celery, redis):
    script_path = os.path.realpath(__file__)
    base_path = script_path.replace("auto-django.py", project_name)

    env_path = os.path.join(base_path, f'{project_name}/.env')
    create_env(env_path, celery, redis, database)

    init_path = os.path.join(base_path, f'{project_name}/__init__.py')
    create_project_init(init_path, celery)

    settings_path = os.path.join(base_path, f'{project_name}/settings.py')
    create_settings(settings_path, project_name, database, celery, redis)
    exception_path = os.path.join(base_path, f"{project_name}/exception.py")
    exception_handler_path = os.path.join(base_path, f"{project_name}/exception_handler.py")
    create_exceptions(exception_path, exception_handler_path)

    if celery.lower() == 'y':
        celery_path = os.path.join(base_path, f'{project_name}/celery.py')
        create_celery(celery_path, project_name)

    utils_path = os.path.join(base_path, "utils")
    os.makedirs(utils_path)
    create_utils(utils_path, project_name)

    logger_path = os.path.join(base_path, f"{project_name}/middlewares")
    os.makedirs(logger_path)
    create_logger_middleware(os.path.join(logger_path, "LoggerMiddleware.py"))


def create_django_project(project_name):
    venv_path = os.path.realpath(__file__)
    venv_path = venv_path.replace("auto-django.py", "venv").replace("\\", "/")
    cmd = f'/bin/bash -c "source {venv_path}/bin/activate && django-admin startproject {project_name}"' if sys.platform != 'win32' else f'"{venv_path}/Scripts/activate" && django-admin startproject {project_name}'
    subprocess.run(cmd, shell=True, check=True)


def install_package_in_venv(database, celery="", redis=""):
    # Replace 'path/to/your/venv' with the path to your virtual environment
    venv_path = os.path.realpath(__file__)
    venv_path = venv_path.replace("auto-django.py", "venv")

    # Activate the virtual environment
    activate_script = os.path.join(venv_path, 'Scripts' if sys.platform == 'win32' else 'bin', 'activate')
    activate_cmd = f'{activate_script}'
    activate_cmd = activate_cmd.replace('\\', '/')

    # Install the package using pip inside the virtual environment
    database_package = ""
    if database == 1:
        database_package = 'mysqlclient'
    elif database == 2:
        database_package = 'psycopg2' if sys.platform == 'win32' else 'psycopg2-binary'
    elif database == 3:
        database_package = 'djongo'

    celery_package = ""
    if celery.lower() == 'y':
        celery_package = 'celery redis'

    redis_package = ""
    if redis.lower() == 'y':
        redis_package = 'redis django-redis'

    install_cmd = f'pip install django djangorestframework {database_package} {celery_package} {redis_package} django-environ loguru django-cors-headers flake8 pytz'
    cmd = f'/bin/bash -c "source {activate_cmd} && {install_cmd}"' if sys.platform != 'win32' else f'{activate_cmd} && {install_cmd}'
    #os.chmod(activate_script, 0o755)
    # Run the activation command and then install the package
    subprocess.run(cmd, shell=True, check=True)


def create_python_venv(python_path):
    subprocess.run([python_path, '-m', 'venv', 'venv'])


def create_requirements_file(project_name):
    script_path = os.path.realpath(__file__)
    venv_path = script_path.replace("auto-django.py", "venv").replace("\\", "/")
    django_path = script_path.replace("auto-django.py", project_name).replace("\\", "/")
    cmd = f'/bin/bash -c "source {venv_path}/bin/activate && pip freeze > {django_path}/requirements.txt"' if sys.platform != 'win32' else f'"{venv_path}/Scripts/activate" && pip freeze > "{django_path}/requirements.txt"'
    subprocess.run(cmd, shell=True, check=True)


def cleanup():
    base_file = os.path.realpath(__file__)
    script_path = base_file.replace("auto-django.py", "scripts")
    shutil.rmtree(script_path)
    os.remove(base_file)


if __name__ == "__main__":
    python_path = input("Enter python path for a specific Python version or press Enter for the default environment: ").strip()
    while python_path:
        if not os.path.exists(python_path):
            python_path = input("please enter a existing python path or press 'enter' for default python: ").strip()
            if python_path == "":
                break
            continue
        else:
            if python_path.split("\\")[-1] != "python.exe":
                python_path = input("Given path is not a valid python path, path should contain 'python.exe' at end.").strip()
            else:
                break
    if python_path == "":
        python_path = 'python3'
        if sys.platform == 'win32': 
            python_path = 'python'
    database = ""
    while isinstance(database, str):
        database = input("""Enter a number to select a DB:
                        0 or enter for default
                        1 for mysql
                        2 for postgres
                        3 for mongodb\n""").strip()
        try:
            if not database:
                database = '0'
            database = int(database)
            if database not in range(0, 4):
                print("please select a valid number(0 to 3)")
                database = ""
        except ValueError:
            print("Enter a valid integer or just press 'ENTER' for default DB configuration")

    while True:
        project_name = input("Enter Django project name: ")
        if not project_name.isidentifier():
            print("""\nProject name must start with a letter or an underscore. Following characters can be letters, digits, or underscores. It cannot start with a digit. Also, empty string is not allowed.""")    
        else:
            break
    celery = input("Do you want celery, 'Y' for yes: ")
    redis = input("want redis cache setup? 'Y' for yes: ")
    create_python_venv(python_path)
    install_package_in_venv(database, celery, redis)
    create_django_project(project_name)
    create_requirements_file(project_name)
    settingup_django(project_name, database, celery, redis)
    cleanup()
