### Prerequisites:

- Python 3
- MongoDB


### Python Command Usage for Different Operating Systems:

- On Windows, use `python` to run Python commands.
- On macOS/Linux, use `python3` to ensure Python 3 is used.


### Steps to Set Up and Run the Project:

1. Clone the project repository.
    command: git clone https://github.com/nikhil200603/Projects.git

2. Create a virtual environment:
    command: python3 -m venv myenv

3. Activate the virtual environment:
    - On Windows:
        command: myenv\Scripts\activate
    - On macOS/Linux:
        command: source myenv/bin/activate

4. Navigate to the 'Projects' directory:
    command: cd Projects

5. Install the project dependencies:
    command: pip install -r requirements.txt

6. Open the `mongosh` terminal.
    command: mongosh

7. Switch to the admin user:
    command: use admin

8. Create a new user:
    command: db.createUser({
                user: "assessment_project_user",
                pwd: "assessment_project_pass",
                roles: [{ role: "readWrite", db: "assessment_project" }]
             })

9. Go back to the Projects directory:

10. Navigate to the `app` directory:
    command: cd app

11. Run the project:
    command: python3 main.py

12. The project will start running on port 8080.

13. Open your browser and access the project:
    - Go to http://0.0.0.0:8080/docs or http://localhost:8080/docs.

14. Perform the required operations via the documentation interface.


### Steps to Set Up the Project for Deploying in AWS Lambda:

# Alternatively, you can optionally pull the aws_lambda branch and start directly from step 6.

1. Move the main.py file from the app directory to the project directory.

2. Update the requirements.txt file with the following versions, which are compatible with AWS Lambda:

   mangum==0.19.0  
   PyJWT==2.8.0  
   pymongo==4.10.1  
   q==2.7  
   six==1.17.0

3. Add app. to all imports originating from the app directory.

   Example:  
   Before:  
   from api.auth_routes import auth_router

   After:  
   from app.api.auth_routes import auth_router

4. Add a handler in the main.py file with the following code:

   from mangum import Mangum

   handler = Mangum(app)

5. Add MONGODB_AWS_LAMBDA_URI in the config.py file, which should contain the MongoDB Atlas cluster URI. Ensure the connection is established using this URI.

6. Create one directory for deployment in project directory.
    command: mkdir deployment_package

7. Copy Project files into that directory.
    command: cp -R app main.py requirements.txt deployment_package/

8. Navigate to the deployment folder.
    command: cd deployment_package

9. Install dependencies.
    command: pip install -r requirements.txt -t .

10. Compress all contents of the deployment_package folder into a .zip file in Project directory.
    command: zip -r ../deployment_package.zip .

11. Go to Project directory.
    command: cd ..

12. Go to the AWS Management Console in any Browser. 

13. Search Lambda in search bar and open Lambda Service.

14. Click on create function to create a new lambda function.

15. Write Project name, select python 3.8 in runtime environment.

16. In Additional Configuration, enable Function URL, select NONE instead of AWS_IAM.

17. Now click on create function.

18. In code section click on upload from and upload the zip file you created in local.

19. Scroll down, in Runtime settings. change handler to main.handler .

20. Now it is deployed and running.You can check by opening function URL.

21. For swagger add /docs after function URL.

