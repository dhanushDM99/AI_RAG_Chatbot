import chromadb
from chromadb.utils.embedding_functions import GoogleGenerativeAiEmbeddingFunction
from dotenv import load_dotenv
import os
from utils_logger.logger import logger

load_dotenv()

class InsuranceRAG:
    def __init__(self):
        self.embed_fn = GoogleGenerativeAiEmbeddingFunction(
            api_key=os.getenv("GEMINI_API_KEY"),
            model_name="models/text-embedding-004"
        )
        
        self.client = chromadb.PersistentClient(path="./insurance_db")
        
        try:
            # Use get_or_create to handle missing collections
            self.collection = self.client.get_or_create_collection(
                name="insurance_docs",
                embedding_function=self.embed_fn,
                metadata={"hnsw:space": "cosine"}
            )
            logger.info("Collection initialized successfully")
            
        except Exception as e:
            logger.critical(f"Collection initialization failed: {str(e)}")
            raise

    # from rag_setup import InsuranceRAG
    # rag = InsuranceRAG()  # Should print "Collection initialized successfully"



# class InsuranceRAG:
#     def __init__(self):
#         self.embed_fn = GoogleGenerativeAiEmbeddingFunction(
#             api_key=os.getenv("GEMINI_API_KEY"),
#             model_name="models/text-embedding-large-exp-03-07"
#         )
        
#         self.client = chromadb.PersistentClient(path="./insurance_db")
        
