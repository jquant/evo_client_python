Employees
=========

The Employees API provides functionality to manage employees in the EVO system. It supports CRUD operations (Create, Read, Update, Delete) for employee records with both synchronous and asynchronous execution modes.

.. module:: evo_client.api.employees_api

API Reference
------------

.. autoclass:: EmployeesApi
    :members:
    :undoc-members:
    :special-members: __init__

    .. method:: get_employees(employee_id=None, name=None, email=None, take=None, skip=None, async_req=False)
        
        Retrieve a list of employees with optional filtering.

        :param employee_id: Optional ID to find a specific employee
        :type employee_id: int, optional
        :param name: Filter employees by name (partial match supported)
        :type name: str, optional
        :param email: Filter employees by email address
        :type email: str, optional
        :param take: Maximum number of records to return
        :type take: int, optional
        :param skip: Number of records to skip for pagination
        :type skip: int, optional
        :param async_req: If True, returns an AsyncResult object
        :type async_req: bool, optional
        :return: List[:class:`~evo_client.models.funcionarios_resumo_api_view_model.FuncionariosResumoApiViewModel`] or AsyncResult
        :raises: :exc:`ValueError` if pagination parameters are invalid
        :raises: :exc:`ApiException` if the API call fails

    .. method:: create_employee(employee, async_req=False)

        Create a new employee record.

        :param employee: Employee data for creation
        :type employee: :class:`~evo_client.models.employee_api_integracao_atualizacao_view_model.EmployeeApiIntegracaoAtualizacaoViewModel`
        :param async_req: If True, returns an AsyncResult object
        :type async_req: bool, optional
        :return: None or AsyncResult
        :raises: :exc:`ValueError` if required fields are missing
        :raises: :exc:`ApiException` if the API call fails

    .. method:: update_employee(employee, async_req=False)

        Update an existing employee's information.

        :param employee: Updated employee data
        :type employee: :class:`~evo_client.models.employee_api_integracao_view_model.EmployeeApiIntegracaoViewModel`
        :param async_req: If True, returns an AsyncResult object
        :type async_req: bool, optional
        :return: None or AsyncResult
        :raises: :exc:`ValueError` if required fields are missing
        :raises: :exc:`ApiException` if employee not found or update fails

    .. method:: delete_employee(employee_id, async_req=False)

        Delete an employee record.

        :param employee_id: ID of the employee to delete
        :type employee_id: int
        :param async_req: If True, returns an AsyncResult object
        :type async_req: bool, optional
        :return: None or AsyncResult
        :raises: :exc:`ValueError` if employee_id is invalid
        :raises: :exc:`ApiException` if employee not found or deletion fails

Models
------

.. module:: evo_client.models.funcionarios_resumo_api_view_model

.. autoclass:: FuncionariosResumoApiViewModel
    :members:
    :undoc-members:

    Model for employee summary information returned by list operations.

    :ivar id_employee: Unique identifier for the employee
    :vartype id_employee: int, optional
    :ivar name: Employee's full name
    :vartype name: str, optional
    :ivar email: Employee's email address
    :vartype email: str, optional
    :ivar telephone: Contact phone number
    :vartype telephone: str, optional
    :ivar job_position: Employee's role or position
    :vartype job_position: str, optional
    :ivar status: Active status (True if active)
    :vartype status: bool, optional
    :ivar photo_url: URL to employee's photo
    :vartype photo_url: str, optional

.. module:: evo_client.models.employee_api_integracao_view_model

.. autoclass:: EmployeeApiIntegracaoViewModel
    :members:
    :undoc-members:

    Model for updating existing employee records.

    :ivar name: Employee's first name
    :vartype name: str, optional
    :ivar last_name: Employee's last name
    :vartype last_name: str, optional
    :ivar document: Primary identification document (e.g., CPF)
    :vartype document: str, optional
    :ivar document_id: Secondary identification (e.g., RG)
    :vartype document_id: str, optional
    :ivar cellphone: Mobile phone number
    :vartype cellphone: str, optional
    :ivar email: Email address (must be unique)
    :vartype email: str, optional
    :ivar gender: Gender identifier ('M' or 'F')
    :vartype gender: str, optional
    :ivar birthday: Date of birth
    :vartype birthday: datetime, optional
    :ivar country: Country of residence
    :vartype country: str, optional
    :ivar address: Street address
    :vartype address: str, optional
    :ivar state: State/province
    :vartype state: str, optional
    :ivar city: City
    :vartype city: str, optional
    :ivar passport: Passport number
    :vartype passport: str, optional
    :ivar zip_code: Postal code
    :vartype zip_code: str, optional
    :ivar complement: Address complement
    :vartype complement: str, optional
    :ivar neighborhood: Neighborhood
    :vartype neighborhood: str, optional
    :ivar number: Street number
    :vartype number: str, optional
    :ivar active: Account status
    :vartype active: bool, optional

