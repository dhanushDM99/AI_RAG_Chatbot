# AI_RAG_Chatbot

# How to run:

 1. create virtual env (preferable) and install requirements.txt
    -- Already the input data is in input folder.
 2. now run app.py 
    if you are in project root then command to run is : pyhton src/app.py
 3. It may take a couple of minutes to get streamlit up and running. Once started ask your queries.

 # Note:  
  - I already pre processed given source documents (conatining tables and all data ) and transformed data to markdown format using llamaparse (# by llamaindex) so please dont add the documents freshly if done the results wont be good as the normal retrievers and tools are not that good with documents containing tables.
  # I hop eto discuss it in detail in the interview if possible 
   The preprocessing also makes it suitable for metadata appending to chunks so that every chunk in vector db is mapped with source document info/ insurance policy name/tier. Which in normal RAG we dont find/do.