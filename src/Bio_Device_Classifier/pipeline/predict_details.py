import json
import httpx


# Define the class definitions
class_definitions = {
    "Class A": "Low Risk. Simple, non-invasive.",
    "Class B": "Low to Moderate Risk. Limited duration, minimal invasiveness, and with additional regulatory controls",
    "Class C": "Moderate to High Risk. Invasive, prolonged contact, and devices needing premarket approval",
    "Class D": "High Risk. Implantable, life-sustaining, and devices needing strict regulatory controls."
}

# Define the API endpoint
url = "http://10.11.6.51:4000/api/generate"

def create_prompt(device_name, intended_use, device_class, class_definitions):
    """Generate the prompt string based on device details and class definitions."""
    class_description = class_definitions.get(device_class, "No definition available")
    prompt = (
        f"{device_name}, it is used for {intended_use}. "
        f"{device_class}: {class_description}. "
        "Why has this been classified as {device_class}? Describe more about the device. "
        "NOTE: If you do not have knowledge about this device, just repeat the input in response. "
        "Provide 3 precise bullet points. Answer without emotion."
    )
    return prompt

async def generate_response(device_name, intended_use, device_class):
    """Send a prompt to the API and get the generated response."""
    # Generate the prompt
    prompt = create_prompt(device_name, intended_use, device_class, class_definitions)
    
    # Define the payload for the API request
    payload = {
        "model": "medllama2",
        "prompt": prompt
    }
    
    # Send the asynchronous request
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, timeout=None)
    
    # Process the response
    response_text = ""

    for line in response.text.splitlines():
        if line:
            data = json.loads(line)
            if 'response' in data:
                response_text += data['response']
    
    return response_text
