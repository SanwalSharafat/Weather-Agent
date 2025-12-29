# Import System
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
from weather import get_current_weather

# Load environment variables
load_dotenv()
GEMINAI_API_KEY = os.getenv("GEMINAI_KEY")
API_KEY = os.getenv("API_KEY")

# --- Initial Setup Checks ---
if not GEMINAI_API_KEY:
    print("Error: GEMINAI_API_KEY environment variable not set.")
    exit()


# The client initializes the Gemini service connection
client = genai.Client(api_key=GEMINAI_API_KEY)


# -----------------------------------------------------
# TOOL DECLARATION
# -----------------------------------------------------
weather_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="get_current_weather",
            description="Returns the current weather for a specific location.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "location": types.Schema(
                        type=types.Type.STRING,
                        description="City name, e.g., Karachi or New York"
                    )
                },
                required=["location"],
            ),
        )
    ]
)

# -----------------------------------------------------
# HISTORY TRIM
# -----------------------------------------------------
def trim_history(history, limit=8):
    if len(history) > limit:
        return history[-limit:]
    return history

# -----------------------------------------------------
# CONFIGURATION
# -----------------------------------------------------
configs = types.GenerateContentConfig(
    system_instruction=(
        "You are a helpful weather assistant. "
        "Always call the get_current_weather tool when asked about the weather."
    ),
    tools=[weather_tool],
)

# -----------------------------------------------------
# AGENT LOGIC
# -----------------------------------------------------
def weather_agent(prompt: str, history, memory) -> str:

    history[:] = trim_history(history)

    # Add user message
    history.append(types.Content(role="user", parts=[types.Part(text=prompt)]))

    prompt_parts = [
        f"User Query: {history}",
        f"Context Data: {memory}"
    ]

    # FIRST MODEL CALL
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt_parts,
            config=configs,
        )
    except Exception as e:
        return f"An API error occurred during the first call: {e}"
    
    # If function call exists
    if response.function_calls:

        # Add assistant response to history
        history.append(
            types.Content(
                role="assistant",
                parts=response.candidates[0].content.parts
            )
        )

        # Extract function call properly
        function_call = response.candidates[0].content.parts [0].function_call

        if function_call.name == "get_current_weather":

            location = function_call.args.get("location")
            if not location:
                return "Error: Tool call missing 'location' argument.'"

            tool_result = get_current_weather(location=location)

            # Prepare tool response part
            function_response_part = types.Part.from_function_response(
                name="get_current_weather",
                response=tool_result
            )

            # Add tool response to history
            history.append(types.Content(role="tool", parts=[function_response_part]))


            # SECOND MODEL CALL
            second_response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=history,
                config=configs,
            )
            return second_response.candidates[0].content.parts[0].text

        else:
            return f"Error: Unexpected function call {function_call.name}."

    # No tool call → Just respond normally
    return response.candidates[0].content.parts[0].text
