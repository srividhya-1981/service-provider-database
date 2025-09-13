
# Service Provider Data Collection Form

## ✅ Setup Instructions

1. Install Python 3.8+ and PostgreSQL.

2. Create the database and table:
   ```sql
   CREATE DATABASE service_provider_db;

   \c service_provider_db

   CREATE TABLE service_providers (
       provider_id SERIAL PRIMARY KEY,
       zone VARCHAR(255),
       sub_zone VARCHAR(255),
       area VARCHAR(255),
       service_type VARCHAR(255),
       provider_name VARCHAR(255),
       address TEXT,
       contact_landline VARCHAR(100),
       contact_mobile VARCHAR(100),
       delivery_available BOOLEAN,
       immediate_delivery BOOLEAN,
       delivery_charges VARCHAR(100),
       service_hours VARCHAR(255),
       field_visit_done BOOLEAN,
       field_visit_remarks TEXT,
       last_verified_date DATE,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```

3. Update database credentials in `app.py`.

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the application:
   ```bash
   python app.py
   ```

6. Access the form at:  
   [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

7. render.com 
   ayurasstparentcare
   hostname:dpg-d32o73ruibrs73a1edhg-a
   Database
service_provider_database

Username
service_provider_database_user

Password
6GcC9sy22YQsZxV2tYn8fuF4eDudeSvV


Internal Database URL
postgresql://service_provider_database_user:6GcC9sy22YQsZxV2tYn8fuF4eDudeSvV@dpg-d32o73ruibrs73a1edhg-a/service_provider_database


External Database URL
postgresql://service_provider_database_user:6GcC9sy22YQsZxV2tYn8fuF4eDudeSvV@dpg-d32o73ruibrs73a1edhg-a.oregon-postgres.render.com/service_provider_database



