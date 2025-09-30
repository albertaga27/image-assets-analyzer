import os
import base64
import json
from typing import List, Dict, Any, Optional
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AzureOpenAIService:
    """Azure OpenAI service for building risk analysis"""
    
    def __init__(self):
        # Initialize Azure OpenAI client with configuration from .env
        self.endpoint = os.getenv('4.1_OPENAI_ENDPOINT')
        self.api_key = os.getenv('4.1_OPENAI_API_KEY')
        self.deployment = os.getenv('4.1_OPENAI_DEPLOYMENT_NAME')
        self.api_version = "2024-04-01-preview"
        
        if not all([self.endpoint, self.api_key, self.deployment]):
            raise ValueError('Missing Azure OpenAI configuration. Please check your .env file.')
        
        self.client = AzureOpenAI(
            azure_endpoint=self.endpoint,
            api_key=self.api_key,
            api_version=self.api_version
        )
        
        print(f"Azure OpenAI Service initialized with endpoint: {self.endpoint}")
    
    async def analyze_building_risks(self, image_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyzes building images for insurance risk assessment
        
        Args:
            image_data: List of image objects with {base64, type, name, size?}
            
        Returns:
            Risk assessment results as dictionary
        """
        try:
            # Normalize input to array format
            images = image_data if isinstance(image_data, list) else [image_data]
            image_count = len(images)
            
            print(f"🔍 Analyzing {image_count} image(s) for building risk assessment")
            
            system_prompt = self._get_system_prompt(image_count)
            user_prompt = self._get_user_prompt(image_count)
            
            # Prepare the user message content with text and images
            user_content = [{"type": "text", "text": user_prompt}]
            
            # Add all images to the content
            for img in images:
                user_content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{img['type']};base64,{img['base64']}",
                        "detail": "high"
                    }
                })
            
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                max_tokens=3000 if image_count > 1 else 2000,
                temperature=0.3,
                model=self.deployment
            )
            
            if hasattr(response, 'error') and response.error:
                raise Exception(f"Azure OpenAI API Error: {response.error}")
            
            content = response.choices[0].message.content
            if not content:
                raise Exception('No response content received from Azure OpenAI')
            
            # Try to parse JSON response
            try:
                json_match = content[content.find('{'):content.rfind('}')+1]
                if json_match:
                    return json.loads(json_match)
                else:
                    return self._create_fallback_response(content, image_count)
            except json.JSONDecodeError as parse_error:
                print(f'Failed to parse JSON response: {parse_error}')
                return self._create_fallback_response(content, image_count)
                
        except Exception as error:
            print(f'Error analyzing building risks: {error}')
            raise Exception(f"Risk analysis failed: {str(error)}")
    
    def _get_system_prompt(self, image_count: int) -> str:
        """Generate system prompt based on number of images"""
        return f"""You are an expert insurance underwriter specializing in building risk assessment. 
You are analyzing {image_count} image{'s' if image_count > 1 else ''} of the same building from different angles/perspectives to provide a comprehensive risk assessment.

{'Consider all images together to form a complete picture of the building and its risks. Look for consistent patterns across images and note any contradictions or additional context provided by multiple viewpoints.' if image_count > 1 else 'Analyze the provided building image and identify potential risks.'}

Focus on these key risk categories:

**Fire & Life Safety Risks:**
- Emergency exits (number, location, width, accessibility)
- Exit routes and egress paths
- Fire suppression systems (sprinklers, extinguishers)
- Fire-resistant materials and construction
- Smoke detection systems

**Structural & Construction Risks:**
- Building age and condition indicators
- Construction materials (wood, steel, concrete)
- Roof condition and materials
- Foundation and structural integrity
- Seismic vulnerabilities

**Security Risks:**
- Access control and entry points
- Lighting adequacy
- Perimeter security
- Surveillance coverage

**Water Damage & Flood Risks:**
- Proximity to water sources
- Drainage systems
- Below-grade areas
- Plumbing condition

**Occupancy & Usage Risks:**
- Occupancy load vs exit capacity
- Hazardous activities or storage
- Mixed-use considerations
- Accessibility compliance

**Environmental & Location Risks:**
- Surrounding hazards
- Natural disaster exposure
- Utility infrastructure proximity

Provide your analysis in the following JSON format:
{{
  "overall_risk_level": "LOW|MEDIUM|HIGH",
  "risk_score": 1-10,
  "images_analyzed": {image_count},
  "key_findings": ["finding1", "finding2", "finding3"],
  "detailed_assessment": {{
    "fire_safety": {{
      "risk_level": "LOW|MEDIUM|HIGH",
      "observations": ["observation1", "observation2"],
      "concerns": ["concern1", "concern2"]
    }},
    "structural": {{
      "risk_level": "LOW|MEDIUM|HIGH",
      "observations": ["observation1", "observation2"],
      "concerns": ["concern1", "concern2"]
    }},
    "security": {{
      "risk_level": "LOW|MEDIUM|HIGH",
      "observations": ["observation1", "observation2"],
      "concerns": ["concern1", "concern2"]
    }},
    "water_damage": {{
      "risk_level": "LOW|MEDIUM|HIGH",
      "observations": ["observation1", "observation2"],
      "concerns": ["concern1", "concern2"]
    }},
    "environmental": {{
      "risk_level": "LOW|MEDIUM|HIGH",
      "observations": ["observation1", "observation2"],
      "concerns": ["concern1", "concern2"]
    }}
  }},
  "recommendations": ["recommendation1", "recommendation2", "recommendation3"],
  "additional_information_needed": ["info1", "info2"],
  "image_analysis_summary": "{'Summary of what was observed across all images and how they complement each other' if image_count > 1 else 'Summary of the single image analysis'}"
}}

Be thorough but realistic in your assessment. Only identify risks that are clearly visible or reasonably inferred from the images. {'When analyzing multiple images, provide insights that benefit from having multiple perspectives of the same building.' if image_count > 1 else ''}"""
    
    def _get_user_prompt(self, image_count: int) -> str:
        """Generate user prompt based on number of images"""
        if image_count > 1:
            return f"Please analyze these {image_count} building images for comprehensive insurance underwriting risk assessment. These images show different angles and aspects of the same building. Provide a thorough evaluation considering all visible risk factors across all images."
        else:
            return "Please analyze this building image for insurance underwriting risk assessment. Provide a comprehensive evaluation of all visible risk factors."
    
    def _create_fallback_response(self, content: str, image_count: int) -> Dict[str, Any]:
        """Create fallback response when JSON parsing fails"""
        return {
            "overall_risk_level": "MEDIUM",
            "risk_score": 5,
            "images_analyzed": image_count,
            "key_findings": ["Analysis completed - see detailed response"],
            "raw_response": content,
            "detailed_assessment": {
                "fire_safety": {"risk_level": "MEDIUM", "observations": [], "concerns": []},
                "structural": {"risk_level": "MEDIUM", "observations": [], "concerns": []},
                "security": {"risk_level": "MEDIUM", "observations": [], "concerns": []},
                "water_damage": {"risk_level": "MEDIUM", "observations": [], "concerns": []},
                "environmental": {"risk_level": "MEDIUM", "observations": [], "concerns": []}
            },
            "recommendations": ["Review detailed analysis"],
            "additional_information_needed": [],
            "image_analysis_summary": f"Analysis of {image_count} building image{'s' if image_count > 1 else ''} completed"
        }
    
    async def health_check(self) -> bool:
        """
        Health check method to verify Azure OpenAI connectivity
        
        Returns:
            Connection status as boolean
        """
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Hello, please respond with 'OK' to confirm connectivity."}
                ],
                max_tokens=10,
                temperature=0,
                model=self.deployment
            )
            
            return 'OK' in (response.choices[0].message.content or '')
        except Exception as error:
            print(f'Azure OpenAI health check failed: {error}')
            return False