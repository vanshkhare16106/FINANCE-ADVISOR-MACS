import streamlit as st
from PIL import Image
from chain import analyze_bill, encode_image

# Page setup - tab title and icon
st.set_page_config(page_title="Personal Finance Advisor", page_icon="💰")

st.title("💰 Smart Finance Advisor")

# --- Memory Setup ---
# Streamlit reloads the whole script every time you interact with it.
# We need to save the chat history and the image in 'session_state'
# so they don't disappear when the app refreshes.
if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_file_content" not in st.session_state:
    st.session_state.uploaded_file_content = None

# --- Sidebar (Inputs) ---
with st.sidebar:
    st.header("1. Add Receipt")

    # Toggle to turn camera on/off (keeps the UI clean)
    enable_camera = st.toggle("📸 Enable Camera", value=False)

    camera_img = None
    if enable_camera:
        camera_img = st.camera_input("Take a picture")

    # Always show the upload button just in case
    uploaded_file = st.file_uploader("Or upload an image", type=["jpg", "png", "jpeg"])

    # Decide which image to use:
    # If the camera is on and has a picture, use that. Otherwise, use the uploaded file.
    image_source = camera_img if (enable_camera and camera_img) else uploaded_file

    if image_source:
        try:
            # Convert the image to a format the AI can read
            new_image_bytes = encode_image(image_source)

            # Only update if it's actually a new image (prevents unnecessary processing)
            if st.session_state.uploaded_file_content != new_image_bytes:
                st.session_state.uploaded_file_content = new_image_bytes
                st.success("Image processed!")

            # Show a preview so we know what the AI is looking at
            st.image(image_source, caption="Receipt to Analyze", use_container_width=True)

        except Exception as e:
            st.error(f"Error processing image: {e}")

    st.divider()

    # Button to reset everything
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.session_state.uploaded_file_content = None
        st.rerun()

# --- Main Chat Area ---

# 1. Print all past messages from the history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 2. Handle new user input
if user_query := st.chat_input("Ask about your bill..."):

    # Make sure we have a bill before answering questions
    if not st.session_state.uploaded_file_content:
        st.warning("⚠️ Please take a photo or upload a receipt first!")
    else:
        # Show the user's question immediately
        with st.chat_message("user"):
            st.markdown(user_query)
        # Add it to memory
        st.session_state.messages.append({"role": "user", "content": user_query})

        # Get the AI response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                # Format history for the backend (User vs AI)
                # We exclude the last message because we just added it above
                history_for_chain = [
                    ("User" if m["role"] == "user" else "AI", m["content"])
                    for m in st.session_state.messages[:-1]
                ]

                # Send everything to the AI model
                response = analyze_bill(
                    st.session_state.uploaded_file_content,
                    user_query,
                    history_for_chain
                )

                st.markdown(response)

        # Save the AI's answer to memory
        st.session_state.messages.append({"role": "assistant", "content": response})