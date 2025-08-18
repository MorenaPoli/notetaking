import streamlit as st
import requests
from datetime import datetime
from typing import List, Dict, Optional
import json

# Configuration
API_BASE_URL = "http://localhost:8000/api/v1"

st.set_page_config(
    page_title="Notes App",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Helper Functions
class NotesAPI:
    @staticmethod
    def get_notes(archived=False, category_ids=None, page=1, page_size=50):
        endpoint = "archived" if archived else "active"
        params = {"page": page, "page_size": page_size}
        if category_ids:
            params["category_ids"] = category_ids
        try:
            response = requests.get(f"{API_BASE_URL}/notes/{endpoint}", params=params)
            return response.json() if response.status_code == 200 else None
        except:
            return None
    
    @staticmethod
    def get_note(note_id):
        try:
            response = requests.get(f"{API_BASE_URL}/notes/{note_id}")
            return response.json() if response.status_code == 200 else None
        except:
            return None
    
    @staticmethod
    def create_note(title, content, category_ids=None):
        data = {"title": title, "content": content, "category_ids": category_ids or []}
        try:
            response = requests.post(f"{API_BASE_URL}/notes/", json=data)
            return response.status_code == 201
        except:
            return False
    
    @staticmethod
    def update_note(note_id, title=None, content=None, category_ids=None):
        data = {}
        if title: data["title"] = title
        if content: data["content"] = content
        if category_ids is not None: data["category_ids"] = category_ids
        try:
            response = requests.put(f"{API_BASE_URL}/notes/{note_id}", json=data)
            return response.status_code == 200
        except:
            return False
    
    @staticmethod
    def delete_note(note_id):
        try:
            response = requests.delete(f"{API_BASE_URL}/notes/{note_id}")
            return response.status_code == 204
        except:
            return False
    
    @staticmethod
    def archive_note(note_id):
        try:
            response = requests.patch(f"{API_BASE_URL}/notes/{note_id}/archive")
            return response.status_code == 200
        except:
            return False
    
    @staticmethod
    def unarchive_note(note_id):
        try:
            response = requests.patch(f"{API_BASE_URL}/notes/{note_id}/unarchive")
            return response.status_code == 200
        except:
            return False
    
    @staticmethod
    def get_categories():
        try:
            response = requests.get(f"{API_BASE_URL}/categories/")
            return response.json() if response.status_code == 200 else []
        except:
            return []
    
    @staticmethod
    def create_category(name, color="#3B82F6"):
        data = {"name": name, "color": color}
        try:
            response = requests.post(f"{API_BASE_URL}/categories/", json=data)
            return response.status_code == 201
        except:
            return False
    
    @staticmethod
    def delete_category(category_id):
        try:
            response = requests.delete(f"{API_BASE_URL}/categories/{category_id}")
            return response.status_code == 204
        except:
            return False

# UI Functions
def display_note_card(note, show_archive_controls=True):
    with st.container():
        col1, col2, col3 = st.columns([6, 2, 2])
        
        with col1:
            st.subheader(note["title"])
            st.write(note["content"][:200] + "..." if len(note["content"]) > 200 else note["content"])
            
            # Display categories
            if note.get("categories"):
                category_names = [cat["name"] for cat in note["categories"]]
                st.caption(f"🏷️ {', '.join(category_names)}")
            
            st.caption(f"📅 {datetime.fromisoformat(note['created_at'].replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M')}")
        
        with col2:
            if st.button("✏️ Edit", key=f"edit_{note['id']}"):
                st.session_state.editing_note = note
                st.rerun()
        
        with col3:
            if show_archive_controls:
                if note["is_archived"]:
                    if st.button("📤 Unarchive", key=f"unarchive_{note['id']}"):
                        if NotesAPI.unarchive_note(note["id"]):
                            st.success("Note unarchived!")
                            st.rerun()
                else:
                    if st.button("📥 Archive", key=f"archive_{note['id']}"):
                        if NotesAPI.archive_note(note["id"]):
                            st.success("Note archived!")
                            st.rerun()
            
            if st.button("🗑️ Delete", key=f"delete_{note['id']}"):
                if NotesAPI.delete_note(note["id"]):
                    st.success("Note deleted!")
                    st.rerun()
        
        st.divider()

def create_note_form():
    st.subheader("📝 Create New Note")
    
    with st.form("create_note_form", clear_on_submit=True):
        title = st.text_input("Title", placeholder="Enter note title...")
        content = st.text_area("Content", height=150, placeholder="Write your note here...")
        
        categories = NotesAPI.get_categories()
        if categories:
            selected_categories = st.multiselect(
                "Categories",
                options=[(cat["id"], cat["name"]) for cat in categories],
                format_func=lambda x: x[1]
            )
            category_ids = [cat[0] for cat in selected_categories]
        else:
            category_ids = []
        
        if st.form_submit_button("Create Note", use_container_width=True):
            if title and content:
                if NotesAPI.create_note(title, content, category_ids):
                    st.success("Note created successfully!")
                    st.rerun()
                else:
                    st.error("Failed to create note")
            else:
                st.error("Please fill in both title and content")

def edit_note_form(note):
    st.subheader("✏️ Edit Note")
    
    with st.form("edit_note_form"):
        title = st.text_input("Title", value=note["title"])
        content = st.text_area("Content", value=note["content"], height=150)
        
        categories = NotesAPI.get_categories()
        current_category_ids = [cat["id"] for cat in note.get("categories", [])]
        
        if categories:
            selected_categories = st.multiselect(
                "Categories",
                options=[(cat["id"], cat["name"]) for cat in categories],
                default=[(cat["id"], cat["name"]) for cat in categories if cat["id"] in current_category_ids],
                format_func=lambda x: x[1]
            )
            category_ids = [cat[0] for cat in selected_categories]
        else:
            category_ids = []
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Save Changes", use_container_width=True):
                if title and content:
                    if NotesAPI.update_note(note["id"], title, content, category_ids):
                        st.success("Note updated successfully!")
                        del st.session_state.editing_note
                        st.rerun()
                    else:
                        st.error("Failed to update note")
                else:
                    st.error("Please fill in both title and content")
        
        with col2:
            if st.form_submit_button("Cancel", use_container_width=True):
                del st.session_state.editing_note
                st.rerun()

def manage_categories():
    st.subheader("🏷️ Manage Categories")
    
    # Create new category
    with st.expander("➕ Add New Category", expanded=False):
        with st.form("create_category_form", clear_on_submit=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                name = st.text_input("Category Name", placeholder="Enter category name...")
            with col2:
                color = st.color_picker("Color", value="#3B82F6")
            
            if st.form_submit_button("Create Category", use_container_width=True):
                if name:
                    if NotesAPI.create_category(name, color):
                        st.success("Category created!")
                        st.rerun()
                    else:
                        st.error("Failed to create category (name might already exist)")
                else:
                    st.error("Please enter a category name")
    
    # List existing categories
    categories = NotesAPI.get_categories()
    if categories:
        st.write("**Existing Categories:**")
        for category in categories:
            col1, col2, col3 = st.columns([1, 4, 1])
            with col1:
                st.markdown(f'<div style="width: 20px; height: 20px; background-color: {category["color"]}; border-radius: 3px;"></div>', unsafe_allow_html=True)
            with col2:
                st.write(category["name"])
            with col3:
                if st.button("🗑️", key=f"delete_cat_{category['id']}"):
                    if NotesAPI.delete_category(category["id"]):
                        st.success("Category deleted!")
                        st.rerun()
    else:
        st.info("No categories yet. Create your first category above!")

# Main App
def main():
    st.title("📝 Notes App")
    st.markdown("---")
    
    # Initialize session state
    if "editing_note" not in st.session_state:
        st.session_state.editing_note = None
    
    # Sidebar
    with st.sidebar:
        st.title("Navigation")
        view = st.radio("View", ["📋 Active Notes", "📦 Archived Notes", "➕ Create Note", "🏷️ Categories"])
        
        # Category filter
        categories = NotesAPI.get_categories()
        if categories and view in ["📋 Active Notes", "📦 Archived Notes"]:
            st.markdown("---")
            st.subheader("Filter by Category")
            selected_categories = st.multiselect(
                "Select Categories",
                options=[(cat["id"], cat["name"]) for cat in categories],
                format_func=lambda x: x[1],
                key="category_filter"
            )
            filter_category_ids = [cat[0] for cat in selected_categories] if selected_categories else None
        else:
            filter_category_ids = None
    
    # Main content
    if st.session_state.editing_note:
        edit_note_form(st.session_state.editing_note)
    elif view == "📋 Active Notes":
        st.header("📋 Active Notes")
        notes_data = NotesAPI.get_notes(archived=False, category_ids=filter_category_ids)
        if notes_data and notes_data.get("notes"):
            st.info(f"Showing {len(notes_data['notes'])} of {notes_data['total']} active notes")
            for note in notes_data["notes"]:
                display_note_card(note, show_archive_controls=True)
        else:
            st.info("No active notes found. Create your first note!")
    
    elif view == "📦 Archived Notes":
        st.header("📦 Archived Notes")
        notes_data = NotesAPI.get_notes(archived=True, category_ids=filter_category_ids)
        if notes_data and notes_data.get("notes"):
            st.info(f"Showing {len(notes_data['notes'])} of {notes_data['total']} archived notes")
            for note in notes_data["notes"]:
                display_note_card(note, show_archive_controls=True)
        else:
            st.info("No archived notes found.")
    
    elif view == "➕ Create Note":
        create_note_form()
    
    elif view == "🏷️ Categories":
        manage_categories()

if __name__ == "__main__":
    main()