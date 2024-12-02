from datetime import datetime
from multiprocessing.pool import AsyncResult
from typing import Any, Dict, List, Optional, Union, overload, Literal

from ..core.api_client import ApiClient


class WorkoutApi:
    """Workout API client for EVO API."""

    def __init__(self, api_client: Optional[ApiClient] = None):
        self.api_client = api_client or ApiClient()
        self.base_path = "/api/v1/workout"

    @overload
    def update_workout(
        self,
        workout_id: int,
        workout_name: Optional[str] = None,
        start_date: Optional[datetime] = None,
        expiration_date: Optional[datetime] = None,
        observation: Optional[str] = None,
        categories: Optional[str] = None,
        restrictions: Optional[str] = None,
        professor_id: Optional[int] = None,
        total_weeks: Optional[int] = None,
        weekly_frequency: Optional[int] = None,
        async_req: Literal[True] = True,
    ) -> AsyncResult[Any]: ...

    @overload
    def update_workout(
        self,
        workout_id: int,
        workout_name: Optional[str] = None,
        start_date: Optional[datetime] = None,
        expiration_date: Optional[datetime] = None,
        observation: Optional[str] = None,
        categories: Optional[str] = None,
        restrictions: Optional[str] = None,
        professor_id: Optional[int] = None,
        total_weeks: Optional[int] = None,
        weekly_frequency: Optional[int] = None,
        async_req: Literal[False] = False,
    ) -> Any: ...

    def update_workout(
        self,
        workout_id: int,
        workout_name: Optional[str] = None,
        start_date: Optional[datetime] = None,
        expiration_date: Optional[datetime] = None,
        observation: Optional[str] = None,
        categories: Optional[str] = None,
        restrictions: Optional[str] = None,
        professor_id: Optional[int] = None,
        total_weeks: Optional[int] = None,
        weekly_frequency: Optional[int] = None,
        async_req: bool = False,
    ) -> Union[Any, AsyncResult[Any]]:
        """
        Update a client's prescribed workout.

        Args:
            workout_id: The workout's ID to be changed
            workout_name: New name for the workout (empty to keep current)
            start_date: The workout's start date
            expiration_date: The workout's expiration date
            observation: Additional observations
            categories: Comma-separated categories (replaces existing)
            restrictions: Comma-separated restrictions (replaces existing)
            professor_id: ID of the professor who created the workout
            total_weeks: Total number of weeks for the workout
            weekly_frequency: Weekly frequency for the client
            async_req: Execute request asynchronously
        """
        params = {
            "idWorkout": workout_id,
            "workoutName": workout_name,
            "startDate": start_date,
            "expirationDate": expiration_date,
            "observation": observation,
            "categories": categories,
            "restrictions": restrictions,
            "idProfessor": professor_id,
            "totalWeeks": total_weeks,
            "weeklyFrequency": weekly_frequency,
        }

        return self.api_client.call_api(
            resource_path=self.base_path,
            method="PUT",
            query_params={k: v for k, v in params.items() if v is not None},
            auth_settings=["Basic"],
            async_req=async_req,
        )

    @overload
    def get_client_workouts(
        self,
        client_id: Optional[int] = None,
        prospect_id: Optional[int] = None,
        employee_id: Optional[int] = None,
        workout_id: Optional[int] = None,
        inactive: Optional[bool] = None,
        deleted: Optional[bool] = None,
        async_req: Literal[True] = True,
    ) -> AsyncResult[Any]: ...

    @overload
    def get_client_workouts(
        self,
        client_id: Optional[int] = None,
        prospect_id: Optional[int] = None,
        employee_id: Optional[int] = None,
        workout_id: Optional[int] = None,
        inactive: Optional[bool] = None,
        deleted: Optional[bool] = None,
        async_req: Literal[False] = False,
    ) -> Any: ...

    def get_client_workouts(
        self,
        client_id: Optional[int] = None,
        prospect_id: Optional[int] = None,
        employee_id: Optional[int] = None,
        workout_id: Optional[int] = None,
        inactive: Optional[bool] = None,
        deleted: Optional[bool] = None,
        async_req: bool = False,
    ) -> Union[Any, AsyncResult[Any]]:
        """
        Get workouts for a client, prospect or employee.

        Args:
            client_id: ID of the client
            prospect_id: ID of the prospect
            employee_id: ID of the employee
            workout_id: Specific workout ID to retrieve
            inactive: Include inactive workouts
            deleted: Include deleted workouts
            async_req: Execute request asynchronously
        """
        params = {
            "idClient": client_id,
            "idProspect": prospect_id,
            "idEmployee": employee_id,
            "idWorkout": workout_id,
            "inactive": inactive,
            "deleted": deleted,
        }

        return self.api_client.call_api(
            resource_path=f"{self.base_path}/default-client-workout",
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            auth_settings=["Basic"],
            async_req=async_req,
        )

    @overload
    def get_workouts_by_month_year_professor(
        self,
        professor_id: Optional[int] = None,
        month: Optional[int] = None,
        year: Optional[int] = None,
        skip: Optional[int] = None,
        take: Optional[int] = None,
        async_req: Literal[True] = True,
    ) -> AsyncResult[Any]: ...

    @overload
    def get_workouts_by_month_year_professor(
        self,
        professor_id: Optional[int] = None,
        month: Optional[int] = None,
        year: Optional[int] = None,
        skip: Optional[int] = None,
        take: Optional[int] = None,
        async_req: Literal[False] = False,
    ) -> Any: ...

    def get_workouts_by_month_year_professor(
        self,
        professor_id: Optional[int] = None,
        month: Optional[int] = None,
        year: Optional[int] = None,
        skip: Optional[int] = None,
        take: Optional[int] = None,
        async_req: bool = False,
    ) -> Union[Any, AsyncResult[Any]]:
        """
        Get workouts filtered by month, year and/or professor.

        Args:
            professor_id: The ID of the professor who created the workouts
            month: Month to filter workouts
            year: Year to filter workouts
            skip: Number of records to skip
            take: Number of records to return (max 50)
            async_req: Execute request asynchronously
        """
        params = {
            "idProfessor": professor_id,
            "month": month,
            "year": year,
            "skip": skip,
            "take": take,
        }

        return self.api_client.call_api(
            resource_path=f"{self.base_path}/workout-monthyear-professor",
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            auth_settings=["Basic"],
            async_req=async_req,
        )

    @overload
    def get_default_workouts(
        self,
        employee_id: Optional[int] = None,
        tag_id: Optional[int] = None,
        async_req: Literal[True] = True,
    ) -> AsyncResult[Any]: ...

    @overload
    def get_default_workouts(
        self,
        employee_id: Optional[int] = None,
        tag_id: Optional[int] = None,
        async_req: Literal[False] = False,
    ) -> Any: ...

    def get_default_workouts(
        self,
        employee_id: Optional[int] = None,
        tag_id: Optional[int] = None,
        async_req: bool = False,
    ) -> Union[Any, AsyncResult[Any]]:
        """
        Get all default workouts with optional filtering.

        Args:
            employee_id: Filter by employee ID
            tag_id: Filter by tag ID
            async_req: Execute request asynchronously

        Returns:
            List of workout objects containing details like:
            - workout ID, name, and type
            - associated client/prospect/employee information
            - creation and validity dates
            - series and exercise details
            - professor information
            - status and settings
        """
        params = {
            "idEmployee": employee_id,
            "idTag": tag_id,
        }

        return self.api_client.call_api(
            resource_path=f"{self.base_path}/default-workout",
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            auth_settings=["Basic"],
            async_req=async_req,
        )

    @overload
    def link_workout_to_client(
        self,
        source_workout_id: int,
        prescription_employee_id: int,
        client_id: Optional[int] = None,
        prospect_id: Optional[int] = None,
        employee_id: Optional[int] = None,
        prescription_date: Optional[datetime] = None,
        async_req: Literal[True] = True,
    ) -> AsyncResult[Any]: ...

    @overload
    def link_workout_to_client(
        self,
        source_workout_id: int,
        prescription_employee_id: int,
        client_id: Optional[int] = None,
        prospect_id: Optional[int] = None,
        employee_id: Optional[int] = None,
        prescription_date: Optional[datetime] = None,
        async_req: Literal[False] = False,
    ) -> bool: ...

    def link_workout_to_client(
        self,
        source_workout_id: int,
        prescription_employee_id: int,
        client_id: Optional[int] = None,
        prospect_id: Optional[int] = None,
        employee_id: Optional[int] = None,
        prescription_date: Optional[datetime] = None,
        async_req: bool = False,
    ) -> Union[bool, AsyncResult[Any]]:
        """
        Link an existing workout to a client, prospect, or employee.

        Args:
            source_workout_id: ID of the workout to be linked
            prescription_employee_id: ID of the employee prescribing the workout
            client_id: ID of the client to link the workout to
            prospect_id: ID of the prospect to link the workout to
            employee_id: ID of the employee to link the workout to
            prescription_date: Date of the prescription (format: yyyy-MM-dd)
            async_req: Execute request asynchronously

        Returns:
            bool: True if the workout was successfully linked
        """
        if not any([client_id, prospect_id, employee_id]):
            raise ValueError(
                "Must provide either client_id, prospect_id, or employee_id"
            )

        params = {
            "sourceWorkoutId": source_workout_id,
            "idPrescriptionEmployee": prescription_employee_id,
            "idClient": client_id,
            "idProspect": prospect_id,
            "idEmployee": employee_id,
            "prescriptionDate": prescription_date,
        }

        return self.api_client.call_api(
            resource_path=f"{self.base_path}/link-workout-to-client",
            method="POST",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=bool,
            auth_settings=["Basic"],
            async_req=async_req,
        )
