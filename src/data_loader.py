import os
import json
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from table_processor import process_tabular_data
from utils_logger.logger import logger

def detect_tier(filename):
    filename_lower = filename.lower()
    for tier in ["gold", "silver", "bronze"]:
        if tier in filename_lower:
            return tier
    return "unknown"

def load_documents(input_dir="input"):
    documents = []
    for filename in os.listdir(input_dir):
        filepath = os.path.join(input_dir, filename)
        tier = detect_tier(filename)
        
        try:
            if filename.endswith(".pdf"):
                # PDF processing remains unchanged
                loader = PyPDFLoader(filepath)
                pages = loader.load()
                for page in pages:
                    page.metadata["insurance_tier"] = tier
                documents.extend(pages)
                
            elif filename.endswith((".md", ".txt", ".json")):
                # Fix: Specify UTF-8 encoding with error handling
                with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()
                
                # Existing processing logic
                if filename.endswith(".json"):
                    data = json.loads(content)
                    content = "\n".join([item["text"] for item in data["pages"]])
                
                if "|" in content:
                    docs = process_tabular_data(content, tier)
                else:
                    docs = [Document(page_content=content, metadata={"insurance_tier": tier})]
                
                documents.extend(docs)
                
        except UnicodeDecodeError as ude:
            logger.error(f"Encoding error in {filename}: {str(ude)}")
            continue  # Skip this file but continue processing others
        except Exception as e:
            logger.error(f"Failed to process {filename}: {str(e)}")
            continue
    
    if not documents:
        logger.critical("No valid documents loaded. Check input files and encoding!")
    else:
        logger.info(f"Successfully loaded {len(documents)} documents")
    
    return documents


# def load_documents(input_dir="input"):
#     documents = []
#     for filename in os.listdir(input_dir):
#         filepath = os.path.join(input_dir, filename)
#         tier = detect_tier(filename)
        
#         try:
#             if filename.endswith(".pdf"):
#                 loader = PyPDFLoader(filepath)
#                 pages = loader.load()
#                 for page in pages:
#                     page.metadata["insurance_tier"] = tier
#                 documents.extend(pages)
                
#             elif filename.endswith((".md", ".txt", ".json")):
#                 with open(filepath, 'r') as f:
#                     content = f.read()
                
#                 if filename.endswith(".json"):
#                     data = json.loads(content)
#                     content = "\n".join([item["text"] for item in data["pages"]])
                
#                 if "|" in content:  # Table detection
#                     docs = process_tabular_data(content, tier)
#                 else:
#                     docs = [Document(page_content=content, metadata={"insurance_tier": tier})]
                
#                 documents.extend(docs)
                
#         except Exception as e:
#             logger.error(f"Failed to process {filename}: {str(e)}")
    
#     return documents



# import os
# import json
# from langchain_community.document_loaders import PyPDFLoader
# from langchain_core.documents import Document
# # from .table_processor import process_tabular_data
# from src.chunk_processor import chunk_documents
# from utils.logger import logger

# from table_processor import process_tabular_data


# def detect_tier(filename):
#     filename_lower = filename.lower()
#     for tier in ["gold", "silver", "bronze"]:
#         if tier in filename_lower:
#             return tier
#     return "unknown"

# def load_documents(input_dir="input"):
#     documents = []
#     for filename in os.listdir(input_dir):
#         filepath = os.path.join(input_dir, filename)
#         tier = detect_tier(filename)
        
#         try:
#             if filename.endswith(".pdf"):
#                 loader = PyPDFLoader(filepath)
#                 pages = loader.load()
#                 for page in pages:
#                     page.metadata["insurance_tier"] = tier
#                 documents.extend(pages)
                
#             elif filename.endswith((".md", ".txt", ".json")):
#                 with open(filepath, 'r') as f:
#                     content = f.read()
                
#                 if filename.endswith(".json"):
#                     data = json.loads(content)
#                     content = "\n".join([item["text"] for item in data["pages"]])
                
#                 if "|" in content:  # Table detection
#                     docs = process_tabular_data(content, tier)
#                 else:
#                     docs = [Document(page_content=content, metadata={"insurance_tier": tier})]
                
#                 documents.extend(docs)
                
#         except Exception as e:
#             logger.error(f"Failed to process {filename}: {str(e)}")
    
#     return documents




# # import os
# # from langchain_community.document_loaders import PyPDFLoader
# # # Correct syntax (2024+)
# # # from langchain_community.document_loaders import TextLoader, PyPDFLoader

# # from utils.logger import logger

# # def load_pdfs(input_dir="input"):
# #     """Load PDFs with tier detection from filenames"""
# #     documents = []
    
# #     for filename in os.listdir(input_dir):
# #         if filename.lower().endswith(".pdf"):
# #             try:
# #                 # Extract tier from filename (case-insensitive)
# #                 tier = "unknown"
# #                 for t in ["gold", "silver", "bronze"]:
# #                     if t in filename.lower():
# #                         tier = t
# #                         break
                        
# #                 filepath = os.path.join(input_dir, filename)
# #                 logger.info(f"Processing {filename} as {tier} tier")
                
# #                 loader = PyPDFLoader(filepath)
# #                 pages = loader.load()
                
# #                 # Add tier metadata to every page
# #                 for page in pages:
# #                     page.metadata["insurance_tier"] = tier
                    
# #                 documents.extend(pages)
                
# #             except Exception as e:
# #                 logger.error(f"Failed to process {filename}: {str(e)}")
# #                 continue
                
# #     return documents
