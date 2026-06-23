"""
Validation Service - Validates SRS JSON against schema
"""

import json
from typing import Optional, Tuple
from jsonschema import validate, ValidationError
from src.utils.logger import logger


class ValidationService:
    """Service for validating SRS JSON output"""
    
    @staticmethod
    def get_srs_schema() -> dict:
        """
        Get the JSON schema that SRS output must conform to
        This ensures consistent and valid output
        
        Returns:
            JSON schema dictionary
        """
        return {
            "type": "object",
            "required": [
                "projectOverview",
                "objectives",
                "stakeholders",
                "functionalRequirements",
                "nonFunctionalRequirements",
                "assumptions",
                "acceptanceCriteria"
            ],
            "properties": {
                "projectOverview": {
                    "type": "object",
                    "required": ["projectName", "clientDescription", "cleanDescription", "businessGoal"],
                    "properties": {
                        "projectName": {"type": "string", "minLength": 3},
                        "clientDescription": {"type": "string", "minLength": 10},
                        "cleanDescription": {"type": "string", "minLength": 10},
                        "businessGoal": {"type": "string", "minLength": 10}
                    }
                },
                "objectives": {
                    "type": "array",
                    "minItems": 2,
                    "items": {"type": "string", "minLength": 10}
                },
                "stakeholders": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "type": "object",
                        "required": ["role", "description"],
                        "properties": {
                            "role": {"type": "string"},
                            "description": {"type": "string"}
                        }
                    }
                },
                "functionalRequirements": {
                    "type": "array",
                    "minItems": 2,
                    "items": {
                        "type": "object",
                        "required": ["id", "title", "description", "priority", "acceptance_criteria"],
                        "properties": {
                            "id": {"type": "string", "pattern": "^FR-\\d{3}$"},
                            "title": {"type": "string"},
                            "description": {"type": "string"},
                            "priority": {"type": "string", "enum": ["CRITICAL", "HIGH", "MEDIUM", "LOW"]},
                            "acceptance_criteria": {
                                "type": "array",
                                "items": {"type": "string"}
                            }
                        }
                    }
                },
                "nonFunctionalRequirements": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "type": "object",
                        "required": ["id", "title", "type", "description"],
                        "properties": {
                            "id": {"type": "string", "pattern": "^NFR-\\d{3}$"},
                            "title": {"type": "string"},
                            "type": {"type": "string"},
                            "description": {"type": "string"}
                        }
                    }
                },
                "assumptions": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "constraints": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "acceptanceCriteria": {
                    "type": "array",
                    "minItems": 1,
                    "items": {"type": "string"}
                }
            }
        }
    
    @staticmethod
    def validate_srs(srs_data: dict) -> Tuple[bool, Optional[str]]:
        """
        Validate SRS data against schema
        
        Args:
            srs_data: SRS dictionary to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            schema = ValidationService.get_srs_schema()
            validate(instance=srs_data, schema=schema)
            logger.info("[OK] SRS validation successful")
            return True, None
        except ValidationError as e:
            error_msg = f"Validation error: {e.message} at path {list(e.absolute_path)}"
            logger.error(f"[FAIL] {error_msg}")
            return False, error_msg
        except Exception as e:
            error_msg = f"Unexpected validation error: {str(e)}"
            logger.error(f"[FAIL] {error_msg}")
            return False, error_msg
    
    @staticmethod
    def validate_and_fix(srs_data: dict) -> Tuple[bool, dict, Optional[str]]:
        """
        Validate SRS and attempt to fix common issues
        
        Args:
            srs_data: SRS dictionary to validate
            
        Returns:
            Tuple of (is_valid, fixed_data, error_message)
        """
        # First validate
        is_valid, error = ValidationService.validate_srs(srs_data)
        
        if is_valid:
            return True, srs_data, None
        
        # Try to fix common issues
        logger.info("Attempting to fix common validation issues...")
        fixed_data = srs_data.copy()
        
        # Ensure constraints is a list if missing
        if "constraints" not in fixed_data:
            fixed_data["constraints"] = []
        
        # Re-validate
        is_valid, error = ValidationService.validate_srs(fixed_data)
        
        if is_valid:
            logger.info("[OK] Validation successful after fixes")
            return True, fixed_data, None
        else:
            return False, fixed_data, error
