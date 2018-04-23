from celery import shared_task


@shared_task(bind=True)
def people_search(self, search_id):
    pass
