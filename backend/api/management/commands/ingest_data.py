from django.core.management.base import BaseCommand
from api.tasks import ingest_customer_data, ingest_loan_data

class Command(BaseCommand):
    help = 'Ingest customer and loan data'

    def handle(self, *args, **options):
        self.stdout.write("Starting ingestion...")
        # For simplicity in this assignment, calling them synchronously or via delay if worker is up.
        # If worker is not up, delay() simply queues it.
        # But for initial setup, we might want to run them synchronously to ensure data is there.
        # However, assignment says "using background workers".
        # So I will use .delay()
        
        task1 = ingest_customer_data.delay()
        self.stdout.write(f"Triggered customer ingestion task: {task1.id}")
        
        task2 = ingest_loan_data.delay()
        self.stdout.write(f"Triggered loan ingestion task: {task2.id}")
