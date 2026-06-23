"""
LLM Service - Handles Google Gemini API integration
Converts unstructured client requests to SRS JSON
"""

import json
from typing import Optional
import google.generativeai as genai
from src.utils.config import Config
from src.utils.logger import logger


class LLMService:
    """Service for interacting with Google Gemini API"""
    
    def __init__(self):
        """Initialize Gemini API client"""
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
        logger.info(f"[OK] Gemini API initialized with model: {Config.GEMINI_MODEL}")
    
    def generate_srs(self, client_request: str) -> Optional[dict]:
        """
        Convert messy client request to structured SRS JSON
        
        Args:
            client_request: Unstructured client requirements text
            
        Returns:
            Parsed SRS JSON dictionary or None if failed
        """
        try:
            logger.info(f"Processing client request: {client_request[:50]}...")
            
            # Build the prompt
            prompt = self._build_prompt(client_request)
            
            # Call Gemini API
            logger.info("Calling Gemini API...")
            response = self.model.generate_content(prompt)
            
            if not response.text:
                logger.error("Empty response from Gemini API")
                return None
            
            logger.info(f"Raw response received: {len(response.text)} chars")
            
            # Extract and parse JSON from response
            srs_json = self._extract_json(response.text)
            
            if srs_json:
                logger.info("[OK] SRS JSON extracted successfully")
                return srs_json
            else:
                logger.error("Failed to extract valid JSON from response")
                return None
                
        except Exception as e:
            logger.error(f"Error in LLM service: {str(e)}")
            return None
    
    def _build_prompt(self, client_request: str) -> str:
        """
        Build the prompt for Gemini API
        This is where we do prompt engineering!
        
        Args:
            client_request: The client's messy requirements
            
        Returns:
            Formatted prompt for LLM
        """
        
        srs_schema = {
            "projectOverview": {
                "projectName": "string",
                "clientDescription": "original_messy_text",
                "cleanDescription": "refined_professional_description",
                "businessGoal": "clear_business_objective"
            },
            "objectives": ["objective1", "objective2"],
            "stakeholders": [
                {"role": "User Role", "description": "Description"}
            ],
            "functionalRequirements": [
                {
                    "id": "FR-001",
                    "title": "Requirement title",
                    "description": "Detailed description",
                    "priority": "CRITICAL|HIGH|MEDIUM|LOW",
                    "acceptance_criteria": ["Criteria 1", "Criteria 2"]
                }
            ],
            "nonFunctionalRequirements": [
                {
                    "id": "NFR-001",
                    "title": "NFR title",
                    "type": "Performance|Security|Scalability|etc",
                    "description": "Description"
                }
            ],
            "assumptions": ["assumption1", "assumption2"],
            "constraints": ["constraint1"],
            "acceptanceCriteria": ["criteria1", "criteria2"]
        }
        
        prompt = f"""You are an expert Business Analyst with 10+ years of experience.

Your task: Convert the following MESSY, UNSTRUCTURED client request into a PROFESSIONAL, STRUCTURED Software Requirements Specification (SRS) document in JSON format.

IMPORTANT INSTRUCTIONS:
1. Extract and infer ALL requirements (explicit and implicit) from the client request
2. Organize requirements into Functional (FR-XXX) and Non-Functional (NFR-XXX) categories
3. Identify all stakeholders/users
4. Create clear, professional objectives
5. Generate realistic assumptions and constraints
6. Return ONLY valid JSON - no markdown, no explanations
7. Ensure ALL string values are properly escaped for JSON
8. Make reasonable business assumptions where details are missing
9. Be comprehensive but concise

CLIENT REQUEST:
"{client_request}"

REQUIRED OUTPUT JSON SCHEMA (follow this exactly):
{json.dumps(srs_schema, indent=2)}

CRITICAL REQUIREMENTS FOR YOUR OUTPUT:
- Return ONLY valid JSON that can be parsed by Python's json.loads()
- projectName must be a clear, professional name (not generic)
- Include at least 4-6 functional requirements with proper IDs
- Include at least 3-5 non-functional requirements
- All acceptance_criteria should be testable and measurable
- Priority levels must be: CRITICAL, HIGH, MEDIUM, or LOW
- Functional requirements should focus on WHAT the system does
- Non-functional requirements should focus on HOW WELL it does it
- Assumptions should be realistic based on context
- Do NOT include any markdown formatting, code blocks, or explanations
- Do NOT wrap the JSON in triple backticks

Now generate the complete SRS JSON document:"""
        
        return prompt
    
    def _extract_json(self, text: str) -> Optional[dict]:
        """
        Extract JSON from LLM response
        Handles cases where LLM might include markdown or explanations
        
        Args:
            text: Raw response text from LLM
            
        Returns:
            Parsed JSON dictionary or None
        """
        try:
            # First, try direct parsing
            return json.loads(text)
        except json.JSONDecodeError:
            # If that fails, try to find JSON in the text
            import re
            
            # Look for JSON object (starts with { and ends with })
            json_match = re.search(r'\{[\s\S]*\}', text)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except json.JSONDecodeError:
                    pass
            
            logger.error("Could not extract valid JSON from response")
            return None
