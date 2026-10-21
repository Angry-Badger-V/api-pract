## Database Setup
This project uses PostgreSQL.
To create/reset the database, run the setup script from the project root:
```
psql -f db/setup.sql
```
Create .env file in project root directory. Use .env.example as template.
Add credientials to your .env:
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=nc_plus_one
DB_USER=your_postgres_username
DB_PASSWORD=your_postgres_password
```
Install project dependencies:
```
pip install -r requirements.txt
```
For info on specific dependency versions see requirements.txt


