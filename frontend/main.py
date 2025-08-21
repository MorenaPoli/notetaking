import streamlit as st
import requests
from datetime import datetime, date
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
    def create_note(title, content, note_type="note", priority="medium", due_date=None, category_ids=None):
        data = {
            "title": title, 
            "content": content, 
            "note_type": note_type,
            "priority": priority,
            "due_date": due_date.isoformat() if due_date else None,
            "category_ids": category_ids or []
        }
        try:
            response = requests.post(f"{API_BASE_URL}/notes/", json=data)
            return response.status_code == 201
        except:
            return False
    
    @staticmethod
    def update_note(note_id, title=None, content=None, note_type=None, priority=None, due_date=None, category_ids=None):
        data = {}
        if title: data["title"] = title
        if content: data["content"] = content
        if note_type: data["note_type"] = note_type
        if priority: data["priority"] = priority
        if due_date is not None: data["due_date"] = due_date.isoformat() if due_date else None
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
    def get_todos(status=None, priority=None, category_ids=None, page=1, page_size=50):
        params = {"page": page, "page_size": page_size}
        if status: params["status"] = status
        if priority: params["priority"] = priority
        if category_ids: params["category_ids"] = category_ids
        try:
            response = requests.get(f"{API_BASE_URL}/notes/todos", params=params)
            return response.json() if response.status_code == 200 else None
        except:
            return None
    
    @staticmethod
    def update_todo_status(note_id, status):
        try:
            response = requests.patch(f"{API_BASE_URL}/notes/{note_id}/status", params={"status": status})
            return response.status_code == 200
        except:
            return False
    
    @staticmethod
    def search_notes(search_term, include_archived=False, category_ids=None):
        params = {"include_archived": include_archived}
        if category_ids: params["category_ids"] = category_ids
        try:
            response = requests.get(f"{API_BASE_URL}/notes/search/{search_term}", params=params)
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
def get_priority_emoji(priority):
    priority_map = {"high": "🔴", "medium": "🟡", "low": "🟢"}
    return priority_map.get(priority, "🟡")

def get_status_emoji(status):
    status_map = {"pending": "⏳", "in_progress": "🔄", "completed": "✅"}
    return status_map.get(status, "⏳")

def display_note_card(note, show_archive_controls=True):
    with st.container():
        # Enhanced card with priority and type indicators
        col1, col2, col3, col4 = st.columns([6, 1, 1, 2])
        
        with col1:
            # Title with type indicator
            type_emoji = "✅" if note.get("note_type") == "todo" else "📝"
            st.subheader(f"{type_emoji} {note['title']}")
            st.write(note["content"][:200] + "..." if len(note["content"]) > 200 else note["content"])
            
            # Display metadata in a more organized way
            meta_info = []
            
            # Priority and status for todos
            if note.get("note_type") == "todo":
                priority_emoji = get_priority_emoji(note.get("priority", "medium"))
                status_emoji = get_status_emoji(note.get("todo_status", "pending"))
                meta_info.append(f"{priority_emoji} {note.get('priority', 'medium').title()}")
                meta_info.append(f"{status_emoji} {note.get('todo_status', 'pending').replace('_', ' ').title()}")
            
            # Due date
            if note.get("due_date"):
                due_date = datetime.fromisoformat(note['due_date'].replace('Z', '+00:00'))
                meta_info.append(f"📅 Due: {due_date.strftime('%Y-%m-%d')}")
            
            # Categories
            if note.get("categories"):
                category_names = [cat["name"] for cat in note["categories"]]
                meta_info.append(f"🏷️ {', '.join(category_names)}")
            
            # Created date
            created = datetime.fromisoformat(note['created_at'].replace('Z', '+00:00'))
            meta_info.append(f"📅 Created: {created.strftime('%Y-%m-%d %H:%M')}")
            
            if meta_info:
                st.caption(" • ".join(meta_info))
        
        with col2:
            if note.get("note_type") == "todo" and not note.get("is_archived"):
                # Quick status toggle for todos
                current_status = note.get("todo_status", "pending")
                if current_status == "pending":
                    if st.button("▶️", key=f"start_{note['id']}", help="Start task"):
                        if NotesAPI.update_todo_status(note["id"], "in_progress"):
                            st.success("Task started!")
                            st.rerun()
                elif current_status == "in_progress":
                    if st.button("✅", key=f"complete_{note['id']}", help="Complete task"):
                        if NotesAPI.update_todo_status(note["id"], "completed"):
                            st.success("Task completed!")
                            st.rerun()
                elif current_status == "completed":
                    if st.button("↩️", key=f"reopen_{note['id']}", help="Reopen task"):
                        if NotesAPI.update_todo_status(note["id"], "pending"):
                            st.success("Task reopened!")
                            st.rerun()
        
        with col3:
            if st.button("✏️", key=f"edit_{note['id']}", help="Edit"):
                st.session_state.editing_note = note
                st.rerun()
        
        with col4:
            col4a, col4b = st.columns(2)
            with col4a:
                if show_archive_controls:
                    if note["is_archived"]:
                        if st.button("📤", key=f"unarchive_{note['id']}", help="Unarchive"):
                            if NotesAPI.unarchive_note(note["id"]):
                                st.success("Unarchived!")
                                st.rerun()
                    else:
                        if st.button("📥", key=f"archive_{note['id']}", help="Archive"):
                            if NotesAPI.archive_note(note["id"]):
                                st.success("Archived!")
                                st.rerun()
            
            with col4b:
                if st.button("🗑️", key=f"delete_{note['id']}", help="Delete"):
                    if NotesAPI.delete_note(note["id"]):
                        st.success("Deleted!")
                        st.rerun()
        
        st.divider()

