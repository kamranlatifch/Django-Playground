# Query optimization and query analysis (using Silk)

**Silk** (we use **django-silky**, the Django 6–compatible fork) records every HTTP request and all SQL queries run during that request. You get query count, total time, duplicate queries, and a Python profiler so you can find N+1 issues and slow views.

---

## 1. Install and run

```bash
# From project root, with your venv activated:
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver
```

Then open **http://127.0.0.1:8000/silk/** in your browser. You’ll see a list of recent requests. Click one to see:

- **SQL** – every query, with count and time
- **Profile** – Python-level timing (if enabled)
- **Meta** – request headers, GET/POST, etc.

---

## 2. What to look for (query analysis)

| Issue                          | What it means                                     | What to do                                                |
| ------------------------------ | ------------------------------------------------- | --------------------------------------------------------- |
| **High query count**           | Many round-trips to the DB for one page           | Reduce with `select_related()` / `prefetch_related()`     |
| **Duplicate queries**          | Same SQL run many times (e.g. per item in a loop) | Classic **N+1**: fetch related data in one or few queries |
| **Slow total time**            | One or more heavy queries                         | Add DB indexes, simplify queries, or cache                |
| **Repeated identical queries** | Same query with same params run again and again   | Use `select_related`/`prefetch_related` or caching        |

---

## 3. Common optimizations

### N+1 and `select_related` / `prefetch_related`

- **N+1:** 1 query for the list + N queries (e.g. one per row) for a related object.
- **Fix:**
  - **ForeignKey / OneToOne:** use `select_related('related_name')` so the relation is fetched in the same query (JOIN).
  - **Many-to-many / reverse ForeignKey (multiple related rows):** use `prefetch_related('related_name')` so Django does one extra query and joins in Python.

**Example – before (N+1):**

```python
# In a view: one query for profiles, then one query per profile when you access profile.student
profiles = StudentProfile.objects.all().order_by("-created_at")
# In template: {% for p in profiles %} {{ p.student.name }} → 1 + N queries
```

**Example – after (2 queries):**

```python
profiles = StudentProfile.objects.select_related("student").order_by("-created_at")
# Now each p.student is already loaded → 1 query total (JOIN)
```

### Only fetch what you need

- Use `only()` or `defer()` when you don’t need all columns:
  - `Student.objects.only("id", "name", "email")`
- Use `values()` / `values_list()` for lists or dicts instead of full model instances when that’s enough.

### Indexes

- Add `db_index=True` or `Meta.indexes` on fields you filter or order by often. Run migrations after changing models.

---

## 4. Workflow with Silk

1. Reproduce the slow or heavy page (e.g. list of students or profiles).
2. Open **/silk/** and click the corresponding request.
3. Check **SQL**: number of queries and total time; look for duplicates.
4. Change the view (e.g. add `select_related`/`prefetch_related`), reload the page, then check the same request again in Silk to compare.

---

## 5. Settings (in `settings.py`)

- **`SILKY_ANALYZE_QUERIES`** – record and show SQL (default True).
- **`SILKY_PYTHON_PROFILER`** – record Python profiling (default True).
- **`SILKY_INTERCEPT_PERCENT`** – percentage of requests to profile (100 = all).
- **`SILKY_META`** – show request meta (headers, etc.).

Disable or restrict Silk in production (e.g. `INTERCEPT_PERCENT = 0` or remove the app); it’s for development and debugging.

---

## 6. Example in this project

- **`profile_list`** view uses `select_related("student")` so listing profiles doesn’t cause one extra query per profile for `profile.student`. In Silk you’ll see fewer queries and lower time compared to using `StudentProfile.objects.all()` without `select_related`.

Use **/silk/** to compare before/after and to inspect any other view’s queries.
