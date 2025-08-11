# import os
# from pathlib import Path
# from src.document_analyzer.data_ingestion import DocumentHandler
# from src.document_analyzer.data_analysis import DocumentAnalyzer

# ## path to the PDF we want to test
# PDF_PATH= r"D:\\ProjectLLM\\document_portal\\data\\document_analysis\\sample.pdf"

# # dummy file wrapper to simuplate uploaded file 

# class DummyFile:
#     def __init__(self,file_path):
#         self.name= Path(PDF_PATH).name
#         self._file_path=file_path

#     def getbuffer(self):
#         return open(self._file_path,"rb").read()


# def main():
#     try:
#         print("Starting PDF ingestion..")
#         dummy_pdf=DummyFile(PDF_PATH) 

#         handler = DocumentHandler(session_id="test_ingestion_analysis")
#         saved_path = handler.save_pdf(dummy_pdf)
#         print(f"pdf saved at: {saved_path}")

#         text_content = handler.read_pdf(saved_path)
#         print(f"extracted text length: {len(text_content)} chars\n")

#         ## step 2 data analysis----
#         print("\n starting analysis metadata...")
#         analyzer=DocumentAnalyzer()
#         analysis_result = analyzer.analyze_metadata(text_content)

#         print("\n metadata analysis result") 
#         for key,value in analysis_result.items():
#              print(f"{key}:{value}")

#     except Exception as e:
#          print(f"Test failed: {e}")



# if __name__ == "__main__":
#     main()


# import io
# from pathlib import Path
# from src.document_compare.data_ingestion import DocumentIngestion
# from src.document_compare.document_comparator import DocumentComparatorLLM

# # ---- Setup: Load local PDF files as if they were "uploaded" ---- #
# def load_fake_uploaded_file(file_path: Path):
#     return io.BytesIO(file_path.read_bytes())  # simulate .getbuffer()

# def test_compare_docuemnts():
#     ref_path = Path("D:\\ProjectLLM\\document_portal\\data\\document_compare\\Long_Report_V1.pdf")
#     act_path = Path("D:\\ProjectLLM\\document_portal\\data\\document_compare\\Long_Report_V2.pdf")
    
#     class FakeUpload:
#         def __init__(self, file_path: Path):
#             self.name = file_path.name
#             self._buffer = file_path.read_bytes()

#         def getbuffer(self):
#             return self._buffer

#     # Instantiate
#     comparator = DocumentIngestion()
#     ref_upload = FakeUpload(ref_path)
#     act_upload = FakeUpload(act_path)

#     # Save files and combine
#     ref_file, act_file = comparator.save_uploaded_files(ref_upload, act_upload)
#     combined_text = comparator.combine_documents()
#     comparator.clean_old_sessions(keep_latest=3)

#     print("\n Combined Text Preview (First 1000 chars):\n")
#     print(combined_text[:1000])

#     # ---- Step 2: Run LLM comparison ---- #
#     llm_comparator = DocumentComparatorLLM()
#     df = llm_comparator.compare_documents(combined_text)
    
#     print("\n Comparison DataFrame:\n")
#     print(df)

# if __name__ == "__main__":
#     test_compare_docuemnts()


# Testing code for document chat functionality

# import sys
# from pathlib import Path
# from langchain_community.vectorstores import FAISS
# from src.single_document_chat.data_ingestion import SingleDocIngestor
# from src.single_document_chat.retrieval import ConversationalRAG
# from utils.model_loader import ModelLoader

# FAISS_INDEX_PATH = Path("faiss_index")

# def test_conversational_rag_on_pdf(pdf_path:str, question:str):
#     try:
#         model_loader = ModelLoader()
        
#         if FAISS_INDEX_PATH.exists():
#             print("Loading existing FAISS index...")
#             embeddings = model_loader.load_embeddings()
#             vectorstore = FAISS.load_local(folder_path=str(FAISS_INDEX_PATH), embeddings=embeddings,allow_dangerous_deserialization=True)
#             retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
#         else:
#             # Step 2: Ingest document and create retriever
#             print("FAISS index not found. Ingesting PDF and creating index...")
#             with open(pdf_path, "rb") as f:
#                 uploaded_files = [f]
#                 ingestor = SingleDocIngestor()
#                 retriever = ingestor.ingest_files(uploaded_files)
#         print("Running Conversational RAG...")
#         session_id = "test_conversational_rag"
#         rag = ConversationalRAG(retriever=retriever, session_id=session_id)
        
#         response = rag.invoke(question)
#         print(f"\nQuestion: {question}\nAnswer: {response}")
                    
#     except Exception as e:
#         print(f"Test failed: {str(e)}")
#         sys.exit(1)
    
# if __name__ == "__main__":
#     # Example PDF path and question
#     pdf_path = "data\\single_document_chat\\NIPS-2017-attention-is-all-you-need-Paper.pdf"
#     question = "What is the significant of atrention mechanis in simple terms?"

#     if not Path(pdf_path).exists():
#         print(f"PDF file does not exist at: {pdf_path}")
#         sys.exit(1)
    
#     # Run the test
#     test_conversational_rag_on_pdf(pdf_path, question)


# Testing code for multiple document chat functionality

import sys
from pathlib import Path
from src.multi_document_chat.data_ingestion import DocumentIngestor
from src.multi_document_chat.retreival import ConversationalRAG

def test_document_ingestion_and_rag():
    try:
        test_files = [
            "data\\multi_doc_chat\\market_analysis_report.docx",
            "data\\multi_doc_chat\\NIPS-2017-attention-is-all-you-need-Paper.pdf",
            "data\\multi_doc_chat\\sample.pdf",
            "data\\multi_doc_chat\\state_of_the_union.txt"
        ]

        uploaded_files = []
        for file_path in test_files:
            if Path(file_path).exists():
                uploaded_files.append(open(file_path, "rb"))
            else:
                print(f"File does not exist: {file_path}")

        if not uploaded_files:
            print("No valid files to upload.")
            sys.exit(1)

        ingestor = DocumentIngestor()
        retriever = ingestor.ingest_files(uploaded_files)

        for f in uploaded_files:
            f.close()

        session_id = "test_multi_doc_chat"
        rag = ConversationalRAG(session_id=session_id, retriever=retriever)
        question = "what is attention all you need paper about?"
        answer=rag.invoke(question)
        print("\n Question:", question)
        print("Answer:", answer)
        
        if not uploaded_files:
            print("No valid files to upload.")
            sys.exit(1)
            
    except Exception as e:
        print(f"Test failed: {str(e)}")
        sys.exit(1)
        
if __name__ == "__main__":
    test_document_ingestion_and_rag()           


