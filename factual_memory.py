# Building Factual Memory

# Packages installed
from google import genai
import os
from dotenv import load_dotenv
from google.genai import types
import re
import json


# Basic setup
load_dotenv ()
GEMINI_API_KEY = os.getenv ("GEMINAI_KEY")
client = genai.Client (api_key = GEMINI_API_KEY)


# STEP 1 COMPLETE Extraction

config = types.GenerateContentConfig (

    system_instruction = f"""
        Extract stable factual information from this message.
        Ignore temporary and emotional information.
        Return json only.
        Message: "query"
        """

)

def llm_extract (query:str):

    response = client.models.generate_content (
        model = "gemini-2.5-flash",
        contents = query,
        config = config,
    )

    return response.text

# Step 2 convert gemini text to json


def rawJson_conversion_to_dict (rawdata):
    
    clean = re.sub(r"```json|```", "", rawdata).strip()
    
    try:
        data = json.loads(clean)   # JSON string → Python dict
        return data
    except json.JSONDecodeError:
        print("Not valid JSON")
        return None

# Step 3 Add or overright (update) the memory


def update_memory (stored,new):

    if not new:
        return stored

    for key,value in new.items ():
        stored [key] = value

    return stored    

# step 4 save the factual memory in file

def save_in_files (memory):

    with open ("stored_memory.json", "w") as f:
        json.dump (memory, f, indent = 2) 

# step 5 read the factual memory

def read_in_file (filename):

    # if call == 0:
    #     print ("It is the firt time to read the file which is empty.")
    #     return {}
    
    # else :
        try : 
            with open (filename, "r") as f:
              data =  json.load (f)
            return data  
        except json.JSONDecodeError:
            print ("Fail in read file")
            return {}


# step 6 File pure json to text

def dict_conversion_to_rawJson (jsonData):

    try:
        data = json.dumps (jsonData)
        return data
    except json.JSONDecodeError:
        print ("Cannot covert to raw text!")
        return None

# step 7 actual factual memory

factual_memory = read_in_file ("stored_memory.json")


if factual_memory is None:
    factual_memory = {}

def retrieve_relevent_info (query, memory):
    
    relevent = {}
    query = query.lower ()

    for key,value in memory.items ():
        if key.lower() in query:
             relevent [key] = value

    return relevent        

# step 9 give memory access + query to gemini -----------> to decide

extra_info = types.GenerateContentConfig (
    system_instruction = '''You are an AI assistant with access to a factual memory store.

 Your behavior rules are:

 1. Always analyze the user's query first.
 2. Determine whether the query requires factual information from memory.
 3. If factual memory is relevant:
   - Retrieve only the information that is directly related to the query.
   - Use the retrieved facts accurately and concisely.
   - Do NOT add assumptions, guesses, or external knowledge.
 4. If no relevant factual information exists:
   - Clearly state that the required information is not available.
   - Do NOT hallucinate or fabricate facts.
 5. If the query does not require factual memory:
   - Respond normally using reasoning or general language ability.
 6. Never expose raw memory data unless explicitly requested.
 7. Prioritize correctness, relevance, and clarity over verbosity.
 8. Maintain a helpful and neutral tone in all responses.
 If factual information is required but missing or incomplete, respond with:
 "I do not have enough factual information to answer this query."
 '''
)

def llm_decider (query, retriveData):

    prompt_parts = [
        f"User Query: {query}",
        f"Context Data: {retriveData}"
    ]

    response = client.models.generate_content (
        model = "gemini-2.5-flash",
        contents = prompt_parts,
        config = extra_info,
        
    )

    return response.text

# Execution

# factual_memory.py
# _factual_memory = {}
_raw_extracted_data = None

def handle_user_message(user_message):
    global _raw_extracted_data, factual_memory

    if "weather" in user_message.lower ():
        _raw_extracted_data = None
        return

    extracted_data = llm_extract(user_message)
    clean_extracted_data = rawJson_conversion_to_dict(extracted_data)

    factual_memory = update_memory(factual_memory, clean_extracted_data)
    save_in_files(factual_memory)

    res = retrieve_relevent_info(user_message, factual_memory)
    _raw_extracted_data = res

def sent_response_back ():
    if _raw_extracted_data == None:
        return {}
    else:
        return _raw_extracted_data or {}