#         try:
#             self.collection = self.client.get_collection(
#                 name="insurance_docs",
#                 embedding_function=self.embed_fn
#             )
#             logger.info("Connected to existing vector DB")
#         except ValueError:
#             self.collection = self.client.create_collection(
#                 name="insurance_docs",
#                 embedding_function=self.embed_fn,
#                 metadata={"hnsw:space": "cosine"}
#             )
#             logger.info("Created new vector DB collection")

    def store_documents(self, chunks):
        """Store documents with tier metadata"""
        try:
            documents = []
            metadatas = []
            ids = []
            
            for idx, chunk in enumerate(chunks):
                documents.append(chunk.page_content)
                metadatas.append({
                    "insurance_tier": chunk.metadata.get("insurance_tier", "unknown"),
                    "content_type": chunk.metadata.get("content_type", "text")
                })
                ids.append(f"doc_{idx}")
                
            self.collection.upsert(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            logger.info(f"Stored {len(chunks)} documents")
            
        except Exception as e:
            logger.error(f"Storage failed: {str(e)}")
            raise

    def retrieve_context(self, query, threshold=0.75):
        """Tier-aware hybrid retrieval"""
        try:
            # Detect tier from query
            detected_tier = next(
                (t for t in ["gold", "silver", "bronze"] if t in query.lower()),
                None
            )
            
            # First-stage retrieval
            results = self.collection.query(
                query_texts=[query],
                n_results=5,
                where={"insurance_tier": detected_tier} if detected_tier else None,
                include=["metadatas", "documents", "distances"]
            )
            
            # Second-stage table retrieval for numerical queries
            if any(c.isdigit() for c in query):
                table_results = self.collection.query(
                    query_texts=[query],
                    n_results=2,
                    where={"content_type": "tabular"}
                )
                results["documents"][0].extend(table_results["documents"][0])
                results["metadatas"][0].extend(table_results["metadatas"][0])
                results["distances"][0].extend(table_results["distances"][0])
            
            # Filter and format results
            context = []
            for doc, meta, dist in zip(results["documents"][0], 
                                     results["metadatas"][0], 
                                     results["distances"][0]):
                if 1 - dist > threshold:
                    context.append(
                        f"## {meta['insurance_tier'].capitalize()} Tier\n{doc}"
                    )
            
            return "\n\n".join(context) if context else None
            
        except Exception as e:
            logger.error(f"Retrieval error: {str(e)}")
            return None




# import chromadb
# from chromadb.utils.embedding_functions import GoogleGenerativeAiEmbeddingFunction
# from dotenv import load_dotenv
# import os

# from utils.logger import logger


# load_dotenv()

# class InsuranceRAG:
#     def __init__(self):
#         self.embed_fn = GoogleGenerativeAiEmbeddingFunction(
#             api_key=os.getenv("GEMINI_API_KEY"),
#             model_name="models/text-embedding-large-exp-03-07"
#         )
        
#         self.client = chromadb.PersistentClient(path="./insurance_db")
        
#         try:
#             self.collection = self.client.get_collection(
#                 name="insurance_docs",
#                 embedding_function=self.embed_fn
#             )
#         except ValueError:
#             self.collection = self.client.create_collection(
#                 name="insurance_docs",
#                 embedding_function=self.embed_fn,
#                 metadata={"hnsw:space": "cosine"}
#             )

#     def store_documents(self, chunks):
#         documents = []
#         metadatas = []
#         ids = []
        
#         for idx, chunk in enumerate(chunks):
#             documents.append(chunk.page_content)
#             metadatas.append({
#                 "insurance_tier": chunk.metadata.get("insurance_tier", "unknown"),
#                 "content_type": chunk.metadata.get("content_type", "text")
#             })
#             ids.append(f"doc_{idx}")
            
#         self.collection.upsert(
#             documents=documents,
#             metadatas=metadatas,
#             ids=ids
#         )

#     def retrieve_context(self, query, threshold=0.75):
#         try:
#             # Tier detection from query
#             detected_tier = None
#             for tier in ["gold", "silver", "bronze"]:
#                 if tier in query.lower():
#                     detected_tier = tier
#                     break
            
#             # Hybrid search
#             results = self.collection.query(
#                 query_texts=[query],
#                 n_results=5,
#                 where={"insurance_tier": detected_tier} if detected_tier else None,
#                 include=["metadatas", "documents", "distances"]
#             )
            
#             # Fallback for numerical queries
#             if any(c.isdigit() for c in query) and not results["documents"][0]:
#                 results = self.collection.query(
#                     query_texts=[query],
#                     n_results=3,
#                     where={"content_type": "tabular"}
#                 )
            
#             # Threshold filtering
#             context = []
#             for doc, meta, dist in zip(results["documents"][0], 
#                                      results["metadatas"][0], 
#                                      results["distances"][0]):
#                 if 1 - dist > threshold:
#                     context.append(
#                         f"## {meta['insurance_tier'].capitalize()} Tier\n{doc}"
#                     )
            
#             return "\n\n".join(context) if context else None
            
#         except Exception as e:
#             logger.error(f"Retrieval error: {str(e)}")
#             return None




# # import chromadb
# # from chromadb.utils.embedding_functions import GoogleGenerativeAiEmbeddingFunction
# # from dotenv import load_dotenv
# # import os
# # from utils.logger import logger

# # load_dotenv()

# # class RAGSystem:
# #     def __init__(self):
# #         self.embed_fn = GoogleGenerativeAiEmbeddingFunction(
# #             api_key=os.getenv("GEMINI_API_KEY"),
# #             model_name="models/text-embedding-large-exp-03-07"
# #         )
        
# #         self.client = chromadb.PersistentClient(path="insurance_db")
        
# #         try:
# #             self.collection = self.client.get_collection(
# #                 name="insurance_docs",
# #                 embedding_function=self.embed_fn
# #             )
# #             logger.info("Loaded existing vector collection")
            
# #         except ValueError:
# #             self.collection = self.client.create_collection(
# #                 name="insurance_docs",
# #                 embedding_function=self.embed_fn
# #             )
# #             logger.info("Created new vector collection")

# #     def store_documents(self, chunks):
# #         """Store chunks with tier metadata"""
# #         try:
# #             documents = []
# #             metadatas = []
# #             ids = []
            
# #             for idx, chunk in enumerate(chunks):
# #                 documents.append(chunk.page_content)
# #                 metadatas.append(chunk.metadata)
# #                 ids.append(f"doc_{idx}")
                
# #             self.collection.add(
# #                 documents=documents,
# #                 metadatas=metadatas,
# #                 ids=ids
# #             )
# #             logger.info(f"Stored {len(chunks)} documents in DB")
            
# #         except Exception as e:
# #             logger.error(f"Storage failed: {str(e)}")
# #             raise

# #     def query(self, question, threshold=0.7):
# #         """Retrieve relevant chunks with tier context"""
# #         try:
# #             results = self.collection.query(
# #                 query_texts=[question],
# #                 n_results=3,
# #                 include=["metadatas", "distances"]
# #             )
            
# #             # Filter by similarity score
# #             valid_results = []
# #             for meta, dist in zip(results["metadatas"][0], results["distances"][0]):
# #                 if 1 - dist > threshold:  # Convert distance to similarity
# #                     valid_results.append(meta)
                    
# #             if not valid_results:
# #                 logger.warning("No relevant documents found")
# #                 return None
                
# #             # Format context with tier info
# #             context = []
# #             for res in valid_results:
# #                 tier = res["insurance_tier"].capitalize()
# #                 context.append(f"[{tier} Tier]\n{res['document']}")
                
# #             return "\n\n".join(context)
            
# #         except Exception as e:
# #             logger.error(f"Query failed: {str(e)}")
# #             raise
