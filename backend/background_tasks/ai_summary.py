from tasks import celery_instance


@celery_instance.task
def generate_ai_summary(data):
    print(f"Processing {data}")
