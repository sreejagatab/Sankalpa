import requests
import json

# Define a new text translator agent
agent_spec = {
    "name": "text_translator",
    "description": "A simple text translation agent",
    "category": "utility",
    "logic": """
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
    """,
    "inputs": [
        {"name": "text", "type": "string"},
        {"name": "target_language", "type": "string"}
    ],
    "outputs": [
        {"name": "translated_text", "type": "string"},
        {"name": "target_language", "type": "string"}
    ]
}

print("Creating text translator agent...")
response = requests.post('http://localhost:8080/api/create-agent', json=agent_spec)
print(f"Status: {response.status_code}")
print(json.dumps(response.json(), indent=2))

# If successful, test the new agent
if response.status_code == 200:
    print("\nTesting the translator agent...")
    
    test_data = {
        "text": "hello world thank you",
        "target_language": "spanish"
    }
    
    test_response = requests.post(
        'http://localhost:8080/api/agents/execute/text_translator', 
        json=test_data
    )
    
    print(f"Status: {test_response.status_code}")
    print(json.dumps(test_response.json(), indent=2))