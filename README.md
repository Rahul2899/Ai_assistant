# AI-PHASE: Intelligent IT Operations Assistant 🤖

## Project Overview
AI-PHASE is an advanced AI-powered IT operations management system designed to provide intelligent incident resolution, system monitoring, and comprehensive IT support.

## 📂 Project Structure

### Main Python Files
1. **`main.py`**
   - FastAPI backend with endpoints for:
     - System overview
     - Incident resolution
     - Incident documentation

2. **`app.py`**
   - Streamlit frontend application
   - Provides interactive UI for:
     - System dashboard
     - Incident resolution
     - Solution tracking

3. **`incident_resolution.py`**
   - AI-powered incident resolution logic
   - Generates resolution steps using LangChain and OpenAI
   - Provides alternative solution generation

4. **`system_overview.py`**
   - Simulates system health monitoring
   - Generates AI-powered system status summaries
   - Tracks server and service statuses

5. **`documentation.py`**
   - Handles incident documentation
   - Creates markdown reports
   - Saves incident details with timestamps

6. **`config.py`**
   - Manages configuration settings
   - Initializes OpenAI Language Model
   - Loads environment variables

7. **`requirements.txt`**
   - Lists all project dependencies
   - Includes Streamlit, LangChain, OpenAI, and other required packages

## 🚀 Setup and Installation

### Prerequisites
- Python 3.8+
- OpenAI API Key

### Installation Steps
```bash
# Clone the repository
git clone https://github.com/yourusername/ai-phase-ops-assistant.git
cd ai-phase-ops-assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

# Set up OpenAI API Key
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