def create_note_form():
    st.subheader("📝 Create New Note/Todo")
    
    with st.form("create_note_form", clear_on_submit=True):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            title = st.text_input("Title", placeholder="Enter title...")
            content = st.text_area("Content", height=150, placeholder="Write your content here...")
        
        with col2:
            note_type = st.selectbox("Type", ["note", "todo"], format_func=lambda x: "📝 Note" if x == "note" else "✅ Todo")
            priority = st.selectbox("Priority", ["low", "medium", "high"], index=1, format_func=lambda x: f"{get_priority_emoji(x)} {x.title()}")
            
            # Due date for todos
            due_date = None
            if note_type == "todo":
                enable_due_date = st.checkbox("Set due date")
                if enable_due_date:
                    due_date = st.date_input("Due date", min_value=date.today())
        
        # Categories
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
        
        if st.form_submit_button("Create", use_container_width=True):
            if title and content:
                if NotesAPI.create_note(title, content, note_type, priority, due_date, category_ids):
                    st.success(f"{'Todo' if note_type == 'todo' else 'Note'} created successfully!")
                    st.rerun()
                else:
                    st.error("Failed to create item")
            else:
                st.error("Please fill in both title and content")

def edit_note_form(note):
    type_label = "Todo" if note.get("note_type") == "todo" else "Note"
    st.subheader(f"✏️ Edit {type_label}")
    
    with st.form("edit_note_form"):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            title = st.text_input("Title", value=note["title"])
            content = st.text_area("Content", value=note["content"], height=150)
        
        with col2:
            note_type = st.selectbox("Type", ["note", "todo"], 
                                   index=0 if note.get("note_type") == "note" else 1,
                                   format_func=lambda x: "📝 Note" if x == "note" else "✅ Todo")
            
            current_priority = note.get("priority", "medium")
            priority_options = ["low", "medium", "high"]
            priority_index = priority_options.index(current_priority) if current_priority in priority_options else 1
            priority = st.selectbox("Priority", priority_options, index=priority_index,
                                  format_func=lambda x: f"{get_priority_emoji(x)} {x.title()}")
            
            # Due date
            current_due_date = None
            if note.get("due_date"):
                current_due_date = datetime.fromisoformat(note['due_date'].replace('Z', '+00:00')).date()
            
            enable_due_date = st.checkbox("Set due date", value=current_due_date is not None)
            due_date = None
            if enable_due_date:
                due_date = st.date_input("Due date", value=current_due_date or date.today(), min_value=date.today())
        
        # Categories
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
                    if NotesAPI.update_note(note["id"], title, content, note_type, priority, due_date, category_ids):
                        st.success(f"{type_label} updated successfully!")
                        del st.session_state.editing_note
                        st.rerun()
                    else:
                        st.error(f"Failed to update {type_label.lower()}")
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

