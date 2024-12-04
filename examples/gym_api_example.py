from datetime import datetime, timedelta
from decimal import Decimal
from multiprocessing.pool import AsyncResult
from typing import cast, List

from evo_client.api.gym_api import GymApi
from evo_client.models.gym_model import (
    NewSale,
    PaymentMethod,
    CardData,
    GymKnowledgeBase,
    Sale,
    OverdueMember,
    Receivable,
)

# Initialize the API client
gym_api = GymApi()

# Example 1: Get gym knowledge base
print("\n=== Getting Gym Knowledge Base ===")
gym_kb_result = gym_api.get_gym_knowledge_base()
if isinstance(gym_kb_result, GymKnowledgeBase):  # Synchronous result
    gym_kb = gym_kb_result
else:  # Async result
    gym_kb = cast(GymKnowledgeBase, gym_kb_result.get())

print(f"Gym Name: {gym_kb.name}")
print(f"Number of Plans: {len(gym_kb.plans)}")
print(f"Number of Activities: {len(gym_kb.activities)}")

# Example 2: Get available plans
print("\n=== Available Plans ===")
for plan in gym_kb.plans:
    print(f"Plan: {plan.name}")
    print(f"Price: ${plan.price}")
    print(f"Features: {', '.join(plan.features)}")
    print("---")

# Example 3: Get activities and schedules
print("\n=== Activities ===")
for activity in gym_kb.activities:
    print(f"Activity: {activity.name}")
    print(f"Instructor: {activity.instructor}")
    print(f"Max Capacity: {activity.max_capacity}")
    print("---")

# Example 4: Create a new sale
print("\n=== Creating a New Sale ===")
new_sale = NewSale(
    idBranch=1,  # Replace with actual branch ID
    idMember=100,  # Replace with actual member ID
    idService=1,  # Replace with actual service ID
    serviceValue=Decimal("99.99"),
    payment_method=PaymentMethod.CREDIT_CARD,
    totalInstallments=1,
    cardData=CardData(
        cardNumber="4111111111111111",
        holderName="John Doe",
        expirationMonth=12,
        expirationYear=2025,
        securityCode="123",
    ),
)

try:
    sale_result = gym_api.create_sale(new_sale)
    if isinstance(sale_result, AsyncResult):  # Async result
        sale_result = cast(Sale, sale_result.get())
    print(f"Sale created successfully! Sale ID: {sale_result.id}")
except Exception as e:
    print(f"Error creating sale: {str(e)}")

# Example 5: Get sales history
print("\n=== Recent Sales ===")
start_date = datetime.now() - timedelta(days=30)  # Last 30 days
sales_result = gym_api.get_sales(
    date_sale_start=start_date,
    date_sale_end=datetime.now(),
    take=5,  # Limit to 5 results
)

if isinstance(sales_result, AsyncResult):  # Async result
    sales = cast(List[Sale], sales_result.get())
else:
    sales = sales_result

for sale in sales:
    print(f"Sale ID: {sale.id}")
    print(f"Member ID: {sale.idMember}")
    print(f"Amount: ${sale.serviceValue}")
    print(f"Date: {sale.createdAt}")
    print("---")

# Example 6: Get overdue members
print("\n=== Overdue Members ===")
overdue_result = gym_api.get_overdue_members(
    min_days_overdue=30
)  # More than 30 days overdue

if isinstance(overdue_result, AsyncResult):  # Async result
    overdue_members = cast(List[OverdueMember], overdue_result.get())
else:
    overdue_members = overdue_result

for member in overdue_members:
    print(f"Member: {member.name}")
    print(f"Total Overdue: ${member.total_overdue}")
    print(f"Overdue Since: {member.overdue_since}")
    if member.last_payment_date:
        print(f"Last Payment: {member.last_payment_date}")
    print("---")

# Example 7: Get receivables
print("\n=== Recent Receivables ===")
receivables_result = gym_api.get_receivables(
    start_date=datetime.now() - timedelta(days=30), end_date=datetime.now()
)

if isinstance(receivables_result, AsyncResult):  # Async result
    receivables = cast(List[Receivable], receivables_result.get())
else:
    receivables = receivables_result

for receivable in receivables:
    print(f"Description: {receivable.description}")
    print(f"Amount: ${receivable.amount}")
    print(f"Due Date: {receivable.due_date}")
    print(f"Status: {receivable.status}")
    print("---")
