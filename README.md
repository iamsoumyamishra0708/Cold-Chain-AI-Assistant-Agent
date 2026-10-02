Cold Chain Logistics - AI Assistant
This project transforms a legacy cold-chain logistics database into an autonomous AI dispatch console. Powered by a LangGraph ReAct agent, the system integrates spatial SQL telemetry, live weather APIs, and Vector RAG compliance rulebooks to proactively anticipate and resolve cargo spoilage risks before they occur. Built for enterprise reliability, it features an invisible, immutable SQL audit trail and is fully deployed to a live AWS EC2 environment using automated CI/CD pipelines.

🚀 Key Features
Autonomous ReAct Agent Brain: A LangGraph-powered orchestrator that autonomously decides when to utilize tools, query databases, or read RAG documents to solve complex dispatch scenarios.

Structured & Unstructured Data Fusion: Seamlessly bridges Structured Data (SQL Server telemetry) with Unstructured Data (Vector RAG compliance rulebooks) in a single, continuous workflow.

Geospatial NLP Translation: Instructs an LLM to dynamically translate natural language geographic and location-based terms into precise GPS bounding-box SQL queries.

Enterprise-Grade Audit Trail: Engineered with an invisible, immutable SQL logging system that permanently records every LLM thought process, tool execution, and decision for strict compliance and enterprise trust.

Automated CI/CD Pipeline: Fully transitioned from local hosting to production using GitHub Actions to deploy the application securely to a live AWS EC2 instance.

🏗️ Architecture & Tech Stack
AI Framework: LangGraph, ReAct Agent Architecture, Vector RAG

Databases: SQL Server (Spatial SQL / GPS Bounding), Vector Database (for Rulebooks)

External APIs: Live Weather APIs

Infrastructure: AWS EC2

DevOps: GitHub Actions, CI/CD, Immutable SQL Logging

⚙️ Prerequisites
Before running this project locally, ensure you have the following installed and configured:

Python 3.9+

SQL Server (with spatial data types enabled)

AWS CLI configured with appropriate EC2 access permissions

API Keys for the chosen LLM provider, Weather API, and Vector DB

🛠️ Local Installation & Setup
Clone the Repository

Bash
git clone https://github.com/your-organization/cold-chain-ai-assistant.git
cd cold-chain-ai-assistant
Set Up a Virtual Environment

Bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
Install Dependencies

Bash
pip install -r requirements.txt
Environment Variables
Create a .env file in the root directory and add your credentials:

Code snippet
LLM_API_KEY=your_api_key_here
WEATHER_API_KEY=your_weather_api_key
DB_CONNECTION_STRING=your_sql_server_connection_string
VECTOR_DB_URL=your_vector_db_url
Run the Application Locally

Bash
python main.py
🌐 Deployment (CI/CD)
This project utilizes GitHub Actions for continuous integration and continuous deployment.

Any push to the main branch automatically triggers the deployment pipeline:

Lints and tests the Python codebase.

Authenticates securely with AWS using GitHub Secrets.

Pulls the latest code to the designated AWS EC2 instance.

Restarts the LangGraph ReAct agent service.

Note: Ensure your GitHub repository has the necessary AWS deployment credentials stored securely in Settings > Secrets and variables > Actions.

🔒 Audit & Compliance Logging
A core feature of this application is its Invisible SQL Audit Trail. You do not need to manually configure logging for standard AI operations. The system intercepts all LangGraph events—including tool calls, API responses, RAG retrieval context, and step-by-step reasoning—and permanently writes them to an immutable SQL table. This ensures complete traceability for regulatory compliance in cold-chain handling.
