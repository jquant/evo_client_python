Activities API
==============

The Activities API provides comprehensive functionality for managing and tracking fitness activities, classes, and schedules within your gym or fitness center. This API enables you to handle class bookings, attendance tracking, instructor assignments, and activity schedules.

Key Features
-----------

* Class and activity management
* Schedule creation and management
* Attendance tracking and reporting
* Instructor assignment and availability
* Capacity management and waitlists
* Real-time booking system
* Activity categories and filtering
* Support for recurring activities
* Comprehensive validation and error handling

Getting Started
-------------

Here are comprehensive examples demonstrating common use cases with the Activities API:

.. code-block:: python

    from evo_client.api import ActivitiesApi
    from evo_client.models import (
        ActivityViewModel,
        ScheduleViewModel,
        BookingViewModel,
        AttendanceViewModel
    )
    from evo_client.exceptions import ApiException
    from datetime import datetime, timedelta
    
    # Initialize the API client
    activities_api = ActivitiesApi()
    
    # Example 1: Managing class schedules
    def manage_class_schedule():
        try:
            # Create a new class schedule
            schedule = ScheduleViewModel(
                id_activity=123,  # Activity ID (e.g., "Yoga")
                id_instructor=456,
                start_time=datetime.now() + timedelta(days=1),
                duration_minutes=60,
                max_capacity=20,
                room_number="Studio A"
            )
            
            created_schedule = activities_api.create_schedule(schedule)
            print(f"Created schedule with ID: {created_schedule.id}")
            
            # Get upcoming classes
            tomorrow = datetime.now() + timedelta(days=1)
            next_week = tomorrow + timedelta(days=7)
            
            classes = activities_api.get_class_schedule(
                start_date=tomorrow,
                end_date=next_week,
                include_attendance=True
            )
            
            for class_ in classes:
                print(f"Class: {class_.activity_name}")
                print(f"Time: {class_.start_time}")
                print(f"Available spots: {class_.available_spots}")
                print("---")
                
        except ValueError as e:
            print(f"Invalid schedule data: {e}")
        except ApiException as e:
            print(f"API error: {e.status} - {e.reason}")
    
    # Example 2: Managing bookings and attendance
    def manage_bookings_attendance(member_id: int, schedule_id: int):
        try:
            # Book a class for a member
            booking = BookingViewModel(
                id_member=member_id,
                id_schedule=schedule_id
            )
            
            booking_result = activities_api.create_booking(booking)
            print(f"Booking confirmed: {booking_result.confirmation_code}")
            
            # Mark attendance
            attendance = AttendanceViewModel(
                id_booking=booking_result.id,
                check_in_time=datetime.now(),
                status="present"
            )
            
            activities_api.mark_attendance(attendance)
            print("Attendance marked successfully")
            
            # Get member's attendance history
            history = activities_api.get_member_attendance(
                id_member=member_id,
                start_date=datetime.now() - timedelta(days=30)
            )
            
            print("\nAttendance History:")
            for record in history:
                print(f"Class: {record.activity_name}")
                print(f"Date: {record.date}")
                print(f"Status: {record.status}")
                print("---")
            
        except ApiException as e:
            if e.status == 409:
                print("Class is full or booking conflict")
            else:
                print(f"Error managing booking: {e}")

Models
------

.. module:: evo_client.models

.. autoclass:: ActivityViewModel
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: ScheduleViewModel
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: BookingViewModel
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: AttendanceViewModel
   :members:
   :undoc-members:
   :show-inheritance:

API Methods
----------

.. module:: evo_client.api

.. autoclass:: ActivitiesApi
   :members:
   :undoc-members:
   :show-inheritance:

Usage Examples
-------------

Creating and Managing Schedules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from evo_client.api import ActivitiesApi
    from evo_client.models import ScheduleViewModel
    from evo_client.exceptions import ApiException
    from datetime import datetime, timedelta

    # Initialize the API client
    activities_api = ActivitiesApi()

    try:
        # Create a new class schedule
        schedule = ScheduleViewModel(
            id_activity=123,  # Required: Activity ID (e.g., "Yoga")
            id_instructor=456,  # Required: Instructor ID
            start_time=datetime.now() + timedelta(days=1),
            duration_minutes=60,
            max_capacity=20,
            room_number="Studio A"
        )
        
        created_schedule = activities_api.create_schedule(schedule)
        print(f"Created schedule with ID: {created_schedule.id}")
        
    except ValueError as e:
        print(f"Validation error: {e}")
    except ApiException as e:
        if e.status == 404:
            print("Activity or instructor not found")
        elif e.status == 409:
            print("Schedule conflicts with existing class")
        else:
            print(f"API error: {e.status} - {e.reason}")

Managing Bookings
~~~~~~~~~~~~~~~

.. code-block:: python

    from evo_client.models import BookingViewModel, AttendanceViewModel

    try:
        # Book a class for a member
        booking = BookingViewModel(
            id_member=789,  # Required: Member ID
            id_schedule=456  # Required: Schedule ID
        )
        
        booking_result = activities_api.create_booking(booking)
        print(f"Booking confirmed: {booking_result.confirmation_code}")
        
    except ApiException as e:
        if e.status == 400:
            print("Invalid booking request")
        elif e.status == 409:
            print("Class is full or booking already exists")
        else:
            print(f"API error: {e.status} - {e.reason}")

Error Handling
------------

The Activities API uses standard HTTP status codes and provides detailed error messages:

- 400: Invalid request (e.g., missing required fields, invalid data)
- 401: Authentication failed
- 403: Insufficient permissions
- 404: Resource not found
- 409: Conflict (e.g., duplicate booking, schedule conflict)
- 429: Too many requests
- 500: Internal server error

All errors are wrapped in :class:`~evo_client.exceptions.ApiException` with additional context.

API Reference
------------

.. autoclass:: evo_client.api.activities_api.ActivitiesApi
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__

Core Operations
-------------

Schedule Management
~~~~~~~~~~~~~~~~

.. automethod:: evo_client.api.activities_api.ActivitiesApi.create_schedule

**Required Parameters**

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Parameter
     - Type
     - Description
   * - ``id_activity``
     - int
     - Activity identifier
   * - ``id_instructor``
     - int
     - Instructor assigned to the class
   * - ``start_time``
     - datetime
     - Class start time
   * - ``duration_minutes``
     - int
     - Class duration in minutes
   * - ``max_capacity``
     - int
     - Maximum number of participants

**Optional Parameters**

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Parameter
     - Type
     - Description
   * - ``room_number``
     - str
     - Room or studio identifier
   * - ``notes``
     - str
     - Additional class information
   * - ``is_recurring``
     - bool
     - Whether the class repeats
   * - ``recurrence_pattern``
     - str
     - Pattern for recurring classes

**Returns**

Returns a :class:`~evo_client.models.ScheduleViewModel` containing:

- ``id``: Schedule identifier
- ``activity_info``: Activity details
- ``instructor_info``: Instructor information
- ``schedule_details``: Timing and capacity information

**Exceptions**

- ``ValueError``: When required parameters are missing or invalid
- ``ApiException``: When the API request fails
- ``ValidationError``: When schedule data fails validation

Booking Management
~~~~~~~~~~~~~~~

.. automethod:: evo_client.api.activities_api.ActivitiesApi.create_booking

**Parameters**

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Parameter
     - Type
     - Description
   * - ``id_member``
     - int
     - Member making the booking
   * - ``id_schedule``
     - int
     - Schedule identifier to book
   * - ``waitlist``
     - bool
     - Join waitlist if class is full (optional)

**Returns**

Returns :class:`~evo_client.models.BookingViewModel` containing:

- ``id``: Booking identifier
- ``confirmation_code``: Unique booking confirmation
- ``status``: Booking status (confirmed/waitlisted)
- ``position``: Waitlist position if applicable

**Example**

.. code-block:: python

    try:
        # Create a booking with waitlist option
        booking = activities_api.create_booking(
            id_member=123,
            id_schedule=456,
            waitlist=True
        )
        
        if booking.status == "confirmed":
            print(f"Booking confirmed: {booking.confirmation_code}")
        else:
            print(f"Added to waitlist, position: {booking.position}")
            
    except ApiException as e:
        if e.status == 409:
            print("Booking conflict: Already booked for this time")
        elif e.status == 404:
            print("Class not found or no longer available")
        else:
            print(f"Booking failed: {e}")

Attendance Tracking
~~~~~~~~~~~~~~~~

.. automethod:: evo_client.api.activities_api.ActivitiesApi.mark_attendance

**Parameters**

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Parameter
     - Type
     - Description
   * - ``id_booking``
     - int
     - Booking identifier
   * - ``check_in_time``
     - datetime
     - Time of check-in
   * - ``status``
     - str
     - Attendance status (present/absent/late)

**Returns**

Returns :class:`~evo_client.models.AttendanceViewModel` containing:

- ``id``: Attendance record identifier
- ``booking_info``: Associated booking details
- ``check_in_details``: Check-in time and status

**Example**

.. code-block:: python

    from datetime import datetime
    
    try:
        # Mark attendance for a booking
        attendance = activities_api.mark_attendance(
            id_booking=123,
            check_in_time=datetime.now(),
            status="present"
        )
        
        print(f"Attendance marked: {attendance.status}")
        print(f"Check-in time: {attendance.check_in_time}")
        
    except ApiException as e:
        if e.status == 404:
            print("Booking not found")
        elif e.status == 400:
            print("Invalid attendance status")
        else:
            print(f"Error marking attendance: {e}")

Advanced Features
---------------

Waitlist Management
~~~~~~~~~~~~~~~~

The Activities API provides comprehensive waitlist management features:

.. code-block:: python

    # Check waitlist position
    position = activities_api.get_waitlist_position(
        id_member=123,
        id_schedule=456
    )
    
    if position > 0:
        print(f"Current waitlist position: {position}")
    
    # Get waitlist notifications
    notifications = activities_api.get_waitlist_notifications(id_member=123)
    
    for notification in notifications:
        print(f"Spot available in: {notification.activity_name}")
        print(f"Time: {notification.schedule_time}")
        print(f"Expires: {notification.expiry_time}")

Capacity Management
~~~~~~~~~~~~~~~~

Monitor and manage class capacity:

.. code-block:: python

    # Get capacity information
    capacity = activities_api.get_schedule_capacity(id_schedule=456)
    
    print(f"Total capacity: {capacity.max_capacity}")
    print(f"Current bookings: {capacity.current_bookings}")
    print(f"Waitlist count: {capacity.waitlist_count}")
    
    # Check if space is available
    if capacity.has_available_spots:
        print(f"Spots available: {capacity.available_spots}")
    else:
        print("Class is full")
        if capacity.accepts_waitlist:
            print(f"Waitlist available: {capacity.waitlist_spots} spots")
