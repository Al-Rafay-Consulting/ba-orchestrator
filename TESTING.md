# BA Engine Orchestrator - Testing Guide

## Quick Start Testing

### 1. Health Check (Should work immediately)

**Using PowerShell:**
```powershell
$response = Invoke-WebRequest -Uri "http://localhost:8000/api/health" -Method GET
Write-Host $response.Content
```

**Using cURL:**
```bash
curl -X GET http://localhost:8000/api/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-06-23T18:30:00.000000",
  "service": "BA Engine Orchestrator",
  "version": "0.1.0"
}
```

---

### 2. Generate SRS (Main Feature - Requires Gemini API Key in .env)

**Using PowerShell:**
```powershell
$body = @{
    client_request = "We need a system where customers can book appointments online, get reminders, and the admin team can manage bookings. It should be simple, mobile-friendly, and maybe include reports later."
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "http://localhost:8000/api/generate-srs" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body

$response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 10 | Write-Host
```

**Using cURL:**
```bash
curl -X POST http://localhost:8000/api/generate-srs \
  -H "Content-Type: application/json" \
  -d '{
    "client_request": "We need a system where customers can book appointments online, get reminders, and the admin team can manage bookings."
  }'
```

---

### 3. Access Interactive API Documentation

FastAPI auto-generates beautiful API documentation. Open in browser:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

### 4. Test Data

Use the sample input from `samples/input_example.txt`:

```
We need a system where customers can book appointments online, get reminders, and the admin team can manage bookings. It should be simple, mobile-friendly, and maybe include reports later.
```

Expected output structure is in `samples/output_example.json`

---

## Troubleshooting

### API Key Error

**Error:** `GEMINI_API_KEY not set!`

**Solution:**
1. Make sure you updated `.env` file
2. Add your actual API key from https://aistudio.google.com/
3. Restart the server

### Connection Refused

**Error:** `Failed to connect to http://localhost:8000`

**Solution:**
1. Check if server is running (you should see "Uvicorn running on" message)
2. If not running, execute in terminal:
   ```
   cd d:\BA-Orchestrator
   .\venv\Scripts\python -m uvicorn src.main:app --reload
   ```

### Unicode/Emoji Errors

These are harmless - they appear during startup/logging on Windows but don't affect functionality.

---

## Key Endpoints Summary

| Endpoint | Method | Purpose | Input |
|----------|--------|---------|-------|
| `/` | GET | API info | None |
| `/api/health` | GET | Health check | None |
| `/api/generate-srs` | POST | Generate SRS | `{client_request: string}` |
| `/api/validate-srs` | POST | Validate SRS JSON | SRS object |
| `/docs` | GET | Swagger UI | None |
| `/redoc` | GET | ReDoc | None |

---

## Success Criteria

✓ Server starts without errors
✓ Health endpoint responds with 200
✓ API documentation is accessible at /docs
✓ generate-srs endpoint returns valid JSON
✓ JSON matches expected SRS schema

