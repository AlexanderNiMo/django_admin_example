#Django admin example.

# Install:
        
        git clone https://github.com/AlexanderNiMo/django_admin_example.git
        docker build --tag docker-admin  ./
        docker run -d --rm \
            -p 8000:8000 \
            --name docker_admin \
            -v some_path:/db  \
            docker-admin
        docker exec -it docker_admin python manage.py createsuperuser

django admin is now available on localhost:8000/admin

# Files description:
- ./app/movies_admin/models.py - file with description of data base model
- ./app/movies_admin/admin.py - description of admin structure