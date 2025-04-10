from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils_logger.logger import logger

def chunk_documents(docs, chunk_size=512):
    """Split documents with metadata preservation"""
    try:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=64,
            add_start_index=True
        )
        chunks = splitter.split_documents(docs)
        logger.info(f"Generated {len(chunks)} chunks")
        return chunks
    except Exception as e:
        logger.error(f"Chunking failed: {str(e)}")
        raise



# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from utils.logger import logger

# def chunk_documents(docs, chunk_size=512):
#     """Split documents with tier-aware chunking"""
#     try:
#         splitter = RecursiveCharacterTextSplitter(
#             chunk_size=chunk_size,
#             chunk_overlap=64,
#             add_start_index=True
#         )
        
#         chunks = splitter.split_documents(docs)
#         logger.info(f"Created {len(chunks)} chunks from {len(docs)} pages")
        
#         # Verify metadata persistence
#         for chunk in chunks[:3]:
#             if "insurance_tier" not in chunk.metadata:
#                 logger.warning("Missing tier metadata in chunk!")
                
#         return chunks
        
#     except Exception as e:
#         logger.error(f"Chunking failed: {str(e)}")
#         raise
