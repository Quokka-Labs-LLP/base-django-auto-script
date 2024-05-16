def create_project_init(path, celery):
    init_content = """from environ import Env


Env.read_env()
env = Env()
"""
    if celery.lower() == 'y':
        init_content += """__all__ = ("celery_app", "env")"""

    with open(path, 'w') as file:
        file.write(init_content)
