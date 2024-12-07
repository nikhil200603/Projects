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