.. module:: evo_client.models.employee_api_integracao_atualizacao_view_model

.. autoclass:: EmployeeApiIntegracaoAtualizacaoViewModel
    :members:
    :undoc-members:

    Model for creating new employee records. Extends :class:`~evo_client.models.employee_api_integracao_view_model.EmployeeApiIntegracaoViewModel` with additional fields.

    :ivar id_employee: Unique identifier (auto-generated)
    :vartype id_employee: int, optional

Examples
--------

The following examples demonstrate common operations with proper error handling.

Retrieving Employees
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from evo_client.api import EmployeesApi
    from evo_client.exceptions import ApiException

    try:
        # Initialize the API client
        employees_api = EmployeesApi()

        # Get all employees with pagination
        employees = employees_api.get_employees(
            take=10,  # Limit to 10 results
            skip=0    # Start from the first result
        )

        # Filter employees by name
        filtered_employees = employees_api.get_employees(
            name="John",
            take=10
        )

        for employee in filtered_employees:
            print(f"Found employee: {employee.name} ({employee.email})")

    except ValueError as e:
        print(f"Invalid parameter: {e}")
    except ApiException as e:
        print(f"API error: {e}")

Creating an Employee
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from evo_client.api import EmployeesApi
    from evo_client.models import EmployeeApiIntegracaoAtualizacaoViewModel
    from evo_client.exceptions import ApiException
    from datetime import datetime

    try:
        # Initialize the API client
        employees_api = EmployeesApi()

        # Create employee data
        new_employee = EmployeeApiIntegracaoAtualizacaoViewModel(
            name="John",
            last_name="Doe",
            email="john.doe@example.com",
            cellphone="1234567890",
            document="123.456.789-00",  # CPF format
            birthday=datetime(1990, 1, 1),
            gender="M",
            address="123 Main St",
            city="New York",
            state="NY",
            country="USA",
            zip_code="10001",
            active=True
        )

        # Create the employee
        employees_api.create_employee(new_employee)
        print("Employee created successfully")

    except ValueError as e:
        print(f"Invalid employee data: {e}")
    except ApiException as e:
        if e.status == 409:
            print("Employee with this email already exists")
        else:
            print(f"API error: {e}")

Updating an Employee
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from evo_client.api import EmployeesApi
    from evo_client.models import EmployeeApiIntegracaoViewModel
    from evo_client.exceptions import ApiException

    try:
        # Initialize the API client
        employees_api = EmployeesApi()

        # Update employee data
        updated_employee = EmployeeApiIntegracaoViewModel(
            name="John",
            last_name="Doe",
            email="john.new@example.com",
            cellphone="0987654321",
            active=True
        )

        # Update the employee
        employees_api.update_employee(updated_employee)
        print("Employee updated successfully")

    except ValueError as e:
        print(f"Invalid employee data: {e}")
    except ApiException as e:
        if e.status == 404:
            print("Employee not found")
        elif e.status == 409:
            print("Email address already in use")
        else:
            print(f"API error: {e}")

Deleting an Employee
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from evo_client.api import EmployeesApi
    from evo_client.exceptions import ApiException

    try:
        # Initialize the API client
        employees_api = EmployeesApi()

        # Delete employee by ID
        employees_api.delete_employee(employee_id=123)
        print("Employee deleted successfully")

    except ValueError as e:
        print(f"Invalid employee ID: {e}")
    except ApiException as e:
        if e.status == 404:
            print("Employee not found")
        else:
            print(f"API error: {e}")

Async Operations
~~~~~~~~~~~~~~

All operations support asynchronous execution for better performance in concurrent scenarios:

.. code-block:: python

    from evo_client.api import EmployeesApi
    from evo_client.exceptions import ApiException

    try:
        # Initialize API client
        employees_api = EmployeesApi()

        # Start async operation
        async_result = employees_api.create_employee(new_employee, async_req=True)

        # Do other work while operation is in progress
        print("Processing...")

        try:
            # Wait for and get the result
            result = async_result.get()
            print("Employee created successfully")
        except ApiException as e:
            print(f"Async operation failed: {e}")

    except ValueError as e:
        print(f"Invalid employee data: {e}")

Authentication
-------------

This API requires Basic Authentication:

- **Username**: Your gym's DNS
- **Password**: Your Secret Key

All requests must include these credentials in the Basic Authentication header.
