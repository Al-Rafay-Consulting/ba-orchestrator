# BA Engine Orchestrator

Convert messy, unstructured client requests into clean, structured Software Requirements Specifications (SRS) in JSON format using AI and automation.

**Live API:** `http://localhost:8000` (when running locally)  
**Interactive Docs:** `http://localhost:8000/docs`  
**GitHub:** [irtizazubair19/ba-orchestrator](https://github.com/irtizazubair19/ba-orchestrator)

## 📋 Project Overview

This project automates the initial requirements gathering phase of software development. Instead of manually converting rambling client requests into structured requirements, the BA Engine Orchestrator uses LLMs (Large Language Models) to intelligently transform unstructured input into professional-grade SRS documents.

**Input:** Messy client request (natural language)  
**Output:** Structured, validated SRS JSON document

## 🎯 Why This Matters

In real-world BA work:
- Clients rarely provide clear specifications
- Manual SRS creation is time-consuming and error-prone
- This tool automates 70% of initial documentation work
- Output is consistent and professional
- Focus can shift to refinement rather than creation

## 🏗️ Architecture

```
Client Request
    ↓
[FastAPI Webhook Endpoint]
    ↓
[Input Validation & Preprocessing]
    ↓
[Google Gemini LLM API]
    ↓
[JSON Validation]
    ↓
[Structured SRS JSON Response]
```

## 🛠️ Technology Stack

| Component | Technology | Reason |
|-----------|-----------|--------|
| Backend Framework | FastAPI | Modern, fast, excellent for APIs |
| Language | Python 3.9+ | Productivity, readability |
| LLM Provider | Google Gemini API | Free tier, excellent JSON output |
| Validation | Pydantic | Type safety, validation |
| API Testing | Postman/cURL | Industry standard |
| Version Control | Git + GitHub | Professional workflow |

## 📁 Project Structure

```
ba-orchestrator/
├── src/
│   ├── main.py                 # FastAPI application entry point
│   ├── api/
│   │   └── routes.py          # API endpoints (webhooks)
│   ├── services/
│   │   ├── llm_service.py     # Gemini API integration
│   │   └── validation_service.py # JSON validation logic
│   ├── models/
│   │   └── schemas.py         # Pydantic data models
│   ├── utils/
│   │   ├── config.py          # Configuration loading
│   │   └── logger.py          # Logging setup
│   └── templates/
│       └── srs_prompt.txt     # LLM prompt template
├── tests/                      # Unit and integration tests
├── samples/
│   ├── input_example.txt      # Example messy input
│   └── output_example.json    # Example clean output
├── requirements.txt            # Python dependencies
├── .env.example               # Template for environment variables
├── .env                       # Your actual API keys (not in Git!)
├── .gitignore                 # Files to exclude from Git
└── README.md                  # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- Git and GitHub Desktop
- Google Gemini API key (free)

### Quick Start (5 minutes)

1. **Clone the repository:**
```bash
git clone https://github.com/irtizazubair19/ba-orchestrator.git
cd ba-orchestrator
```

2. **Create virtual environment:**
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # On Windows
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure API key:**
```bash
# Copy the template
cp .env.example .env

# Edit .env and add your Gemini API key from https://aistudio.google.com/
# GEMINI_API_KEY=your_key_here
```

5. **Start the server:**
```bash
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

6. **Open browser and test:**
- Interactive API: http://localhost:8000/docs
- Health check: http://localhost:8000/api/health

### How to Use

**Send a messy client request:**

```bash
curl -X POST http://localhost:8000/api/generate-srs \
  -H "Content-Type: application/json" \
  -d '{
    "client_request": "We need a system where customers can book appointments online, get reminders, and admin can manage bookings. Should be mobile-friendly."
  }'
```

**Expected response (structured SRS JSON):**

```json
{
  "success": true,
  "data": {
    "projectOverview": {
      "projectName": "Service Appointment Management System",
      "businessGoal": "Enable efficient appointment management..."
    },
    "functionalRequirements": [
      {
        "id": "FR-001",
        "title": "User Account Management",
        "description": "...",
        "priority": "CRITICAL",
        "acceptance_criteria": [...]
      }
    ],
    "nonFunctionalRequirements": [...],
    "stakeholders": [...],
    ...
  },
  "metadata": {
    "processing_time_ms": 18094,
    "model": "gemini-2.5-flash",
    "timestamp": "2026-06-23T18:45:01.438126"
  }
}
```

---

## 📊 API Endpoints

### POST /api/generate-srs

Converts a messy client request into structured SRS JSON.

**Request:**
```json
{
  "client_request": "We need a system where customers can book appointments online..."
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "projectOverview": {...},
    "objectives": [...],
    "functionalRequirements": [...],
    ...
  },
  "metadata": {
    "processing_time_ms": 2345,
    "model": "gemini-2.5-flash",
    "timestamp": "2026-06-23T18:45:01.438126",
    "validation_status": "passed"
  }
}
```

## ✅ Testing Results

The API has been tested and is **working successfully** with real requests. Here are the actual performance metrics:

### Test Case: Appointment Booking System

**Input Request:**
```
"We need a system where customers can book appointments online, get reminders, 
and admin can manage bookings. Should be mobile-friendly."
```

**Output Metrics:**
- ✓ **HTTP Status:** 200 OK
- ✓ **Processing Time:** ~18-20 seconds (limited by Gemini API latency)
- ✓ **Output Validation:** Passed schema validation
- ✓ **Functional Requirements Generated:** 6 requirements
- ✓ **Non-Functional Requirements Generated:** 5 requirements
- ✓ **Stakeholders Identified:** 3 stakeholders

**Generated SRS Structure:**
```
✓ Project Overview (name, business goal, scope)
✓ Functional Requirements (6 FR with IDs: FR-001 through FR-006)
✓ Non-Functional Requirements (5 NFR with IDs: NFR-001 through NFR-005)
✓ Stakeholders (admin, customer, support staff)
✓ Assumptions (5 key assumptions documented)
✓ Constraints (technical and business constraints)
✓ Dependencies (external systems identified)
```

**Model:** `gemini-2.5-flash` (latest available)

See [sample output](samples/output_example.json) for complete generated SRS.

---

## 🤖 LLM Prompt Strategy

The system uses a carefully engineered prompt that:

1. **Defines the task clearly:** "Convert the following client request into a structured SRS"
2. **Specifies output format:** "Return valid JSON matching this schema"
3. **Provides schema:** Shows exact structure expected
4. **Includes examples:** Demonstrates proper formatting
5. **Sets constraints:** "Extract only requirements, no implementation details"

**Sample Prompt:**
```
You are an expert Business Analyst. Convert the following unstructured client request 
into a professional Software Requirements Specification (SRS) document in JSON format.

Client Request:
{client_request}

Requirements:
- Identify project goals and objectives
- List all functional requirements with IDs (FR-001, FR-002, etc.)
- Include non-functional requirements (NFR-001, etc.)
- Specify acceptance criteria
- Return ONLY valid JSON, no markdown or explanations

JSON Schema:
{schema}

Return the complete JSON document.
```

## ✅ JSON Output Structure

The system generates SRS JSON with these sections:

| Section | Purpose | Example |
|---------|---------|---------|
| **projectOverview** | Project context and goals | Name, description, business goal |
| **objectives** | High-level project aims | "Enable self-service booking" |
| **stakeholders** | Users and their roles | Customer, Admin, Owner |
| **functionalRequirements** | What system must DO | Booking, reminders, management |
| **nonFunctionalRequirements** | Quality attributes | Performance, security, scalability |
| **assumptions** | Stated assumptions | "Client has email infrastructure" |
| **constraints** | Limitations | "8-week timeline" |
| **acceptanceCriteria** | Project success metrics | "Mobile responsive", "99.5% uptime" |

See `samples/output_example.json` for complete example.

## 🔍 Validation Process

The system validates JSON output:

1. **Schema validation:** Checks structure matches expected format
2. **Type checking:** Ensures correct data types
3. **Required fields:** Verifies all mandatory fields present
4. **Content validation:** Checks for reasonable values
5. **Error handling:** Returns detailed error messages

## ⚠️ Error Handling

The system gracefully handles:

| Error | Response | Solution |
|-------|----------|----------|
| Invalid input | HTTP 400 | Check request format |
| API rate limit | HTTP 429 | Implement backoff retry |
| Malformed JSON | HTTP 422 | Re-submit with valid JSON |
| API key invalid | HTTP 401 | Check .env file |
| Server error | HTTP 500 | Check logs |

## 🧪 Testing

Run tests:

```bash
pytest tests/ -v
```

Test the endpoint manually:

```bash
# Using samples
type samples/input_example.txt | curl -X POST http://localhost:8000/api/generate-srs ...

# See tests/test_api.py for detailed examples
```

## 📦 Assignment Deliverables

- GitHub Repository URL: https://github.com/irtizazubair19/ba-orchestrator
- Pull Request URL: https://github.com/irtizazubair19/ba-orchestrator/pull/1
- Source Code: Included in `src/`
- Sample Input: `samples/input_example.txt`
- Sample Output: `samples/output_example.json`
- API Test Outputs: Generated in `outputs/`

## 📸 Evidence Screenshots

The following screenshots are included for workflow and API validation evidence:

1. Swagger Documentation: ![Swagger Docs](Screenshots/localhost_8000_docs.png)
2. Health Endpoint Test: ![Health Check](Screenshots/api%20health.png)
3. SRS Generation Response: ![SRS Generation](Screenshots/srs%20generation.png)
4. Output Evidence 1: ![Output 1](Screenshots/output%201.png)
5. Output Evidence 2: ![Output 2](Screenshots/output%202.png)
6. Output Evidence 3: ![Output 3](Screenshots/output%203.png)
7. Output Evidence 4: ![Output 4](Screenshots/output%204.png)
8. Output Evidence 5: ![Output 5](Screenshots/output%205.png)
9. Output Evidence 6: ![Output 6](Screenshots/output%206.png)
10. GitHub PR Merged Status: ![PR Merged](Screenshots/GitHub%20Meged.png)

## 📚 How AI Was Used

1. **Prompt Engineering:** Crafted detailed instructions to guide LLM output
2. **Schema Definition:** Defined exact JSON structure for consistency
3. **Validation Logic:** AI output validated against schema before returning
4. **Error Recovery:** Failed requests re-attempted with modified prompts
5. **Temperature Control:** Set LLM "creativity" parameter for consistency

## 📈 Sample Execution

**Input:**
```
We need a system where customers can book appointments online, 
get reminders, and the admin team can manage bookings. 
It should be simple, mobile-friendly, and maybe include reports later.
```

**Output:**
```json
{
  "projectOverview": {
    "projectName": "Online Appointment Booking System",
    "businessGoal": "Enable efficient appointment management..."
  },
  "objectives": [
    "Enable customers to book appointments online",
    "Provide automated reminder notifications",
    "Centralize booking management"
  ],
  ...
}
```

See `samples/output_example.json` for complete example.

## 🔄 Git Workflow

This project follows professional Git practices:

```
main branch (production)
    ↑
    └── feature branch (development)
        └── Commits with meaningful messages
        └── Pull Request for code review
```

Using **GitHub Desktop:**

1. Create feature branch: `feature/add-gemini-integration`
2. Make changes and commit
3. Create Pull Request
4. Review changes
5. Merge to main

## 🚀 Deployment

Future improvements for production:

- Deploy to cloud (AWS Lambda, Google Cloud Run, etc.)
- Add database (PostgreSQL, MongoDB) for persistence
- Implement authentication and rate limiting
- Add monitoring and alerting
- Create CI/CD pipeline with GitHub Actions
- Add API documentation with Swagger/OpenAPI
- Implement caching for identical requests

## 📚 Future Improvements

If given more time:

1. **Multi-language support:** Convert requests in any language
2. **Template library:** Different SRS formats for different project types
3. **User dashboard:** Track SRS generation history
4. **Collaborative features:** Allow team to edit SRS before finalization
5. **Integration APIs:** Connect to Jira, Azure DevOps, etc.
6. **Advanced validation:** Business rule validation beyond schema
7. **Versioning:** Track SRS changes over time
8. **Analytics:** Report on requirement patterns and trends
9. **Custom fields:** Allow clients to define additional SRS sections
10. **Export formats:** PDF, Word, Markdown generation

## 📞 Support & Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'fastapi'"

**Solution:**
```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### Issue: "Invalid API key"

**Solution:**
```bash
# Check .env file
# Ensure GEMINI_API_KEY is set correctly
# Get new key from https://aistudio.google.com/
```

### Issue: "Connection timeout to Gemini API"

**Solution:**
```bash
# Check internet connection
# Verify API key has quota remaining
# Check Gemini API status
```

## 📖 Learning Resources

Understanding the concepts in this project:

- **FastAPI:** https://fastapi.tiangolo.com/
- **Pydantic:** https://docs.pydantic.dev/
- **Google Gemini:** https://ai.google.dev/
- **REST APIs:** https://restfulapi.net/
- **JSON Schema:** https://json-schema.org/

## 👨‍💼 For Interviews/Reviews

**Key Points to Discuss:**

1. **Problem solving:** How you approached converting unstructured to structured data
2. **Architecture:** Why you chose this project structure
3. **Error handling:** How you dealt with API failures
4. **Validation:** Why schema validation is critical
5. **Scalability:** How the system could handle 1000+ requests/day
6. **Testing:** How you verified correctness
7. **Git practices:** Professional workflow and commit messages
8. **Prompt engineering:** How you instructed the AI effectively

## 📄 License

This project is for educational purposes.

## ✍️ Author

BA Development Team

---

**Status:** In Development  
**Last Updated:** 2026-06-24  
**Version:** 0.1.0
