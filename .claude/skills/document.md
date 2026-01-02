# /document

Generate and update documentation for code, APIs, and project.

## Usage

```
/document [target] [--type <type>] [--update-readme]
```

## Arguments

- `target`: File, directory, or API endpoint to document (default: current file)
- `--type <type>`: Type of documentation to generate:
  - `docstrings`: Add/update function/class docstrings
  - `api`: Generate API documentation (OpenAPI/Swagger)
  - `readme`: Update README.md sections
  - `examples`: Generate code examples
- `--update-readme`: Also update README.md with new features

## Instructions

When this skill is invoked:

1. **Analyze the target**:
   - Read the target file(s)
   - Identify undocumented functions, classes, modules
   - Check existing documentation quality
   - Review related files for context

2. **Generate documentation** based on type:

   ### Docstrings (`--type docstrings`)

   For each public function/class:
   - Add Google-style docstring if missing
   - Update existing docstrings if incomplete
   - Include:
     - Brief description
     - Args section with types and descriptions
     - Returns section with type and description
     - Raises section for exceptions
     - Examples for complex functions

   **Template:**
   ```python
   def function_name(param1: Type1, param2: Type2) -> ReturnType:
       """Brief description of what the function does.

       More detailed description if needed. Can span multiple lines
       and explain the function's purpose, behavior, and usage.

       Args:
           param1: Description of param1 and its purpose.
           param2: Description of param2 and its constraints.

       Returns:
           Description of what is returned and its structure.

       Raises:
           ValueError: When param1 is invalid.
           NotFoundError: When resource is not found.

       Example:
           >>> result = function_name("value1", "value2")
           >>> print(result)
           "expected output"
       """
   ```

   ### API Documentation (`--type api`)

   - Review FastAPI routes
   - Ensure all endpoints have:
     - Descriptive summary and description
     - Proper response models
     - Error response documentation
     - Example request/response
   - Update OpenAPI schema if needed

   **Example:**
   ```python
   @router.post(
       "/users",
       response_model=User,
       status_code=status.HTTP_201_CREATED,
       summary="Create a new user",
       description="Creates a new user account with the provided information.",
       responses={
           201: {"description": "User created successfully"},
           400: {"description": "Invalid input data"},
           409: {"description": "User already exists"},
       },
   )
   async def create_user(data: UserCreate) -> User:
       """Create a new user account."""
       # ...
   ```

   ### README Updates (`--type readme` or `--update-readme`)

   - Add new features to Features section
   - Update API examples if endpoints changed
   - Add new environment variables to Configuration section
   - Update installation steps if dependencies changed
   - Add new commands to Commands section

3. **Follow documentation standards**:
   - Use Google-style docstrings (see prd/01_Technical_standards.md)
   - Include type information in Args
   - Provide examples for complex APIs
   - Keep descriptions concise but complete
   - Use proper markdown formatting in README

4. **Verify documentation**:
   - Check that all public APIs are documented
   - Ensure docstrings match function signatures
   - Verify README examples work
   - Check for broken links or outdated information

## Documentation Standards

### Module-Level Docstrings

```python
"""Module for user management.

This module provides functionality for creating, updating, and managing
user accounts in the system. It includes authentication, authorization,
and user profile management features.

Classes:
    UserService: Main service for user operations.
    UserRepository: Data access layer for users.

Functions:
    validate_user_email: Validates email format.
    hash_password: Securely hashes passwords.
"""
```

### Class Docstrings

```python
class UserService:
    """Service for user management operations.

    This service handles all business logic related to users, including
    creation, updates, authentication, and authorization.

    Attributes:
        repository: UserRepository instance for data access.
        logger: Logger instance for logging operations.

    Example:
        >>> service = UserService()
        >>> user = await service.create_user(UserCreate(email="test@example.com"))
        >>> print(user.email)
        "test@example.com"
    """
```

### Function Docstrings

```python
async def create_user(data: UserCreate) -> User:
    """Create a new user account.

    Creates a user account with the provided information. Validates
    the email format, checks for duplicates, and hashes the password
    before storing.

    Args:
        data: UserCreate model containing user information.

    Returns:
        User model representing the created user.

    Raises:
        ValidationError: If email format is invalid.
        DuplicateUserError: If user with email already exists.

    Example:
        >>> data = UserCreate(email="user@example.com", name="John")
        >>> user = await create_user(data)
        >>> assert user.email == "user@example.com"
    """
```

## Example

```
/document src/project_name/api/users.py --type docstrings --update-readme
```

Generates docstrings for all functions in `users.py` and updates README.md with API documentation.
