#!/bin/bash

PROJECT_DIR="$(dirname "$(dirname "$(dirname "$0")")")"
cd "$PROJECT_DIR"

# Run Django shell command to delete inactive customers
deleted_count=$(echo "
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer

one_year_ago = timezone.now() - timedelta(days=365)
inactive_customers = Customer.objects.filter(
    orders__isnull=True, created_at__lt=one_year_ago
) | Customer.objects.filter(
    orders__date__lt=one_year_ago
)

count = inactive_customers.count()
inactive_customers.delete()
print(count)
" | python3 manage.py shell 2>/dev/null)

# Log the result with timestamp
echo \"$(date '+%Y-%m-%d %H:%M:%S') - Deleted $deleted_count inactive customers\" >> /tmp/customer_cleanup_log.txt
