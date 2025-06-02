from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import json
from guardrail import validate_memory_write
from datetime import datetime

# Load environment variables and initialize client
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

def fetch_memory_for_user(user_id):
    try:
        with open("memory.json", "r") as memory_file:
            memory_data = json.load(memory_file)
            user_data = memory_data.get(user_id, {})
            memory_content = ", ".join([x for k,x in user_data.items()])
            return memory_content
    except FileNotFoundError:
        return ""

def gemini_response(conversation_history=[], user_information = {'id': 'user_1'}):
    # Cost calculations per million tokens
    INPUT_TOKEN_PRICE = 0.10 / 1000000
    OUTPUT_TOKEN_PRICE = 0.40 / 1000000
    api_call_count = 0
    total_input_tokens = 0
    total_output_tokens = 0

    # Define system prompt
    with open("system_prompt.txt", "r") as file:
        system_prompt = file.read()

    user_memory = fetch_memory_for_user(user_information['id'])
    print(f"User memory: {user_memory}")
    if user_memory:
        system_prompt = f"{system_prompt} \n\n The below is the long term stored memory of the user, it can also be empty, use this when needed: \n\n {user_memory}"

    # Configuration for content generation
    generate_config = types.GenerateContentConfig(
        system_instruction=system_prompt,
        response_mime_type="text/plain")
    
    # Conversation history
    conversation_history = conversation_history

    while True: 
        print('-' * 50)
        user_input = input("User: ")
        
        # Check for exit commands
        if user_input.lower() in ["close chat", "quit chat", "exit chat", "stop chat", "end chat"]:
            # Display usage statistics
            total_cost = (total_input_tokens * INPUT_TOKEN_PRICE) + (total_output_tokens * OUTPUT_TOKEN_PRICE)
            print(f"Input tokens: {total_input_tokens}")
            print(f"Output tokens: {total_output_tokens}")
            print(f"Total cost: ${total_cost:.6f}")
            print(f"API calls made: {api_call_count}")
            return total_input_tokens, total_output_tokens, api_call_count
        
        memory_update = validate_memory_write(user_input)

        if memory_update.status:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Load existing memory data
            memory_data = {user_information['id']: {}}
            if os.path.exists("memory.json"):
                try:
                    with open("memory.json", "r") as memory_file:
                        memory_data = json.load(memory_file)
                except json.JSONDecodeError:
                    pass  # Handle empty or invalid JSON file
            
            # Store the memory content with timestamp as key
            memory_data[user_information['id']][timestamp] = memory_update.memory_content
            
            # Write updated data back to file
            with open("memory.json", "w") as memory_file:
                json.dump(memory_data, memory_file, indent=4)
        else:
            pass


        # Create user content object
        user_message = types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_input)],
        )
        
        # Add user message to conversation history
        conversation_history.append(user_message)

        # Get streaming response from Gemini
        try:
            response_stream = gemini_client.models.generate_content_stream(
                model="gemini-2.0-flash",
                contents=conversation_history,
                config=generate_config)
            api_call_count += 1
        except Exception as e:
            # print(f"Error: Could not generate response. See logs for details.")
            print('-' * 50)
            print("Gemini: Error: Could not generate response. See logs for details.")
            continue
        
        # Process and display the response
        print('-' * 50)
        print("Gemini:", end=" ")
        full_response = ""
        last_chunk = None

        for chunk in response_stream:
            last_chunk = chunk
            if chunk.text:
                full_response += chunk.text
                print(chunk.text, end="", flush=True)

        print('-' * 50)
        # Update token counts if metadata available
        if hasattr(last_chunk, 'usage_metadata') and last_chunk.usage_metadata:
            usage = last_chunk.usage_metadata
            chunk_input_tokens = usage.prompt_token_count if usage.prompt_token_count else 0
            chunk_output_tokens = usage.candidates_token_count if usage.candidates_token_count else 0
            
            # Add to running totals
            total_input_tokens += chunk_input_tokens
            total_output_tokens += chunk_output_tokens

        # Add the model's response to conversation history
        model_message = types.Content(
            role="model",
            parts=[types.Part.from_text(text=full_response)],
        )
        conversation_history.append(model_message)

if __name__ == "__main__":
    try:        
        # Initialize conversation history and user information
        conversation_history = []
        user_information = {'id': f"user_{input('Enter your user ID: ')}"}
        print("Let us start with your name and a brief introduction about yourself. --- Let the river of wisdom flow!")
        # Start the conversation
        gemini_response(conversation_history, user_information)
    except KeyboardInterrupt:
        print("\nChat closed by user.")
    except Exception as e:
        print(f"An unexpected error occurred. Check the log file for details.")