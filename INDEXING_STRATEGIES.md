# Indexing strategies (including composite indexes)

Indexes speed up **lookups** (WHERE), **sorting** (ORDER BY), and **joins**. They cost extra writes and storage, so add them where queries are frequent and selective.

---

## 1. When to add indexes

| Use case | Example | Index type |
|----------|---------|------------|
| Filter often on a column | `Student.objects.filter(roll_no=101)` | Single-field (or unique) |
| Order often by a column | `Student.objects.order_by('-created_at')` | Single-field on `created_at` |
| Filter on A then sort by B | `filter(age=20).order_by('created_at')` | Composite `(age, created_at)` |
| Lookup by multiple columns together | `filter(age=20, roll_no__gte=100)` | Composite `(age, roll_no)` |

**Already indexed in Django (no extra work):**

- **Primary key** (`id`) – always indexed
- **`unique=True`** – creates a unique index (e.g. `email`, `roll_no`)
- **ForeignKey / OneToOne** – index on the foreign key column (e.g. `student_id`)

---

## 2. Single-field index: `db_index=True`

Use when you often filter or order by **one** column.

```python
class Student(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)  # single-field index
```

- **Pros:** Simple, good for one-column WHERE or ORDER BY.
- **Cons:** Only helps that one column; multiple columns in the same query need a composite index for best effect.

---

## 3. Composite index: `Meta.indexes`

Use when you often filter and/or order by **several columns together**. Order of columns matters (left-prefix: the index can be used for leading columns only).

```python
class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            # Good for: order_by('-created_at') then by roll_no, or filter(age=20).order_by('created_at')
            models.Index(fields=["-created_at", "roll_no"], name="student_created_roll_idx"),
            # Good for: filter(age=20, created_at__gte=...) or order_by('age', 'created_at')
            models.Index(fields=["age", "created_at"], name="student_age_created_idx"),
        ]
```

**Column order rules:**

- Put **equality filters** first (e.g. `age = 20`), then **range/sort** (e.g. `created_at`).
- The index can be used for **left-prefix** only: `(age, created_at)` helps `filter(age=20)`, and `filter(age=20).order_by('created_at')`, but not `order_by('created_at')` alone.

**Naming:** Use a short, clear name (e.g. `student_created_roll_idx`). Django generates one if you omit `name`.

---

## 4. Unique composite: `UniqueConstraint`

When uniqueness is on **multiple columns together** (not per column), use `UniqueConstraint` in `Meta.constraints`:

```python
class Meta:
    constraints = [
        models.UniqueConstraint(fields=["course", "student"], name="unique_enrollment")
    ]
```

---

## 5. Covering index (advanced)

Some databases support **covering** indexes (include extra columns so the query doesn’t touch the table). In Django you can use `include` in `Index` (Django 3.11+, PostgreSQL):

```python
models.Index(fields=["status"], name="ord_status_idx", include=["created_at", "total"])
```

---

## 6. What we added in this project

- **student.Student:**  
  - `created_at` with `db_index=True` (for `order_by('-created_at')`).  
  - Composite index `(created_at, roll_no)` for “recent first, then by roll”.
- **student.StudentProfile:**  
  - `created_at` with `db_index=True` (for list ordering).  
  - Composite `(student_id, created_at)` is redundant because `student` is already indexed (OneToOne); we only add `created_at` here.
- **oneToMany.Book:**  
  - `created_at` with `db_index=True`.  
  - Composite `(author, created_at)` for “books by author, by date”.
- **manyToMany.Course / Student:**  
  - `created_at` with `db_index=True` for ordering.

After changing models, run:

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

Use **Silk** (`/silk/`) to see query count and time, and **`QuerySet.explain()`** to check whether the database uses your indexes:

```python
# In shell: python manage.py shell
from student.models import Student
print(Student.objects.order_by('-created_at').explain())
```
