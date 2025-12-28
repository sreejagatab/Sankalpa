

import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from agents.base import BaseAgent
from typing import Dict, Any

class TextTranslatorAgent(BaseAgent):
    """
    A simple text translation agent
    
    Category: utility
    """
    
    def __init__(self, name="text_translator", memory=None):
        super().__init__(name, memory)
        self.category = "utility"
        self.description = "A simple text translation agent"
    
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent with the given input data
        
        Args:
            input_data: Dictionary containing input parameters
            
        Returns:
            Dictionary containing agent output
        """
        # Validate inputs
        for input_field in [{'name': 'text', 'type': 'string'}, {'name': 'target_language', 'type': 'string'}]:
            field_name = input_field["name"]
            if field_name not in input_data:
                return {
                    "error": f"Missing required input: {field_name}",
                    "status": "error"
                }
        
        # Agent implementation
        
        text = input_data.get("text", "")
        target_language = input_data.get("target_language", "spanish").lower()
        
        if not text:
            return {"error": "No text provided", "status": "error"}
            
        # Simple word translations (just for demonstration)
        translations = {
            "spanish": {
                "hello": "hola",
                "world": "mundo",
                "good": "bueno",
                "morning": "mañana",
                "evening": "tarde",
                "welcome": "bienvenido",
                "thank you": "gracias",
                "goodbye": "adiós"
            },
            "french": {
                "hello": "bonjour",
                "world": "monde",
                "good": "bon",
                "morning": "matin",
                "evening": "soir",
                "welcome": "bienvenue",
                "thank you": "merci",
                "goodbye": "au revoir"
            },
            "german": {
                "hello": "hallo",
                "world": "welt",
                "good": "gut",
                "morning": "morgen",
                "evening": "abend",
                "welcome": "willkommen",
                "thank you": "danke",
                "goodbye": "auf wiedersehen"
            }
        }
        
        # Check if the target language is supported
        if target_language not in translations:
            return {"error": f"Unsupported language: {target_language}", "status": "error"}
            
        # Split text into words and translate each word if possible
        words = text.lower().split()
        translated_words = []
        
        for word in words:
            if word in translations[target_language]:
                translated_words.append(translations[target_language][word])
            else:
                translated_words.append(word)  # Keep original if no translation
        
        translated_text = " ".join(translated_words)
        
        result = {
            "original_text": text,
            "translated_text": translated_text,
            "target_language": target_language
        }
        
        return result
    
        
        return {
            "message": "text_translator executed successfully",
            "status": "success",
            "data": result
        }
