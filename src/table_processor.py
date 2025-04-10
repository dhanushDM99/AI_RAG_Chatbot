from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_core.documents import Document
from utils_logger.logger import logger

def process_tabular_data(content, tier):
    try:
        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
            ("|", "Table")
        ]
        
        splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=headers_to_split_on,
            strip_headers=False
        )
        
        chunks = splitter.split_text(content)
        for chunk in chunks:
            chunk.metadata.update({
                "insurance_tier": tier,
                "content_type": "tabular"
            })
            
        return chunks
        
    except Exception as e:
        logger.error(f"Table processing failed: {str(e)}")
        return []




# from langchain_text_splitters import MarkdownHeaderTextSplitter
# from utils.logger import logger

# def process_tabular_data(content, tier):
#     try:
#         headers_to_split_on = [
#             ("#", "Header 1"),
#             ("##", "Header 2"),
#             ("###", "Header 3"),
#             ("|", "Table")
#         ]
        
#         splitter = MarkdownHeaderTextSplitter(
#             headers_to_split_on=headers_to_split_on,
#             strip_headers=False
#         )
        
#         chunks = splitter.split_text(content)
#         for chunk in chunks:
#             chunk.metadata.update({
#                 "insurance_tier": tier,
#                 "content_type": "tabular"
#             })
            
#         return chunks
        
#     except Exception as e:
#         logger.error(f"Table processing failed: {str(e)}")
#         return []
