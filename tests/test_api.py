"""
Basic tests for BA Engine Orchestrator
Run with: pytest tests/test_api.py -v
"""

import pytest
import json
from fastapi.testclient import TestClient
from src.main import app

# Create test client
client = TestClient(app)


class TestHealthCheck:
    """Test health check endpoint"""
    
    def test_health_check(self):
        """Verify API is healthy"""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data


class TestValidation:
    """Test validation endpoint"""
    
    def test_validate_srs_valid(self):
        """Test validation with valid SRS"""
        valid_srs = {
            "projectOverview": {
                "projectName": "Test Project",
                "clientDescription": "Client request here",
                "cleanDescription": "Clean description here",
                "businessGoal": "Business goal here"
            },
            "objectives": ["Objective 1", "Objective 2"],
            "stakeholders": [
                {"role": "User", "description": "End user of the system"}
            ],
            "functionalRequirements": [
                {
                    "id": "FR-001",
                    "title": "Test Feature",
                    "description": "Test feature description",
                    "priority": "HIGH",
                    "acceptance_criteria": ["Criteria 1"]
                }
            ],
            "nonFunctionalRequirements": [
                {
                    "id": "NFR-001",
                    "title": "Performance",
                    "type": "Performance",
                    "description": "Must be fast"
                }
            ],
            "assumptions": ["Assumption 1"],
            "acceptanceCriteria": ["Criteria 1"]
        }
        
        response = client.post("/api/validate-srs", json=valid_srs)
        assert response.status_code == 200
        data = response.json()
        assert data["is_valid"] == True


class TestRoot:
    """Test root endpoint"""
    
    def test_root_endpoint(self):
        """Verify root endpoint returns info"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "endpoints" in data
        assert "version" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
