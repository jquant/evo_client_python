# API Documentation Guidelines

## Before You Begin

### 1. Verify Implementation

Before writing or updating any API documentation, ALWAYS:

1. Check the API implementation in `src/evo_client/api/` to understand:
   - Available methods and their parameters
   - Return types
   - Error handling
   - Authentication requirements

2. Verify models in `src/evo_client/models/` to confirm:
   - Which models actually exist
   - Required and optional fields
   - Field types and constraints
   - Model relationships

3. Run a test implementation to verify:
   - The documented behavior matches actual behavior
   - All examples are runnable
   - Error cases are handled correctly

NEVER document features, models, or methods that don't exist in the implementation.

## Core Documentation Elements

### 1. Pydantic Models

First, verify the model exists and check its implementation. Then document:

```python
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class ExampleModel(BaseModel):
    """Brief description of the model's purpose.

    Detailed explanation of when and how to use this model.
    Include any important notes about validation or constraints.

    Attributes:
        field_name (Type): Detailed description of the field including:
            - Purpose and usage
            - Validation rules
            - Business logic constraints
            - Default behavior if optional
    """
    field_name: str = Field(
        default=None,
        description="Clear description of field purpose",
        examples=["example1", "example2"]
    )
    number_field: Optional[int] = Field(
        default=None,
        description="Description of numeric field",
        examples=[123, 456]
    )

    model_config = ConfigDict(
        json_schema_extra={
            'examples': [
                {
                    'field_name': "example value",
                    'number_field': 123
                },
                {
                    'field_name': "another example",
                    'number_field': 456
                }
            ]
        }
    )
```

### 2. API Methods

Always check the actual implementation before documenting methods:

```python
def method_name(
    self, 
    param1: ModelName,
    param2: Optional[int] = None
) -> ReturnModel:
    """One-line description of method purpose.

    More detailed explanation of the method's functionality,
    including important notes about usage or behavior.

    Args:
        param1: Detailed description of the first parameter
            Reference the model: :class:`~package.ModelName`
        param2: Description of optional parameter
            Include valid values and default behavior

    Returns:
        :class:`~package.ReturnModel`: Description of return value
            Include possible states and values

    Raises:
        ValueError: When and why this occurs
        TypeError: Other error conditions

    Examples:
        >>> api = SalesApi()
        >>> result = api.method_name(
        ...     param1=ModelName(field="value"),
        ...     param2=123
        ... )
    """
```

### 3. RST Documentation Structure

```rst
Module Name
===========

Brief introduction of module purpose and functionality.
Include only features that are actually implemented.

API Reference
------------

.. autoclass:: package.module.ClassName
   :members:
   :undoc-members:
   :special-members: __init__

Models
------

Only document models that exist in the codebase.
For each model, verify its implementation before documentation.

Examples
--------

Ensure all examples:
1. Use only existing methods and models
2. Have been tested and work as documented
3. Follow best practices
4. Include error handling where appropriate
```

## Best Practices

1. **Verify First**: Always check the actual implementation before writing or updating documentation.

2. **Test Examples**: All code examples should be tested to ensure they work with the current implementation.

3. **Be Accurate**: Never document features, models, or methods that don't exist.

4. **Stay Updated**: When the implementation changes, update the documentation to match.

5. **Cross-Reference**: Link to related models and methods that exist in the codebase.

6. **Error Handling**: Document common errors and their solutions based on actual implementation.

## Documentation Review Checklist

Before submitting documentation changes:

- [ ] Verified all documented features exist in implementation
- [ ] Checked all referenced models exist
- [ ] Tested all code examples
- [ ] Confirmed all method signatures match implementation
- [ ] Verified error cases and handling
- [ ] Checked cross-references point to existing code
- [ ] Ensured authentication requirements are accurate
- [ ] Validated all links and references

## Common Pitfalls to Avoid

1. Documenting planned features that aren't implemented yet
2. Referencing models or methods that don't exist
3. Providing examples that won't work with current implementation
4. Missing important parameters or return types
5. Outdated authentication methods
6. Incorrect error handling examples
7. Broken cross-references

Remember: Documentation should always reflect the current state of the code, not future plans or past implementations.