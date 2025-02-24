# Medical Q&A

This repository contains a web application for Medical Q&A . The frontend is built with React, and the backend is powered by FastAPI. 


## Tech Stack

- **Frontend**: React
- **Backend**: FastAPI
- **LLM**: llama3(Ollama)

## Setup Instructions

### Prerequisites

- [Python 3.10+](https://www.python.org/)
- [venv](https://docs.python.org/3/library/venv.html) (for creating virtual environments)

### Frontend Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/Mubashirshariq/Q-A_PDF_CHAT.git](https://github.com/Mubashirshariq/MEDIC_CHAT.git
    ```

2. Navigate to the `frontend` directory:
    ```sh
    cd frontend
    ```

3. Install the dependencies:
    ```sh
    npm install
    ```

4. Start the frontend development server:
    ```sh
    npm run dev
    ```

### Backend Setup
Now create one more terminal to run the backend
1. Navigate to the `backend` directory:
    ```sh
    cd backend
    ```

2. Create a virtual environment:
    ```sh
    python -m venv myenv
    ```

4. Activate the virtual environment:
    - On Windows:
        ```sh
        myenv\Scripts\activate
        ```
    - On macOS and Linux:
        ```sh
        source myenv/bin/activate
        ```

5. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

6. Run the FastAPI server:
    ```sh
     python -m app.main
    ```

## Usage
<img width="1457" alt="Screenshot 2025-02-24 at 2 50 56 PM" src="https://github.com/user-attachments/assets/2eb2642a-dce6-4010-8520-b9a32d6259ca" />

<img width="1446" alt="Screenshot 2025-02-24 at 2 51 09 PM" src="https://github.com/user-attachments/assets/c7d1879b-0221-4228-8193-107dc636185a" />

Once both the frontend and backend servers are running, you can access the application by navigating to `http://localhost:5173` in your web browser.
