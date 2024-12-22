from datetime import datetime
import streamlit as st


def process_pdf_document(pdf_path, embeddings_manager):
    """Process and store PDF document contents."""
    try:
        result = embeddings_manager.create_embeddings(pdf_path)
        # Store PDF processing record in database
        c = st.session_state.cursor
        c.execute('''INSERT INTO document_processing 
                     (file_path, processing_date, status)
                     VALUES (?, ?, ?)''',
                  (pdf_path, datetime.now(), 'success'))
        st.session_state.conn.commit()
        return result
    except Exception as e:
        # Log error in database
        c = st.session_state.cursor
        c.execute('''INSERT INTO document_processing 
                     (file_path, processing_date, status, error_message)
                     VALUES (?, ?, ?, ?)''',
                  (pdf_path, datetime.now(), 'error', str(e)))
        st.session_state.conn.commit()
        raise e
