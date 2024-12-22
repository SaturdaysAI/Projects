import hashlib
import streamlit as st
from PIL import Image
import io

def hash_password(password):
    """Create a secure hash of the password."""
    return hashlib.sha256(str.encode(password)).hexdigest()

def create_user(username, password, email):
    try:
        c = st.session_state.cursor
        c.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)',
                 (username, hash_password(password), email))
        st.session_state.conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def check_user(username, password):
    c = st.session_state.cursor
    c.execute('SELECT username, email, profile_pic FROM users WHERE username=? AND password=?',
              (username, hash_password(password)))
    user = c.fetchone()
    if user:
        st.session_state.user = {
            'username': user[0],
            'email': user[1],
            'profile_pic': user[2]
        }
        return True
    return False

def update_password(username, new_password):
    c = st.session_state.cursor
    c.execute('UPDATE users SET password=? WHERE username=?',
              (hash_password(new_password), username))
    st.session_state.conn.commit()

def update_profile_pic(username, profile_pic):
    c = st.session_state.cursor
    c.execute('UPDATE users SET profile_pic=? WHERE username=?',
              (profile_pic, username))
    st.session_state.conn.commit()

def get_profile_pic(username):
    c = st.session_state.cursor
    c.execute('SELECT profile_pic FROM users WHERE username=?', (username,))
    result = c.fetchone()
    return result[0] if result else None

# User profile management
def render_user_profile():
    st.title("User Profile")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Profile Information")
        st.write(f"Username: {st.session_state.user['username']}")
        st.write(f"Email: {st.session_state.user['email']}")

        new_email = st.text_input("New Email")
        if st.button("Update Email"):
            c = st.session_state.cursor
            c.execute('UPDATE users SET email=? WHERE username=?',
                      (new_email, st.session_state.user['username']))
            st.session_state.conn.commit()
            st.session_state.user['email'] = new_email
            st.success("Email updated successfully!")

        st.subheader("Change Password")
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")

        if st.button("Change Password"):
            if check_user(st.session_state.user['username'], current_password):
                if new_password == confirm_password:
                    update_password(st.session_state.user['username'], new_password)
                    st.success("Password changed successfully!")
                else:
                    st.error("New passwords do not match.")
            else:
                st.error("Current password is incorrect.")

    with col2:
        st.subheader("Profile Picture")
        profile_pic = get_profile_pic(st.session_state.user['username'])
        if profile_pic:
            st.image(profile_pic, width=200)
        else:
            st.info("No profile picture uploaded yet.")

        uploaded_file = st.file_uploader("Choose a profile picture", type=["jpg", "png", "jpeg"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()

            update_profile_pic(st.session_state.user['username'], img_byte_arr)
            st.session_state.user['profile_pic'] = img_byte_arr
            st.success("Profile picture updated successfully!")
            st.rerun()
