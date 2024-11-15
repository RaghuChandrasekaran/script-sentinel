from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.prompts import PromptTemplate
import time
import yaml
import os
import json

class ModelHandler:
    def __init__(self):
        # Load config
        with open('config/config.yaml', 'r') as file:
            self.config = yaml.safe_load(file)
        
        # Store API key for reuse
        self.api_key = os.getenv('OPENROUTER_API_KEY', self.config.get('openrouter_api_key'))
    
    def analyze_script(self, script, model, technique):
        
        # Create a new client with the selected model
        self.client = ChatOpenAI(
            api_key=self.api_key,
            base_url="https://openrouter.ai/api/v1",
            model=self._get_model_identifier(model)
        )
        
        # Load appropriate prompt template based on technique
        technique_config = self.config['prompting_techniques'][technique.lower().replace(' ', '_')]
        template_path = f'prompts/{technique_config["template"]}'
        with open(template_path, 'r') as f:
            template_content = f.read()
            
        # Create PromptTemplate
        prompt_template = PromptTemplate(
            template=template_content,
            input_variables=["script"]
        )
        
        
        try:
            start_time = time.time()
            response = self.client.invoke(prompt_template.format(script=script))
            end_time = time.time()
            print(f"\n Model: {self._get_model_identifier(model)} | Response: {response.content}")
            result = self._parse_response(response.content)
            full_response = response.content
        except Exception as e:
            print(f"Error during analysis: {e}")
            result = "Error during analysis"
            full_response = str(e)
        
        return {
            'result': result,
            'response': full_response,
            'response_time': end_time - start_time
        }
    
    def _get_model_identifier(self, model_name):
        # Map friendly names to OpenRouter model identifiers
        model_map = {
            "o1-mini": "openai/o1-mini",
            "o1-preview": "openai/o1-preview",
            "GPT-4o": "openai/gpt-4o",
            "GPT-4o-mini": "openai/gpt-4o-mini",
            "GPT-4": "openai/gpt-4-turbo",  
            "GPT-3.5": "openai/gpt-3.5-turbo-0125",
            "Claude Haiku": "anthropic/claude-3-haiku",
            "Claude Sonnet": "anthropic/claude-3-sonnet",
            "Google Gemini Flash": "google/gemini-flash-1.5-8b",
            "Google Gemma 2": "google/gemma-2-9b-it:free",
            "Google Gemini Pro": "google/gemini-pro-1.5",
            "Llama 3.2": "meta-llama/llama-3.2-3b-instruct:free",
            "Mistral Nemo": "mistralai/mistral-nemo",
            "Grok 2": "x-ai/grok-2"
        }
        return model_map.get(model_name) 
    
    def _parse_response(self, response):
        try:
            # Try to parse the response as JSON
            # Remove ```json and ``` if present
            cleaned_response = response.strip()
            if cleaned_response.startswith('```json'):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith('```'):
                cleaned_response = cleaned_response[:-3]
            response_dict = json.loads(cleaned_response.strip())
            return response_dict['classification'].strip().lower()
        except json.JSONDecodeError:
            # Raise exception if response is not valid JSON
            raise ValueError("Response is not in valid JSON format. Expected JSON with 'classification' field.")