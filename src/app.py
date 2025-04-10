import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils_logger.logger import logger

from langchain_google_genai import ChatGoogleGenerativeAI
from data_loader import load_documents
from chunk_processor import chunk_documents
from rag_setup import InsuranceRAG
from utils_logger.logger import logger
import os

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


# def initialize_system():
#     # Load and process documents
#     raw_docs = load_documents()
#     if not raw_docs:
#         logger.error("No documents loaded. Check input folder!")
#         return None
        
#     # Generate chunks
#     chunks = chunk_documents(raw_docs)
    
#     # Initialize RAG system
#     rag = InsuranceRAG()
#     rag.store_documents(chunks)
    
#     # Initialize LLM
#     llm = ChatGoogleGenerativeAI(
#         model="gemini-2.0-flash",
#         temperature=0,
#         google_api_key=os.getenv("GEMINI_API_KEY")
#     )
    
#     return rag, llm



def main():
    rag, llm = initialize_system()
    if not rag or not llm:
        print("Failed to initialize system. Check logs for details.")
        return  # Exit gracefully
    
    
    print("Insurance Query Bot (type 'exit' to quit)")
    while True:
        try:
            query = input("\nQuestion: ").strip()
            if query.lower() == 'exit':
                break
                
            # Retrieve context
            context = rag.retrieve_context(query)
            if not context:
                print("I don't know.")
                continue
                
            # Generate response
            response = llm.invoke(
                f"""Answer using ONLY this context. Follow these rules:
                1. Specify the insurance tier in your answer
                2. Cite exact numbers from tables when available
                3. If unsure, say "I don't know"
                
                Context:
                {context}
                
                Question: {query}"""
            )
            
            print(f"\nAnswer: {response.content}")
            
        except Exception as e:
            logger.error(f"Runtime error: {str(e)}")
            print("An error occurred. Please check logs.")

if __name__ == "__main__":
    main()



# import sys
# from pathlib import Path

# # Add project root to Python path
# sys.path.append(str(Path(__file__).parent.parent))


# from langchain_google_genai import ChatGoogleGenerativeAI
# from data_loader import load_documents
# from chunk_processor import chunk_documents
# from rag_setup import RAGSystem
# from utils.logger import logger
# import os

# # import sys
# # from pathlib import Path

# # # Add project root to Python path
# # sys.path.append(str(Path(__file__).parent.parent))


# def initialize_system():
#     # Load documents
#     raw_docs = load_documents()
#     if not raw_docs:
#         logger.error("No documents loaded. Check input folder!")
#         return None
        
#     # Process chunks
#     chunks = chunk_documents(raw_docs)
    
#     # Initialize RAG
#     rag = RAGSystem()
#     rag.store_documents(chunks)
    
#     # Initialize LLM
#     llm = ChatGoogleGenerativeAI(
#         model="gemini-2.0-flash",
#         temperature=0,
#         google_api_key=os.getenv("GEMINI_API_KEY")
#     )
    
#     return rag, llm

# def main():
#     rag, llm = initialize_system()
    
#     print("Insurance Bot (type 'exit' to quit)")
#     while True:
#         query = input("\nQuestion: ")
#         if query.lower() == "exit":
#             break
            
#         # Retrieve context
#         context = rag.query(query)
#         if not context:
#             print("I don't know.")
#             continue
            
#         # Generate response
#         try:
#             response = llm.invoke(
#                 f"Answer using ONLY this context:\n{context}\n\n"
#                 f"Question: {query}\n"
#                 "If unsure, strictly say 'I don't know'."
#             )
#             print(f"\nAnswer: {response.content}")
            
#         except Exception as e:
#             logger.error(f"Generation failed: {str(e)}")
#             print("Sorry, I encountered an error.")

# if __name__ == "__main__":
#     main()
