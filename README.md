# Pageloot Test task


## Installation and Setup

### 1. Clone the Repository

```
git clone https://github.com/shaxxeno/pageloot-test.git
```

### 2. Install deps

```
poetry install
poetry shell
```

### 2. Configuration

1. Rename ```.env.sample``` to ```.env```
2. Set up your env variables


### 3. Migration and Running the project

```
python manage.py migrate
```

```
python manage.py runserver
```

### OTHER

Run tests with:

```
python manage.py test
```

Access swagger docs via

```
http://127.0.0.1:8000/docs/
```

NOTE:
- by_date_range and category_summary are not working properly in swagger, you can use CURL to test them manually.

```
curl -X GET "http://127.0.0.1:8000/api/expenses/by_date_range/?user_id=<id>&start_date=<date>&end_date=<date>"
```

```
curl -X GET "http://127.0.0.1:8000/api/expenses/category_summary/?user_id=<id>&month=<month>"
```