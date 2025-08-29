from sqlalchemy import text
from db import engine

with engine.begin() as conn:
    conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
    conn.execute(text("DROP TABLE IF EXISTS transactions"))
    conn.execute(text("DROP TABLE IF EXISTS users"))  
    conn.execute(text("DROP TABLE IF EXISTS plans"))
    conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
    
    conn.execute(text("""
    CREATE TABLE plans (
        plan_id INT AUTO_INCREMENT PRIMARY KEY,
        plan_name VARCHAR(100) NOT NULL,
        price DECIMAL(6,2) NOT NULL,
        data_gb DECIMAL(4,1) NOT NULL,
        validity_days INT NOT NULL
    )
    """))

    conn.execute(text("""
    CREATE TABLE users (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        phone VARCHAR(12) UNIQUE NOT NULL,
        name VARCHAR(50) NOT NULL,
        plan_id INT NOT NULL,
        balance_mb INT DEFAULT 0,
        FOREIGN KEY (plan_id) REFERENCES plans(plan_id)
    )
    """))

    conn.execute(text("""
    CREATE TABLE transactions (
        txn_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        amount DECIMAL(6,2) NOT NULL,
        txn_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status VARCHAR(20) DEFAULT 'completed',
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """))

    plans_data = [
        ('Jio Basic', 149.00, 1.0, 28),
        ('Airtel Smart', 249.00, 1.5, 28),
        ('Vi Power', 399.00, 2.0, 56),
        ('BSNL Value', 99.00, 0.5, 28),
        ('Jio Premium', 599.00, 2.5, 84)
    ]
    
    for plan in plans_data:
        conn.execute(text("""
            INSERT INTO plans (plan_name, price, data_gb, validity_days) 
            VALUES (:plan_name, :price, :data_gb, :validity_days)
        """), {
            'plan_name': plan[0], 'price': plan[1], 
            'data_gb': plan[2], 'validity_days': plan[3]
        })

    users_data = [
        ('9876543210', 'Rajesh Kumar', 1, 800),
        ('9123456789', 'Priya Sharma', 2, 1200),
        ('9988776655', 'Amit Singh', 3, 2000),
        ('9555444333', 'Sneha Gupta', 4, 400),
        ('9111222333', 'Vikash Yadav', 5, 2500)
    ]
    
    for user in users_data:
        conn.execute(text("""
            INSERT INTO users (phone, name, plan_id, balance_mb) 
            VALUES (:phone, :name, :plan_id, :balance_mb)
        """), {
            'phone': user[0], 'name': user[1], 
            'plan_id': user[2], 'balance_mb': user[3]
        })

    transactions_data = [
        (1, 149.00, '2024-08-15 10:30:00', 'completed'),
        (2, 249.00, '2024-08-20 14:15:00', 'completed'),
        (3, 399.00, '2024-08-10 09:45:00', 'completed'),
        (4, 99.00, '2024-08-25 16:20:00', 'completed'),
        (5, 599.00, '2024-07-30 11:10:00', 'completed')
    ]
    
    for txn in transactions_data:
        conn.execute(text("""
            INSERT INTO transactions (user_id, amount, txn_date, status) 
            VALUES (:user_id, :amount, :txn_date, :status)
        """), {
            'user_id': txn[0], 'amount': txn[1], 
            'txn_date': txn[2], 'status': txn[3]
        })

print("Simple telecom database created!")
