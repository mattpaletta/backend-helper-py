# Backend Helper Py

### Usage
```python
from backend_helper.postgres import connect
from psycopg2.extras import RealDictCursor

postgres_pool = connect(user = "postgres", 
                        password = "password",
                        host =  "localhost",
                        port = 5432,
                        database = "mydb",
                        minconn = 1, # defaults to 1
                        maxconn = 20, # defaults to 20
                        max_retries = 100) # defaults to 100

with postgres_pool.cursor(cursor_factory=RealDictCursor) as cur:
    cur.execute("SELECT * FROM mydb.my_table;")
    results = cur.fetchall()
```