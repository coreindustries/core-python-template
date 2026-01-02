# /optimize

Analyze and optimize code for performance, database queries, and async patterns.

## Usage

```
/optimize [target] [--type <type>] [--profile]
```

## Arguments

- `target`: File, function, or endpoint to optimize (default: current file)
- `--type <type>`: Type of optimization:
  - `performance`: General performance improvements
  - `database`: Database query optimization
  - `async`: Async/await pattern improvements
  - `memory`: Memory usage optimization
- `--profile`: Suggest profiling tools and commands

## Instructions

When this skill is invoked:

1. **Analyze the target**:
   - Read the target code
   - Identify performance bottlenecks
   - Check database query patterns
   - Review async/await usage
   - Look for N+1 queries, inefficient loops, blocking operations

2. **Identify optimization opportunities**:

   ### Database Optimization

   - **N+1 Query Problem**: Multiple queries in loops
   - **Missing Indexes**: Queries without proper indexes
   - **Inefficient Joins**: Complex queries that can be simplified
   - **Over-fetching**: Selecting unnecessary columns
   - **Missing Pagination**: Loading all records at once

   **Example:**
   ```python
   # Before (N+1 queries)
   async def get_users_with_profiles(user_ids: list[str]) -> list[UserWithProfile]:
       users = []
       for user_id in user_ids:
           user = await db.user.find_unique(where={"id": user_id})
           profile = await db.profile.find_unique(where={"userId": user_id})
           users.append(UserWithProfile(user=user, profile=profile))
       return users

   # After (batch query)
   async def get_users_with_profiles(user_ids: list[str]) -> list[UserWithProfile]:
       users = await db.user.find_many(where={"id": {"in": user_ids}})
       profiles = await db.profile.find_many(where={"userId": {"in": user_ids}})
       profile_map = {p.userId: p for p in profiles}
       return [
           UserWithProfile(user=u, profile=profile_map.get(u.id))
           for u in users
       ]
   ```

   ### Async Optimization

   - **Sequential await**: Operations that can run concurrently
   - **Blocking operations**: Synchronous code in async functions
   - **Missing concurrency**: Not using asyncio.gather()

   **Example:**
   ```python
   # Before (sequential)
   async def fetch_all_data(user_id: str) -> dict:
       user = await get_user(user_id)
       profile = await get_profile(user_id)
       settings = await get_settings(user_id)
       return {"user": user, "profile": profile, "settings": settings}

   # After (concurrent)
   async def fetch_all_data(user_id: str) -> dict:
       user, profile, settings = await asyncio.gather(
           get_user(user_id),
           get_profile(user_id),
           get_settings(user_id),
       )
       return {"user": user, "profile": profile, "settings": settings}
   ```

   ### Performance Optimization

   - **Inefficient loops**: O(n²) algorithms that can be O(n)
   - **Repeated computations**: Calculations in loops
   - **Large data processing**: Not using generators or pagination
   - **String concatenation**: Using + instead of join()

   **Example:**
   ```python
   # Before (inefficient)
   def process_items(items: list[str]) -> str:
       result = ""
       for item in items:
           result += item.upper() + ","
       return result

   # After (efficient)
   def process_items(items: list[str]) -> str:
       return ",".join(item.upper() for item in items)
   ```

3. **Apply optimizations**:
   - Refactor inefficient patterns
   - Add database indexes if needed
   - Use batch operations for database queries
   - Implement concurrent async operations
   - Optimize algorithms and data structures
   - Add caching where appropriate

4. **Verify optimizations**:
   - Run tests to ensure functionality unchanged
   - Check performance improvements
   - Verify database query counts reduced
   - Ensure async operations are truly concurrent

## Optimization Patterns

### Database Query Optimization

1. **Use batch queries**:
   ```python
   # Instead of loop with individual queries
   results = await db.model.find_many(where={"id": {"in": ids}})
   ```

2. **Select only needed fields**:
   ```python
   # Select specific fields instead of all
   users = await db.user.find_many(select={"id": True, "email": True})
   ```

3. **Use pagination**:
   ```python
   # Paginate large result sets
   users = await db.user.find_many(skip=offset, take=limit)
   ```

4. **Add database indexes** (in Prisma schema):
   ```prisma
   model User {
     email String @unique
     createdAt DateTime

     @@index([email])
     @@index([createdAt])
   }
   ```

### Async Pattern Optimization

1. **Use asyncio.gather() for concurrent operations**:
   ```python
   results = await asyncio.gather(*[fetch_data(id) for id in ids])
   ```

2. **Use asyncio.create_task() for fire-and-forget**:
   ```python
   task = asyncio.create_task(send_notification(user_id))
   # Continue with other work
   ```

3. **Avoid blocking operations in async functions**:
   ```python
   # Use run_in_executor for CPU-bound work
   result = await loop.run_in_executor(None, cpu_intensive_function, data)
   ```

### Memory Optimization

1. **Use generators for large datasets**:
   ```python
   def process_large_dataset():
       for item in large_list:
           yield process(item)
   ```

2. **Use streaming for file operations**:
   ```python
   async with aiofiles.open(file_path) as f:
       async for line in f:
           process(line)
   ```

## Profiling Tools

When `--profile` is specified, suggest:

```bash
# Python profiling
uv run python -m cProfile -o profile.stats script.py
uv run python -m pstats profile.stats

# Memory profiling
uv add --dev memory-profiler
uv run python -m memory_profiler script.py

# Async profiling
uv add --dev py-spy
uv run py-spy record -o profile.svg -- python script.py
```

## Example

```
/optimize src/project_name/api/users.py --type database --profile
```

Analyzes database queries in `users.py`, identifies N+1 problems, suggests batch queries, and provides profiling commands.
