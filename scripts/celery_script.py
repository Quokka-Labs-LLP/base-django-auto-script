def create_celery(path, project_name):
    celery_content = """import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_base_architecture.settings')

app = Celery('django_base_architecture')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')"""   # noqa
    celery_content = celery_content.replace("django_base_architecture", project_name)
    with open(path, 'w') as file:
        file.write(celery_content)
          
