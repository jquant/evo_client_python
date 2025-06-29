"""Clean synchronous Workout API."""

from datetime import datetime
from typing import Any, Optional, cast

from .base import SyncBaseApi


class SyncWorkoutApi(SyncBaseApi):
    """Clean synchronous Workout API client."""

    def __init__(self, api_client=None):
        super().__init__(api_client)
        self.base_path = "/api/v1/workout"

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
    ) -> Any:
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

        Returns:
            Update result

        Example:
            >>> with SyncWorkoutApi() as api:
            ...     result = api.update_workout(
            ...         workout_id=123,
            ...         workout_name="New Strength Program",
            ...         start_date=datetime(2024, 1, 1),
            ...         total_weeks=12,
            ...         weekly_frequency=3
            ...     )
            ...     print(f"Workout updated: {result}")
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

        result = self.api_client.call_api(
            resource_path=self.base_path,
            method="PUT",
            query_params={k: v for k, v in params.items() if v is not None},
            auth_settings=["Basic"],
        )
        return result

    def get_client_workouts(
        self,
        client_id: Optional[int] = None,
        prospect_id: Optional[int] = None,
        employee_id: Optional[int] = None,
        workout_id: Optional[int] = None,
        inactive: Optional[bool] = None,
        deleted: Optional[bool] = None,
    ) -> Any:
        """
        Get workouts for a client, prospect or employee.

        Args:
            client_id: ID of the client
            prospect_id: ID of the prospect
            employee_id: ID of the employee
            workout_id: Specific workout ID to retrieve
            inactive: Include inactive workouts
            deleted: Include deleted workouts

        Returns:
            Workout data for the specified person

        Example:
            >>> with SyncWorkoutApi() as api:
            ...     workouts = api.get_client_workouts(
            ...         client_id=123,
            ...         inactive=False
            ...     )
            ...     for workout in workouts:
            ...         print(f"Workout: {workout.name}")
        """
        params = {
            "idClient": client_id,
            "idProspect": prospect_id,
            "idEmployee": employee_id,
            "idWorkout": workout_id,
            "inactive": inactive,
            "deleted": deleted,
        }

        result = self.api_client.call_api(
            resource_path=f"{self.base_path}/default-client-workout",
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            auth_settings=["Basic"],
        )
        return result

    def get_workouts_by_month_year_professor(
        self,
        professor_id: Optional[int] = None,
        month: Optional[int] = None,
        year: Optional[int] = None,
        skip: Optional[int] = None,
        take: Optional[int] = None,
    ) -> Any:
        """
        Get workouts filtered by month, year and/or professor.

        Args:
            professor_id: The ID of the professor who created the workouts
            month: Month to filter workouts
            year: Year to filter workouts
            skip: Number of records to skip
            take: Number of records to return (max 50)

        Returns:
            Filtered workout data

        Example:
            >>> with SyncWorkoutApi() as api:
            ...     workouts = api.get_workouts_by_month_year_professor(
            ...         professor_id=5,
            ...         month=12,
            ...         year=2024,
            ...         take=20
            ...     )
            ...     print(f"Found {len(workouts)} workouts")
        """
        params = {
            "idProfessor": professor_id,
            "month": month,
            "year": year,
            "skip": skip,
            "take": take,
        }

        result = self.api_client.call_api(
            resource_path=f"{self.base_path}/workout-monthyear-professor",
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            auth_settings=["Basic"],
        )
        return result

    def get_default_workouts(
        self,
        employee_id: Optional[int] = None,
        tag_id: Optional[int] = None,
    ) -> Any:
        """
        Get all default workouts with optional filtering.

        Args:
            employee_id: Filter by employee ID
            tag_id: Filter by tag ID

        Returns:
            List of workout objects containing details like:
            - workout ID, name, and type
            - associated client/prospect/employee information
            - creation and validity dates
            - series and exercise details
            - professor information
            - status and settings

        Example:
            >>> with SyncWorkoutApi() as api:
            ...     workouts = api.get_default_workouts(
            ...         employee_id=10,
            ...         tag_id=5
            ...     )
            ...     for workout in workouts:
            ...         print(f"Default workout: {workout.name}")
        """
        params = {
            "idEmployee": employee_id,
            "idTag": tag_id,
        }

        result = self.api_client.call_api(
            resource_path=f"{self.base_path}/default-workout",
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            auth_settings=["Basic"],
        )
        return result

    def link_workout_to_client(
        self,
        source_workout_id: int,
        prescription_employee_id: int,
        client_id: Optional[int] = None,
        prospect_id: Optional[int] = None,
        employee_id: Optional[int] = None,
        prescription_date: Optional[datetime] = None,
    ) -> bool:
        """
        Link an existing workout to a client, prospect, or employee.

        Args:
            source_workout_id: ID of the workout to be linked
            prescription_employee_id: ID of the employee prescribing the workout
            client_id: ID of the client to link the workout to
            prospect_id: ID of the prospect to link the workout to
            employee_id: ID of the employee to link the workout to
            prescription_date: Date of the prescription (format: yyyy-MM-dd)

        Returns:
            bool: True if the workout was successfully linked

        Raises:
            ValueError: If no target person (client_id, prospect_id, or employee_id) is provided

        Example:
            >>> with SyncWorkoutApi() as api:
            ...     success = api.link_workout_to_client(
            ...         source_workout_id=456,
            ...         prescription_employee_id=10,
            ...         client_id=123,
            ...         prescription_date=datetime.now()
            ...     )
            ...     print(f"Workout linked: {success}")
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

        result = self.api_client.call_api(
            resource_path=f"{self.base_path}/link-workout-to-client",
            method="POST",
            query_params={k: v for k, v in params.items() if v is not None},
            auth_settings=["Basic"],
        )
        return cast(bool, result)
