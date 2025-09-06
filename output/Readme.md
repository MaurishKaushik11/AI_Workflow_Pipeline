# AI Workflow Pipeline

A modular AI workflow pipeline that allows running various AI tasks with configurable settings. This project is designed for ease of evaluation and extensibility.

## Features

- Modular pipeline structure
- Supports multiple AI/ML tasks
- Configurable via environment variables
- Clean codebase with reusable modules

## Prerequisites

- Python 3.10+  
- Virtual environment (recommended)  
- Required Python packages: see `requirements.txt`

## Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/MaurishKaushik11/AI_Workflow_Pipeline.git
cd AI_Workflow_Pipeline
Create a virtual environment

bash
Copy code
python -m venv .venv
# Activate it
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
Install dependencies

bash
Copy code
pip install -r requirements.txt
Set up environment variables

Copy the template .env.example to .env:

bash
Copy code
copy .env.example .env   # Windows
cp .env.example .env     # Linux/Mac
Fill in your own credentials and API keys in .env

Note: Do not commit your .env or any secret files to GitHub.

Run the pipeline

bash
Copy code
python main.py
Project Structure
bash
Copy code
AI_Workflow_Pipeline/
│
├── credentials/           # Google Cloud service accounts (ignored by Git)
├── modules/               # Pipeline modules
├── .venv/                 # Python virtual environment (ignored by Git)
├── .gitignore
├── .env.example           # Template for environment variables
├── main.py                # Entry point
├── requirements.txt
└── README.md
