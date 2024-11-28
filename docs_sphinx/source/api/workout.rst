Workout API
===========

The Workout API enables you to manage workout prescriptions and training programs for clients, prospects, and employees. This API provides functionality for creating, updating, and retrieving workout plans, as well as managing default workouts and linking them to users.

API Methods
----------

.. module:: evo_client.api

.. autoclass:: WorkoutApi
   :members:
   :undoc-members:
   :show-inheritance:

   .. automethod:: update_workout
      :noindex:

   .. automethod:: get_client_workouts
      :noindex:

   .. automethod:: get_workouts_by_month_year_professor
      :noindex:

   .. automethod:: get_default_workouts
      :noindex:

   .. automethod:: link_workout_to_client
      :noindex:

Usage Examples
-------------

Updating a Workout
~~~~~~~~~~~~~~~

.. code-block:: python

    from evo_client.api import WorkoutApi
    from evo_client.exceptions import ApiException
    from datetime import datetime, timedelta

    workout_api = WorkoutApi()

    try:
        # Update workout details
        workout_api.update_workout(
            workout_id=12345,
            workout_name="Advanced Strength Training",
            start_date=datetime.now(),
            expiration_date=datetime.now() + timedelta(weeks=12),
            observation="Focus on progressive overload",
            categories="strength,hypertrophy",
            restrictions="no_cardio",
            professor_id=789,
            total_weeks=12,
            weekly_frequency=4
        )
        
        print("Workout updated successfully")
        
    except ValueError as e:
        print(f"Invalid workout data: {e}")
    except ApiException as e:
        if e.status == 404:
            print("Workout not found")
        elif e.status == 403:
            print("Insufficient permissions to update workout")
        else:
            print(f"API error: {e.status} - {e.reason}")

Retrieving Client Workouts
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    try:
        # Get active workouts for a client
        workouts = workout_api.get_client_workouts(
            client_id=12345,
            inactive=False,
            deleted=False
        )
        
        for workout in workouts:
            print(f"Workout: {workout.get('workoutName')}")
            print(f"Start Date: {workout.get('startDate')}")
            print(f"Professor: {workout.get('professorName')}")
            print(f"Categories: {workout.get('categories')}")
            print("---")
            
    except ApiException as e:
        if e.status == 404:
            print("Client not found")
        else:
            print(f"API error: {e.status} - {e.reason}")

Managing Default Workouts
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    try:
        # Get default workouts for a specific trainer
        default_workouts = workout_api.get_default_workouts(
            employee_id=789  # Trainer's ID
        )
        
        # Link a default workout to a client
        if default_workouts:
            workout_api.link_workout_to_client(
                source_workout_id=default_workouts[0]['id'],
                prescription_employee_id=789,  # Trainer prescribing the workout
                client_id=12345,
                prescription_date=datetime.now()
            )
            print("Workout assigned to client")
            
    except ApiException as e:
        if e.status == 400:
            print("Invalid workout assignment")
        elif e.status == 404:
            print("Workout or client not found")
        else:
            print(f"API error: {e.status} - {e.reason}")

Retrieving Workouts by Professor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from datetime import datetime

    try:
        # Get workouts for a professor in current month
        current_date = datetime.now()
        workouts = workout_api.get_workouts_by_month_year_professor(
            professor_id=789,
            month=current_date.month,
            year=current_date.year,
            take=50  # Maximum records to return
        )
        
        for workout in workouts:
            print(f"Client: {workout.get('clientName')}")
            print(f"Workout: {workout.get('workoutName')}")
            print(f"Status: {workout.get('status')}")
            print("---")
            
    except ApiException as e:
        if e.status == 404:
            print("Professor not found")
        else:
            print(f"API error: {e.status} - {e.reason}")

Error Handling
------------

The Workout API uses standard HTTP status codes:

- 400: Invalid request (e.g., invalid workout data, invalid dates)
- 401: Authentication failed
- 403: Insufficient permissions to manage workouts
- 404: Resource not found (workout, client, professor)
- 409: Conflict (e.g., overlapping workout dates)
- 429: Too many requests
- 500: Internal server error

All errors are wrapped in :class:`~evo_client.exceptions.ApiException` with detailed error messages.

Pagination
---------

The API supports pagination for professor workouts through the following parameters:

- ``take``: Number of records to return (maximum 50)
- ``skip``: Number of records to skip

Example pagination:

.. code-block:: python

    # Get all workouts for a professor page by page
    page_size = 50
    current_page = 0
    
    while True:
        workouts = workout_api.get_workouts_by_month_year_professor(
            professor_id=789,
            take=page_size,
            skip=current_page * page_size
        )
        
        if not workouts:
            break
            
        # Process workouts
        for workout in workouts:
            print(f"Processing workout: {workout.get('workoutName')}")
            
        current_page += 1

Best Practices
------------

1. **Workout Management**:
   - Always set appropriate expiration dates for workouts
   - Include clear observations and restrictions
   - Use consistent categories for better organization
   - Consider weekly frequency when prescribing workouts

2. **Error Handling**:
   - Validate workout dates before updating
   - Handle workout not found scenarios gracefully
   - Implement proper error handling for all API calls

3. **Default Workouts**:
   - Create reusable default workouts for common scenarios
   - Use tags for better organization and searchability
   - Verify compatibility before linking to clients

4. **Security and Access Control**:
   - Verify professor permissions before workout operations
   - Keep audit trail of workout modifications
   - Respect client privacy when accessing workout data
