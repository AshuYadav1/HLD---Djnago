# myapp/tasks.py
from celery import shared_task
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def process_campaign(self, campaign_data):
    try:
        logger.info(f"Processing campaign: {campaign_data['name']}")
        # Add your processing logic here (e.g., external API call)
    except Exception as e:
        logger.error(f"Task failed: {e}")
        self.retry(exc=e, countdown=60)  # Retry after 60 seconds