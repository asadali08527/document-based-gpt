
# Document-Based GPT Frontend

## Overview

This is the frontend of the Document-Based GPT system, implemented using React. The application provides a user interface for interacting with a document-based question-answering system, allowing users to register/login, upload documents (for admin users), and ask questions based on the uploaded documents.

The frontend connects to a FastAPI-based backend which handles authentication, document processing, and querying.

## Tech Stack & Libraries Used

- **React**: A JavaScript library for building user interfaces.
- **axios**: For making HTTP requests to the backend API.
- **jwt-decode**: For decoding JSON Web Tokens (JWT) to manage user sessions.
- **Bootstrap (or any other CSS framework)**: For styling and UI components.

## Project Directory Structure

```
/src
  ├── App.js                  # Main application logic
  ├── App.css                 # Styles for the application
  ├── index.js                # Entry point for the React app
  ├── components/             # Reusable UI components
  └── services/               # Axios services for API calls
```

## Important Files

### `App.js`

Contains the main logic for the application including routing, state management, and conditional rendering based on user role (admin or user).

### `App.css`

Provides styling for the UI components to make the application visually appealing and responsive.

## Running the Solution

To build and run the frontend React application using Docker, follow these steps:

1. Ensure you have Docker installed on your machine.
2. Build the Docker image using the following command:

    ```bash
    docker build -t document-gpt-client:latest .
    ```

3. Once the build is complete, run the Docker container:

    ```bash
    docker run -p 3000:3000 document-gpt-client:latest
    ```

4. After the container is up and running, visit [http://localhost:3000](http://localhost:3000) in your browser to access the application.

---

## Development

If you want to run the application locally without Docker, follow these steps:

1. **Install Dependencies**: Run `npm install` to install all the necessary packages.

    ```bash
    npm install
    ```

2. **Run the Development Server**: Use `npm start` to start the development server.

    ```bash
    npm start
    ```

3. Visit [http://localhost:3000](http://localhost:3000) to view the application in your browser.

## Notes

- Make sure the backend is also up and running on `http://localhost:8000` as the frontend makes requests to this endpoint.
- The frontend provides two main functionalities:
  - **User Authentication**: Users can register as admin or regular users and log in to receive a JWT token.
  - **Document Upload & Query**: Admins can upload documents, and users can query the system based on these documents.

Feel free to modify and enhance the application as per your requirements!
