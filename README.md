# phan_tan_20191

## Yêu cầu môi trường cần cài trước khi run project
- Python 3.7.3
- pipenv
- database Postgres

## Các bước run project (Yêu cầu teminal đã trỏ đến project)
B1: Cài mỗi trường pipenv
### pipenv install
### pipenv shell 
B1: Cài các package cần thiết
### pipenv install
B3: Tạo database ở máy máy local với tên tùy ý (vd: db_phan_tan)
B4: Tạo file ".env" trong project, nội dung file là:
### ENVIRONMENT=DEVELOPMENT
### DATABASE_URI=postgresql://{database_user_name}}}:{database_password}@{host_db}:5432/{database_name}
B5: Tạo bảng trong database
### export DATABASE_URI=postgresql://{database_user_name}}}:{database_password}@{host_db}:5432/{database_name}
### alembic upgrade heads
B6: Run project
### python run.py