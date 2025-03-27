
import asyncio
import json
import logging

import certifi
from django.core.management.base import BaseCommand
from redis import Redis

logger = logging.getLogger(__name__)
import certifi
from redis import Redis

redis_client = Redis.from_url(
    'rediss://red-cvhse65ds78s73egu3h0:JX9MPosnkjEG77hvdk6TY0apEXLusKCH@oregon-keyvalue.render.com:6379',
    ssl_cert_reqs='required',
    ssl_ca_certs=certifi.where()
)




semaphore = asyncio.Semaphore(10)  # Limit to 10 concurrent tasks

class Command(BaseCommand):
    help = "Process campaigns from Redis queue"

    def add_arguments(self, parser):
        parser.add_argument('api_key', type=str)
        parser.add_argument('queue_name', type=str)

    async def process_queue(self, api_key, queue_name):
        while True:
            try:
                campaign_json = redis_client.rpop(queue_name)
                if campaign_json:
                    campaign = json.loads(campaign_json)
                    async with semaphore:
                        await self.trigger_call(campaign, api_key)
            except Exception as e:
                logger.error(f"Error processing campaign: {e}")

    async def trigger_call(self, campaign, api_key):
        logger.info(f"Triggering call for campaign: {campaign['name']} with API key: {api_key}")
        await asyncio.sleep(1)  # Simulate processing

    def handle(self, *args, **options):
        api_key = options['api_key']
        queue_name = options['queue_name']
        asyncio.run(self.process_queue(api_key, queue_name))