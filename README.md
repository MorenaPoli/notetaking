# 📝 Notes & Todo App

A modern, full-featured note-taking and todo management web application built with FastAPI and Streamlit.

## ✨ Features

### 📋 Notes Management
- Create, edit, and delete notes
- Rich text content support
- Archive/unarchive functionality
- Category organization with color coding
- Search functionality across all notes

### ✅ Todo Management
- Create todos with different priority levels (High 🔴, Medium 🟡, Low 🟢)
- Task status tracking (Pending ⏳, In Progress 🔄, Completed ✅)
- Due date support for time-sensitive tasks
- Quick status updates with one-click buttons
- Filter todos by status, priority, and categories

### 🏷️ Category System
- Create custom categories with color coding
- Assign multiple categories to notes/todos
- Filter content by categories
- Visual category indicators

### 🔍 Advanced Search
- Full-text search across titles and content
- Filter search results by categories
- Include/exclude archived items in search

### 📊 Dashboard Features
- Quick stats overview (active notes, todos, archived items)
- Organized todo list grouped by status
- Enhanced UI with emojis and visual indicators
- Responsive design for better user experience

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Git (for cloning the repository)

### Installation

1. **Clone the repository:**
```bash
git clone <your-repo-url>
cd notetaking
```

2. **Start the application:**
```bash
# Make setup script executable (Linux/Mac)
chmod +x setup.sh
./setup.sh

# Or run directly with Docker Compose
docker-compose up --build -d
```

3. **Access the application:**
- **Frontend (Streamlit):** http://localhost:8501
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

## 🏗️ Architecture

### Backend (FastAPI)
- **Framework:** FastAPI with async support
- **Database:** PostgreSQL with SQLAlchemy ORM
- **API Design:** RESTful API with automatic OpenAPI documentation
- **Features:** CORS enabled, pagination, filtering, search

### Frontend (Streamlit)
- **Framework:** Streamlit for rapid UI development
- **Features:** Interactive forms, real-time updates, responsive layout
- **Navigation:** Sidebar navigation with quick stats
- **UI/UX:** Modern design with emojis and visual indicators

### Database Schema
- **Notes:** Title, content, type (note/todo), priority, status, due_date, timestamps
- **Categories:** Name, color, timestamps
- **Many-to-Many:** Notes ↔ Categories relationship

## 📱 Usage Guide

### Creating Content
1. Navigate to "➕ Create New" in the sidebar
2. Choose between Note 📝 or Todo ✅
3. Set priority level and due date (for todos)
4. Assign categories for organization
5. Click "Create" to save

### Managing Todos
1. Go to "✅ Todo List" to see all todos organized by status
2. Use quick action buttons:
   - ▶️ Start a pending task
   - ✅ Complete an in-progress task
   - ↩️ Reopen a completed task
3. Filter by status, priority, or categories

### Search & Organization
1. Use "🔍 Search" to find specific content
2. Filter by categories in "📋 Active Notes" view
3. Manage categories in "🏷️ Categories" section
4. Archive completed items to keep workspace clean

## 🛠️ Development

### Project Structure
```
notetaking/
├── backend/
│   ├── app/
│   │   ├── controllers/     # API endpoints
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   ├── repositories/   # Data access layer
│   │   └── utils/          # Utilities
│   ├── requirements.txt
│   └── dockerfile.txt
├── frontend/
│   ├── main.py            # Streamlit app
│   ├── requirements.txt
│   └── dockerfile.txt
├── docker-compose.yml
└── setup.sh
```

### API Endpoints
- `GET /api/v1/notes/active` - Get active notes
- `GET /api/v1/notes/todos` - Get todos with filtering
- `POST /api/v1/notes/` - Create note/todo
- `PUT /api/v1/notes/{id}` - Update note/todo
- `PATCH /api/v1/notes/{id}/status` - Update todo status
- `GET /api/v1/notes/search/{term}` - Search notes
- `GET /api/v1/categories/` - Get categories

### Environment Variables
Create a `.env` file in the backend directory:
```env
DATABASE_URL=postgresql://notes_user:notes_password@localhost:5432/notes_db
API_TITLE=Notes API
DEBUG=true
```

## 🐳 Docker Configuration

The application uses Docker Compose with three services:
- **db:** PostgreSQL database
- **backend:** FastAPI application
- **frontend:** Streamlit application

All services are configured with health checks and proper dependencies.

## 🔧 Troubleshooting

### Common Issues
1. **Database connection errors:** Ensure PostgreSQL is running and credentials are correct
2. **Port conflicts:** Check if ports 8000, 8501, or 5432 are already in use
3. **API connection issues:** Verify backend is running at http://localhost:8000

### Logs
```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Reset Database
```bash
docker-compose down -v
docker-compose up --build -d
```

## 🎯 Future Enhancements

- [ ] Data export functionality (JSON, CSV)
- [ ] Email notifications for due dates
- [ ] Collaborative features (sharing, comments)
- [ ] Mobile app version
- [ ] Advanced filtering and sorting options
- [ ] Bulk operations (archive, delete, categorize)

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

**Enjoy organizing your notes and todos! 📝✅**