def display_todos():
    st.header("✅ Todo List")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.selectbox("Filter by Status", 
                                   ["all", "pending", "in_progress", "completed"],
                                   format_func=lambda x: "All" if x == "all" else f"{get_status_emoji(x)} {x.replace('_', ' ').title()}")
    with col2:
        priority_filter = st.selectbox("Filter by Priority", 
                                     ["all", "high", "medium", "low"],
                                     format_func=lambda x: "All" if x == "all" else f"{get_priority_emoji(x)} {x.title()}")
    with col3:
        categories = NotesAPI.get_categories()
        if categories:
            selected_categories = st.multiselect(
                "Filter by Categories",
                options=[(cat["id"], cat["name"]) for cat in categories],
                format_func=lambda x: x[1]
            )
            filter_category_ids = [cat[0] for cat in selected_categories] if selected_categories else None
        else:
            filter_category_ids = None
    
    # Get todos
    status = None if status_filter == "all" else status_filter
    priority = None if priority_filter == "all" else priority_filter
    
    todos_data = NotesAPI.get_todos(status=status, priority=priority, category_ids=filter_category_ids)
    
    if todos_data and todos_data.get("notes"):
        st.info(f"Showing {len(todos_data['notes'])} of {todos_data['total']} todos")
        
        # Group todos by status for better organization
        todos_by_status = {"pending": [], "in_progress": [], "completed": []}
        for todo in todos_data["notes"]:
            status_key = todo.get("todo_status", "pending")
            todos_by_status[status_key].append(todo)
        
        # Display todos by status
        for status_key, status_todos in todos_by_status.items():
            if status_todos:
                status_emoji = get_status_emoji(status_key)
                st.subheader(f"{status_emoji} {status_key.replace('_', ' ').title()} ({len(status_todos)})")
                for todo in status_todos:
                    display_note_card(todo, show_archive_controls=True)
    else:
        st.info("No todos found. Create your first todo!")

def search_interface():
    st.header("🔍 Search Notes & Todos")
    
    with st.form("search_form"):
        search_term = st.text_input("Search term", placeholder="Enter keywords to search...")
        
        col1, col2 = st.columns(2)
        with col1:
            include_archived = st.checkbox("Include archived items")
        
        with col2:
            categories = NotesAPI.get_categories()
            if categories:
                selected_categories = st.multiselect(
                    "Filter by Categories",
                    options=[(cat["id"], cat["name"]) for cat in categories],
                    format_func=lambda x: x[1]
                )
                filter_category_ids = [cat[0] for cat in selected_categories] if selected_categories else None
            else:
                filter_category_ids = None
        
        if st.form_submit_button("Search", use_container_width=True):
            if search_term:
                results = NotesAPI.search_notes(search_term, include_archived, filter_category_ids)
                
                if results:
                    st.success(f"Found {len(results)} results for '{search_term}'")
                    for result in results:
                        display_note_card(result, show_archive_controls=True)
                else:
                    st.info(f"No results found for '{search_term}'")
            else:
                st.error("Please enter a search term")

# Main App
def main():
    st.title("📝 Notes App")
    st.markdown("---")
    
    # Initialize session state
    if "editing_note" not in st.session_state:
        st.session_state.editing_note = None
    
    # Sidebar
    with st.sidebar:
        st.title("📝 Notes & Todos")
        view = st.radio("Navigation", [
            "📋 Active Notes", 
            "✅ Todo List", 
            "📦 Archived Items", 
            "🔍 Search", 
            "➕ Create New", 
            "🏷️ Categories"
        ])
        
        # Category filter for relevant views
        categories = NotesAPI.get_categories()
        if categories and view in ["📋 Active Notes", "📦 Archived Items"]:
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
        
        # Quick stats
        st.markdown("---")
        st.subheader("📊 Quick Stats")
        try:
            active_notes = NotesAPI.get_notes(archived=False, page_size=1)
            todos_data = NotesAPI.get_todos(page_size=1)
            archived_notes = NotesAPI.get_notes(archived=True, page_size=1)
            
            if active_notes:
                st.metric("Active Notes", active_notes.get('total', 0))
            if todos_data:
                st.metric("Total Todos", todos_data.get('total', 0))
            if archived_notes:
                st.metric("Archived Items", archived_notes.get('total', 0))
        except:
            st.caption("Stats unavailable")
    
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
    
    elif view == "✅ Todo List":
        display_todos()
    
    elif view == "📦 Archived Items":
        st.header("📦 Archived Items")
        notes_data = NotesAPI.get_notes(archived=True, category_ids=filter_category_ids)
        if notes_data and notes_data.get("notes"):
            st.info(f"Showing {len(notes_data['notes'])} of {notes_data['total']} archived items")
            for note in notes_data["notes"]:
                display_note_card(note, show_archive_controls=True)
        else:
            st.info("No archived items found.")
    
    elif view == "🔍 Search":
        search_interface()
    
    elif view == "➕ Create New":
        create_note_form()
    
    elif view == "🏷️ Categories":
        manage_categories()

if __name__ == "__main__":
    main()