import sys
import os
import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils_logger.logger import logger
from langchain_google_genai import ChatGoogleGenerativeAI
from data_loader import load_documents
from chunk_processor import chunk_documents
from rag_setup import InsuranceRAG

# Initialize RAG and LLM
@st.cache_resource  # Cache initialization to avoid reloading on every user interaction
def initialize_system():
    try:
        raw_docs = load_documents()
        if not raw_docs:
            logger.error("No documents loaded. Check input folder and logs!")
            return None, None  # Return tuple to prevent unpacking error
            
        chunks = chunk_documents(raw_docs)
        rag = InsuranceRAG()
        rag.store_documents(chunks)
        
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0,
            google_api_key=os.getenv("GEMINI_API_KEY")
        )
        
        return rag, llm
        
    except Exception as e:
        logger.critical(f"System initialization failed: {str(e)}")
        return None, None


# Streamlit app layout
st.set_page_config(page_title="Insurance Query Bot", layout="centered")

st.title("Insurance Query Bot")
st.write("Ask questions about insurance tiers (Gold, Silver, Bronze).")

rag, llm = initialize_system()
if not rag or not llm:
    st.error("Failed to initialize system. Check logs for details.")
    st.stop()

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if user_query := st.chat_input("Type your question here..."):
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})

    # Retrieve context using RAG system
    context = rag.retrieve_context(user_query)
    if not context:
        response = "I don't know."
    else:
        response = llm.invoke(
            f"""Answer using ONLY this context. Follow these rules:
            1. Cite exact numbers from tables when available.
            2. If unsure, say 'I don't know.'
            
            Context:
            {context}
            
            Question: {user_query}"""
        ).content

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})





# import sys
# import os

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from utils_logger.logger import logger

# from langchain_google_genai import ChatGoogleGenerativeAI
# from data_loader import load_documents
# from chunk_processor import chunk_documents
# from rag_setup import InsuranceRAG
# from utils_logger.logger import logger
# import os

# def initialize_system():
#     try:
#         raw_docs = load_documents()
#         if not raw_docs:
#             logger.error("No documents loaded. Check input folder and logs!")
#             return None, None  # Return tuple to prevent unpacking error
            
#         chunks = chunk_documents(raw_docs)
#         rag = InsuranceRAG()
#         rag.store_documents(chunks)
        
#         llm = ChatGoogleGenerativeAI(
#             model="gemini-2.0-flash",
#             temperature=0,
#             google_api_key=os.getenv("GEMINI_API_KEY")
#         )
        
#         return rag, llm
        
#     except Exception as e:
#         logger.critical(f"System initialization failed: {str(e)}")
#         return None, None


# # def initialize_system():
# #     # Load and process documents
# #     raw_docs = load_documents()
# #     if not raw_docs:
# #         logger.error("No documents loaded. Check input folder!")
# #         return None
        
# #     # Generate chunks
# #     chunks = chunk_documents(raw_docs)
    
# #     # Initialize RAG system
# #     rag = InsuranceRAG()
# #     rag.store_documents(chunks)
    
# #     # Initialize LLM
# #     llm = ChatGoogleGenerativeAI(
# #         model="gemini-2.0-flash",
# #         temperature=0,
# #         google_api_key=os.getenv("GEMINI_API_KEY")
# #     )
    
# #     return rag, llm



# def main():
#     rag, llm = initialize_system()
#     if not rag or not llm:
#         print("Failed to initialize system. Check logs for details.")
#         return  # Exit gracefully
    
    
#     print("Insurance Query Bot (type 'exit' to quit)")
#     while True:
#         try:
#             query = input("\nQuestion: ").strip()
#             if query.lower() == 'exit':
#                 break
                
#             # Retrieve context
#             context = rag.retrieve_context(query)
#             if not context:
#                 print("I don't know.")
#                 continue
                
#             # Generate response
#             response = llm.invoke(
#                 f"""Answer using ONLY this context. Follow these rules:
#                 1. Specify the insurance tier in your answer
#                 2. Cite exact numbers from tables when available
#                 3. If unsure, say "I don't know"
                
#                 Context:
#                 {context}
                
#                 Question: {query}"""
#             )
            
#             print(f"\nAnswer: {response.content}")
            
#         except Exception as e:
#             logger.error(f"Runtime error: {str(e)}")
#             print("An error occurred. Please check logs.")

# if __name__ == "__main__":
#     main()


