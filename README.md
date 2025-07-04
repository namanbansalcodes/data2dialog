# data2dialog

**data2dialog** is a powerful LLM-powered application designed specifically for managers and product owners. With this tool, you can chat directly with your database, making data queries and operations as simple as having a conversation.

This application leverages the capabilities of state-of-the-art language models to interpret and execute commands, giving users an intuitive and user-friendly interface to interact with their database.

## Getting Started

Follow these steps to get the application up and running in a development environment:

### 1. Create a Configuration File

Before starting the application, you need to create a configuration file to store the application's secret key and mode.

```bash
touch secrets.env
```

Inside the secrets.env file, add the following:

```
SECRET_KEY=<your_secret_key>
MODE="DEV"
```
Note: Replace <your_secret_key> with any random string of your choice. This will be used by Django for various purposes including cryptographic signing.

### 2. Build the Docker Containers
To build the necessary Docker containers for the application, use the following command:

```bash
Copy code
docker-compose -f docker-compose-dev.yml build
```
This will set up the required environment for the application using the configuration provided in the docker-compose-dev.yml file.


### 3. Run the Application
Once the Docker containers have been built, you can start the application with the following command:

```bash
Copy code
docker-compose -f docker-compose-dev.yml up
```
The application should now be up and running. Navigate to the designated port on your local machine to access the data2dialog interface.


Contribution
If you're collaborating on this project, we're excited to have you on board! Please make sure you follow the setup instructions correctly to ensure a consistent development environment.

Feedback & Suggestions
We welcome feedback and suggestions to enhance the capabilities and performance of data2dialog. Please feel free to create an issue or submit a pull request.

License
This project is licensed under the MIT License.

