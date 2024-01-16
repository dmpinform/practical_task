
### alembic ###

```bash
reports run-alembic revision --autogenerate -m "initial"
```
```bash
reports run-alembic upgrade head
```
```bash
reports run-alembic downgrade base
```
```bash
uvicorn api:app --reload
```
