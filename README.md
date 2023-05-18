## Challenge: User service
The objective of this exercise is to implement a rest-service which is able to:

- Create new user with contact data
- Return user by id
- Return user by name
- Add additional mail/phone data
- Update existing mail/phone data
- Delete user

The data objects are defined as followed:
```
User:
    id: <int>
    lastName: <string>
    firstName: <string>
    emails: List<Email>
    phoneNumbers: List<PhoneNumber>

Email:
    id: <int>
    mail: <string>
    
PhoneNumber:
    id: <int>
    number: <string>
```

#### Constraints
- You provide straightforward documentation how to build and run the service
- Submitted data is stored in database (free choice which one)
- You can only use the following programming languages: Scala, Java, Python
- If using Python, we strongly suggest not using the Django framework

#### Bonus
- You let your service run within a container based environment (Docker, Kubernetes)
- You provide documentation of your services API endpoints
- Your service is covered with tests

## Installation
#### Docker
*You need to have installed Docker on your computer

- Build Docker image
```
docker-compose build --no-cache
```
- Run application
```
docker-compose up 
```
- Open the app in a browser
```
http://127.0.0.1:5050
```

#### Standalone run
*Recommended python version is 3.10

- Install dependencies
```
pip3 install -r requirements.txt
```
- From root of the app run the command
```
python -m flask run --host=0.0.0.0 --port=5050
```

## Documentation

#### Built-in documentation
The app has endpoint to swagger documentation. Open the link in your browser when the application is running:
```
http://127.0.0.1:5000/docs/
```

#### Postman Documentation
Swagger file is uploaded to Postman website. Here is the link to the documentation

 [Documentation on Postman website](https://www.postman.com/samoilenko26/workspace/user-service/api/5e6b562a-364a-4375-b8c3-c6c1d05df5c7)
*Open a **Definition** tab

#### Swagger Json
For manual visualisation you can download swagger.json
 [swagger.json](https://github.com/SamoylenkoVadim/user-service/blob/main/swagger.json)

## Endpoint testing
All endpoints are loaded to the Postman with all necessaries parameters. 

 [Documentation on Postman website](https://www.postman.com/samoilenko26/workspace/user-service/api/5e6b562a-364a-4375-b8c3-c6c1d05df5c7)
*Open a **User Service** collection

You can use the resource as examples of a requests. Or open it on the Desktop version of Postman and use it for testing without extra settings.

## Run unit/pytests

From the root directory of the application run the command
```
 pytest tests 
```







