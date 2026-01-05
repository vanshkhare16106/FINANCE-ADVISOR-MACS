import os
import base64
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# Loading the secret keys from the .env file so I don't have to hardcode them
load_dotenv()

# --- Setting up the AI Model ---
# I'm using GPT-4o-mini here because it's fast, cheap, and good at seeing images.
llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0.3  # Low temp keeps the answers focused, not random
)


def encode_image(image_file):
    """
    Helper function to turn the image into a weird text format (base64)
    that the AI can actually read.
    """
    return base64.b64encode(image_file.read()).decode('utf-8')


def save_to_vector_db(data):
    """
    This is just a fake database function for now.
    In the future, I'll connect this to something real like Pinecone.
    Right now it just prints the data so I know it worked.
    """
    print(f"\n[DB LOG] Inserting record into Vector DB:")
    # Using json.dumps just to make the print output look pretty
    print(json.dumps(data, indent=2))
    return True


def analyze_bill(image_data, current_query, chat_history):
    """
    This is the main brain of the app.
    It takes the image + chat history + user question and sends it all to the AI.
    """

    # --- Step 1: Tell the AI what its job is ---
    system_prompt = """
    You are a Personal Finance Advisor.
    1. Analyze the receipt image (if available).
    2. Answer user questions about expenses, items, or totals.
    3. Be concise and helpful.
    """

    messages = [SystemMessage(content=system_prompt)]

    # If there is an image, we need to add it to the message list
    if image_data:
        messages.append(
            HumanMessage(
                content=[
                    {"type": "text", "text": "Here is the receipt image."},
                    # This is the tricky part - sending the base64 string
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}},
                ]
            )
        )

    # Loop through the old messages and add them so the AI remembers context
    for sender, text in chat_history:
        if sender == "AI":
            role = AIMessage
        else:
            role = HumanMessage
        messages.append(role(content=text))

    # Finally, add the question the user just asked
    messages.append(HumanMessage(content=current_query))

    # --- Step 2: Ask the AI ---
    # We get the normal answer first so the user isn't waiting
    response = llm.invoke(messages)
    final_response_text = response.content

    # --- Step 3: Check if we need to SAVE the data ---
    # I'm using a simple keyword check here. If the user says "save" or "log",
    # we run a second pass to extract the data.
    triggers = ["save", "log", "record", "store"]

    # Check if any of the trigger words are in the user's sentence
    if any(keyword in current_query.lower() for keyword in triggers):

        # Prepare a special instruction to get clean JSON data
        extraction_prompt = """
        Based on the image and conversation above, extract the following details in strict JSON format:
        {
            "merchant": "Store Name",
            "date": "YYYY-MM-DD",
            "total_amount": "0.00",
            "currency": "Symbol",
            "items": ["list", "of", "items"]
        }
        Do not add markdown formatting (like ```json). Just return the raw JSON string.
        """

        # Add the AI's previous answer + the new instruction to the conversation
        extraction_messages = messages + [
            AIMessage(content=final_response_text),
            HumanMessage(content=extraction_prompt)
        ]

        try:
            # Ask the AI again, but this time specifically for the JSON
            extraction_response = llm.invoke(extraction_messages)

            # Cleanup: Sometimes the AI adds "```json" at the start, so I remove it
            json_str = extraction_response.content.replace("```json", "").replace("```", "").strip()

            # Convert string to a real Python dictionary
            bill_data = json.loads(json_str)

            # Send to the fake DB function
            save_to_vector_db(bill_data)

            # Let the user know it worked by adding a checkmark message
            final_response_text += "\n\n✅ **Bill details have been logged to the database.**"

        except Exception as e:
            # If something breaks during JSON parsing, just print the error and tell the user
            print(f"Extraction Error: {e}")
            final_response_text += "\n\n⚠️ *I tried to save the bill, but couldn't extract all details automatically.*"

    return final_response_text