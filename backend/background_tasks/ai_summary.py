from ..tasks import celery


@celery.task
def generate_ai_summary(data):
    print(f"Processing {data}")
