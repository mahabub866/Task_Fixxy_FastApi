# Task_Fixxy_FastApi
Create a FastAPI app with user registration/login, secure password hashing, role-based permissions, JWT authentication, and property management. Document and test the endpoints, ensuring robust security, and share the codebase with setup instructions for evaluation.

# Prerequisites
1. Mysql Database Server 7 or above
2. Python 3.8 or above
3. Python vertiual Environment Create **(python -m venv fast-env)** this script for windows if you use linux os then it will be **(python3.10 -m venv fast-env)**
4. Python Virtual Environment Activate **(fast-env\Scripts\fast-env)** this script for windows if you use linux os then it will be **(source fast-env/bin/activate)****

# Runing Process
In .env files please give your database host name and password correctly.I already have give a demo database Name (fixxy).If you give your database host and password properly then it will be automatically created a database. After that, you will run the following command **(uvicorn main:app --reload)** and server will be on automatically. If you do not give host or port then server will run default port is 8000 and it will be localhost **(http://127.0.0.1:8000)**.

