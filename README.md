# TeamMate API 
___
#### A private-use mini API developed with Python and Django Rest Framework for team and member management. Is used PostgreSQL database for optimal data handling. Features CRUD endpoints for "teams" and "team members". Different user roles have distinct permissions.

## 🔧 Technologies used:
___
* [X] Django Rest Framework
* [X] Django ORM
* [X] PostgreSQL
* [X] Docker

# 🧾 Features
___
* [X] JWT authentication 🔒
* [X] CRUD functionality for Person and Team.
* [X] Detailed Documentation of all endpoints on "http://127.0.0.1:8000/api/doc/swagger/"
* [X] Totally Dockerized
* [X] Different permissions for different types of users:
  - Anyone can register at the portal;
  - Person (standard user) can update or delete only own account;
  - Person can choose the Team only while creating account;
  - Admin user can manage, delete or create any Person;
  - Only authenticated users can access Detail and List pages of a Team;
  - Admin user can manage Persons between Teams, update, delete and create Teams


### 💾 Installation:
___
#### 1. Clone the repository:
```shell
git clone https://github.com/bohdan-yatsyna/TeamMate_API
cd TeamMate_API
```
#### 2. Create and activate virtual environment with requirements install:
🖥 Windows:
```shell
python -m venv venv
venv\Scripts\activate
```
💻 Linux/MacOS:
```shell
python -m venv venv
source venv/bin/activate
```
#### 3. 🗝 Set up environment variables (using .env):
- Create an empty .env file in the root folder of the project.
- Copy the entire content of the .env.sample to your .env file.
- Modify the placeholders in the .env file with your preferable environment variables.

#### 4. 🐳 Run it with DOCKER:
- DOCKER should be installed and opened.
```shell
docker-compose up --build
```
- And open in your browser "http://127.0.0.1:8000/"

####  !!! Note, test data will be automatically loaded to the database !!!
### Feel free to use next admin user credentials to test my app:
```shell
email: admin@admin.com
password: admin123
```

#### 🗝 For creating own admin user:  
- Check actual container id of the application with ```docker ps```  
- Enter it to the next command and run ```docker exec -it <container_id> python manage.py createsuperuser```  

#### 🗝 For creating standard user next endpoints will help:  
- **User creating** - send a POST request to /api/persons/register/ 
- **Obtain token** - send a POST request to /api/persons/login/

#### 🗝 For Authorization:
- Install **ModHeader** extension and create Request header "Authorize" with value: Bearer &lt;Your access token&gt;


# 🕶 DEMO
### Documentation with all endpoints:
![sample_DOCUMENTATION](https://github.com/bohdan-yatsyna/TeamMate_API/blob/591832117fd79383491e1f31d9a39155aeddcc48/samples/Endpoints-sample-1.png)
