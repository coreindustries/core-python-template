# /new-feature

Scaffold a new feature with routes, models, services, and tests following project standards.

## Usage

```
/new-feature <feature_name> [--with-db] [--crud]
```

## Arguments

- `feature_name`: Name of the feature in snake_case (e.g., `user_profile`, `payment`)
- `--with-db`: Include Prisma model scaffold
- `--crud`: Generate full CRUD operations

## Instructions

When this skill is invoked:

1. **Validate the feature name**:
   - Must be snake_case
   - Must not conflict with existing features
   - Check `src/project_name/` for existing modules

2. **Create the following files** (replace `{feature}` with the feature name):

   ### API Route (`src/project_name/api/{feature}.py`)
   ```python
   """API routes for {feature} feature."""

   from fastapi import APIRouter, HTTPException, status

   from project_name.models.{feature} import {Feature}, {Feature}Create, {Feature}Update
   from project_name.services.{feature} import {Feature}Service

   router = APIRouter(prefix="/{feature}s", tags=["{feature}s"])


   @router.get("/", response_model=list[{Feature}])
   async def list_{feature}s() -> list[{Feature}]:
       """List all {feature}s."""
       service = {Feature}Service()
       return await service.list_all()


   @router.get("/{{{feature}_id}}", response_model={Feature})
   async def get_{feature}({feature}_id: str) -> {Feature}:
       """Get a {feature} by ID."""
       service = {Feature}Service()
       result = await service.get_by_id({feature}_id)
       if not result:
           raise HTTPException(status_code=404, detail="{Feature} not found")
       return result


   @router.post("/", response_model={Feature}, status_code=status.HTTP_201_CREATED)
   async def create_{feature}(data: {Feature}Create) -> {Feature}:
       """Create a new {feature}."""
       service = {Feature}Service()
       return await service.create(data)


   @router.patch("/{{{feature}_id}}", response_model={Feature})
   async def update_{feature}({feature}_id: str, data: {Feature}Update) -> {Feature}:
       """Update a {feature}."""
       service = {Feature}Service()
       result = await service.update({feature}_id, data)
       if not result:
           raise HTTPException(status_code=404, detail="{Feature} not found")
       return result


   @router.delete("/{{{feature}_id}}", status_code=status.HTTP_204_NO_CONTENT)
   async def delete_{feature}({feature}_id: str) -> None:
       """Delete a {feature}."""
       service = {Feature}Service()
       if not await service.delete({feature}_id):
           raise HTTPException(status_code=404, detail="{Feature} not found")
   ```

   ### Model (`src/project_name/models/{feature}.py`)
   ```python
   """Pydantic models for {feature} feature."""

   from datetime import datetime

   from pydantic import Field

   from project_name.models import BaseSchema


   class {Feature}Base(BaseSchema):
       """Base {feature} schema."""

       name: str = Field(min_length=1, max_length=255)
       # TODO: Add feature-specific fields


   class {Feature}Create({Feature}Base):
       """Schema for creating a {feature}."""

       pass


   class {Feature}Update(BaseSchema):
       """Schema for updating a {feature}."""

       name: str | None = Field(default=None, min_length=1, max_length=255)
       # TODO: Add feature-specific fields


   class {Feature}({Feature}Base):
       """Schema for {feature} responses."""

       id: str
       created_at: datetime
       updated_at: datetime
   ```

   ### Service (`src/project_name/services/{feature}.py`)
   ```python
   """Business logic for {feature} feature."""

   from project_name.db import get_db
   from project_name.logging import get_audit_logger, AuditAction
   from project_name.models.{feature} import {Feature}, {Feature}Create, {Feature}Update
   from project_name.services import BaseService

   audit = get_audit_logger()


   class {Feature}Service(BaseService[{Feature}, {Feature}Create, {Feature}Update]):
       """Service for {feature} operations."""

       async def get_by_id(self, entity_id: str) -> {Feature} | None:
           """Get a {feature} by ID."""
           async with get_db() as db:
               result = await db.{feature}.find_unique(where={"id": entity_id})
               return {Feature}.model_validate(result) if result else None

       async def list_all(self) -> list[{Feature}]:
           """List all {feature}s."""
           async with get_db() as db:
               results = await db.{feature}.find_many()
               return [{Feature}.model_validate(r) for r in results]

       async def create(self, data: {Feature}Create) -> {Feature}:
           """Create a new {feature}."""
           async with get_db() as db:
               result = await db.{feature}.create(data=data.model_dump())
               audit.data_access(
                   user_id="system",  # TODO: Get from context
                   resource_type="{feature}",
                   resource_id=result.id,
                   action=AuditAction.DATA_CREATE,
               )
               return {Feature}.model_validate(result)

       async def update(self, entity_id: str, data: {Feature}Update) -> {Feature} | None:
           """Update a {feature}."""
           async with get_db() as db:
               update_data = data.model_dump(exclude_unset=True)
               if not update_data:
                   return await self.get_by_id(entity_id)
               result = await db.{feature}.update(
                   where={"id": entity_id},
                   data=update_data,
               )
               if result:
                   audit.data_access(
                       user_id="system",
                       resource_type="{feature}",
                       resource_id=entity_id,
                       action=AuditAction.DATA_UPDATE,
                   )
               return {Feature}.model_validate(result) if result else None

       async def delete(self, entity_id: str) -> bool:
           """Delete a {feature}."""
           async with get_db() as db:
               try:
                   await db.{feature}.delete(where={"id": entity_id})
                   audit.data_access(
                       user_id="system",
                       resource_type="{feature}",
                       resource_id=entity_id,
                       action=AuditAction.DATA_DELETE,
                   )
                   return True
               except Exception:
                   return False
   ```

   ### Tests (`tests/unit/test_{feature}.py`)
   ```python
   """Tests for {feature} feature."""

   import pytest
   from httpx import AsyncClient

   from project_name.models.{feature} import {Feature}Create


   class Test{Feature}API:
       """Tests for {feature} API endpoints."""

       @pytest.mark.asyncio
       async def test_create_{feature}(self, client: AsyncClient) -> None:
           """Test creating a {feature}."""
           response = await client.post(
               "/{feature}s",
               json={"name": "Test {Feature}"},
           )
           assert response.status_code == 201
           data = response.json()
           assert data["name"] == "Test {Feature}"
           assert "id" in data

       @pytest.mark.asyncio
       async def test_get_{feature}_not_found(self, client: AsyncClient) -> None:
           """Test getting a non-existent {feature}."""
           response = await client.get("/{feature}s/nonexistent")
           assert response.status_code == 404


   class Test{Feature}Service:
       """Tests for {feature} service."""

       def test_{feature}_create_model(self) -> None:
           """Test {Feature}Create model validation."""
           data = {Feature}Create(name="Test")
           assert data.name == "Test"
   ```

3. **If `--with-db` is specified**, add to `prisma/schema.prisma`:
   ```prisma
   model {Feature} {
     id        String   @id @default(cuid())
     name      String
     createdAt DateTime @default(now()) @map("created_at")
     updatedAt DateTime @updatedAt @map("updated_at")

     @@map("{feature}s")
   }
   ```

4. **Register the router** in `src/project_name/api/routes.py`:
   ```python
   from project_name.api.{feature} import router as {feature}_router
   router.include_router({feature}_router)
   ```

5. **After scaffolding**, remind the user to:
   - Run `uv run prisma generate` if database model was added
   - Run `uv run prisma migrate dev --name add_{feature}` to create migration
   - Update the generated code with feature-specific fields
   - Run `uv run pytest tests/unit/test_{feature}.py` to verify

## Example

```
/new-feature user_profile --with-db --crud
```

Creates:
- `src/project_name/api/user_profile.py`
- `src/project_name/models/user_profile.py`
- `src/project_name/services/user_profile.py`
- `tests/unit/test_user_profile.py`
- Updates `prisma/schema.prisma`
- Registers router in main routes
