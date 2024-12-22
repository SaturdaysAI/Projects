import streamlit as st
import re
import tempfile
from PIL import Image
from database import setup_database
from user_management import check_user, create_user, render_user_profile
from parking_analysis import process_parking_image
from camera_integration import camera_integration_dashboard
from pdf_processing import process_pdf_document
from data_analysis import render_data_analysis
from video_analysis import render_video_analysis_dashboard
from chatbot import ChatbotManager
from vectors import EmbeddingsManager
from subscription import render_unified_subscription_page


# Email validation function
def validate_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)


# Password validation function
def validate_password(password):
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    return True, ""


# Initialize session state
if 'user' not in st.session_state:
    st.session_state.update({
        'user': None,
        'temp_pdf_path': None,
        'temp_video_path': None,
        'chatbot_manager': None,
        'messages': [],
        'parking_stats': {'empty': 0, 'filled': 0},
        'conn': None,
        'cursor': None
    })


def main():
    # Initialize database connection if not already done
    if st.session_state.conn is None or st.session_state.cursor is None:
        st.session_state.conn, st.session_state.cursor = setup_database()

    # Set page configuration
    st.set_page_config(
        page_title="Intelligent Parking Space Detection",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Sidebar navigation
    with st.sidebar:
        st.image("logo.png", use_column_width=True)
        st.markdown("### 🚗 Smart Parking Assistant")
        st.markdown("---")

        if st.session_state.user is None:
            login_tab, register_tab = st.tabs(["Login", "Register"])

            # Login tab
            with login_tab:
                login_user = st.text_input("Username", key="login_user")
                login_pass = st.text_input("Password", type="password", key="login_pass")

                if st.button("Login"):
                    if check_user(login_user, login_pass):
                        st.session_state.user = {'username': login_user}
                        st.success("Successfully logged in!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials")

            # Registration tab with validation
            with register_tab:
                reg_user = st.text_input("Username", key="reg_user")
                reg_email = st.text_input("Email", key="reg_email")
                reg_pass = st.text_input("Password", type="password", key="reg_pass")

                if st.button("Register"):
                    # Validate inputs
                    if not reg_user:
                        st.warning("Username cannot be empty.")
                    elif not validate_email(reg_email):
                        st.warning("Invalid email format.")
                    else:
                        valid_password, message = validate_password(reg_pass)
                        if not valid_password:
                            st.warning(message)
                        else:
                            # Create user in the database
                            if create_user(reg_user, reg_pass, reg_email):
                                st.success("Registration successful! Please login.")
                            else:
                                st.error("Username or email already exists")
        else:
            st.write(f"Welcome, {st.session_state.user['username']}!")
            if st.session_state.user.get('profile_pic'):
                st.image(st.session_state.user['profile_pic'], width=100)

            menu = [
                "🏠 Home", "🚗 Parking Analysis", "🎥 Video Analysis",
                "🤖 Parking Assistant", "📊 Data Analysis",
                "📹 Live Camera Analysis", "💰 Pricing",
                "👤 User Profile", "📧 Contact"
            ]

            choice = st.selectbox("Navigate", menu)

            if st.button("Logout"):
                st.session_state.user = None
                st.rerun()

    # Main content based on navigation choice
    if st.session_state.user is None:
        st.title("Welcome to Smart Parking Assistant")
        st.markdown("Please login or register to continue.")
    else:
        if choice == "🏠 Home":
            st.title("Smart Parking Assistant Dashboard")
            st.markdown("""
            Welcome to your smart parking management system! 🚀
            
            Our system helps you:
            - Monitor parking spaces in real-time
            - Analyze parking patterns and trends
            - Generate detailed reports and insights
            - Optimize parking operations
            """)

            # Quick stats
            if 'parking_stats' in st.session_state:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Spaces Monitored",
                              f"{st.session_state.parking_stats['empty'] + st.session_state.parking_stats['filled']}")
                with col2:
                    st.metric("Available Spaces", f"{st.session_state.parking_stats['empty']}")
                with col3:
                    st.metric("Occupied Spaces", f"{st.session_state.parking_stats['filled']}")

        elif choice == "🚗 Parking Analysis":
            st.title("🚗 Parking Space Analysis")

            uploaded_file = st.file_uploader("Upload parking lot image", type=['png', 'jpg', 'jpeg'])
            if uploaded_file is not None:
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Image", use_column_width=True)

                notes = st.text_area("Add notes (optional)")

                if st.button("Analyze Parking Spaces"):
                    with st.spinner("Analyzing parking spaces..."):
                        empty_count, filled_count, efficiency, revenue, peak_hour = process_parking_image(image, notes)

                        st.success("Analysis complete!")

                        # Display results
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Empty Spots", empty_count)
                        with col2:
                            st.metric("Filled Spots", filled_count)
                        with col3:
                            st.metric("Efficiency", f"{efficiency:.1%}")

                        st.metric("Estimated Revenue", f"${revenue:.2f}")
                        st.info(f"Current hour: {'Peak' if '7' <= peak_hour <= '19' else 'Off-peak'} ({peak_hour})")

        elif choice == "🎥 Video Analysis":
            st.title("Video Upload")
            uploaded_video = st.file_uploader("Upload parking lot video", type=['mp4', 'avi', 'mov'])

            if uploaded_video:
                # Save the uploaded video to a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
                    tmp_file.write(uploaded_video.getvalue())
                    video_path = tmp_file.name

                # Render the video analysis dashboard
                render_video_analysis_dashboard(video_path)
            else:
                st.title("Welcome to Video Analysis Dashboard")
                st.info("Please upload a video file to begin analysis.")

        elif choice == "🤖 Parking Assistant":
            st.title("🤖 Parking Assistant")

            uploaded_pdf = st.file_uploader("Upload Parking Documentation", type=["pdf"])
            if uploaded_pdf is not None:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                    tmp_file.write(uploaded_pdf.getvalue())
                    st.session_state.temp_pdf_path = tmp_file.name

                st.success("📄 Document uploaded successfully!")

                if st.button("Process Document"):
                    try:
                        embeddings_manager = EmbeddingsManager(
                            model_name="BAAI/bge-small-en",
                            device="cpu",
                            encode_kwargs={"normalize_embeddings": True},
                            qdrant_url="http://localhost:6333",
                            collection_name="vector_db"
                        )
                        result = process_pdf_document(st.session_state.temp_pdf_path, embeddings_manager)
                        st.success(result)

                        # Initialize chatbot
                        if st.session_state.chatbot_manager is None:
                            st.session_state.chatbot_manager = ChatbotManager(
                                model_name="BAAI/bge-small-en",
                                device="cpu",
                                encode_kwargs={"normalize_embeddings": True},
                                llm_model="llama3.2:1b",
                                llm_temperature=0.7,
                                qdrant_url="http://localhost:6333",
                                collection_name="vector_db"
                            )

                    except Exception as e:
                        st.error(f"Error processing document: {str(e)}")

            # Chat interface
            st.markdown("### 💬 Chat with Parking Assistant")
            if st.session_state.chatbot_manager is not None:
                # Display chat history
                for message in st.session_state.messages:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])

                # Chat input
                prompt = st.chat_input("Ask about parking...")
                if prompt:
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    with st.chat_message("user"):
                        st.markdown(prompt)

                    with st.chat_message("assistant"):
                        response = st.session_state.chatbot_manager.get_response(prompt)
                        st.markdown(response)

                    st.session_state.messages.append({"role": "assistant", "content": response})
            else:
                st.info("Please upload and process a document to start chatting.")

        elif choice == "📹 Live Camera Analysis":
            camera_integration_dashboard()
        elif choice == "📊 Data Analysis":
            render_data_analysis()
        elif choice == "💰 Pricing":
            render_unified_subscription_page()
        elif choice == "👤 User Profile":
            render_user_profile()

        elif choice == "📧 Contact":
            st.title("📬 Contact Us")
            st.markdown("""
            We'd love to hear from you! Contact our support team:

            - **Email:** urbantrafficoptimizer@gmail.com
            - **Phone:** +250 (728) 254-819
            """)

            # Contact form
            with st.form("contact_form"):
                name = st.text_input("Name")
                email = st.text_input("Email")
                message = st.text_area("Message")
                submitted = st.form_submit_button("Send Message")

                if submitted:
                    st.success("Thank you for your message! We'll get back to you soon.")


if __name__ == "__main__":
    main()
