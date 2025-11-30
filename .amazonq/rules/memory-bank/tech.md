# Technology Stack

## Programming Languages
- **Python 3.x**: Backend API and AI integration
- **JavaScript (ES6+)**: Frontend application
- **SQL**: Database queries via SQLAlchemy ORM

## Backend Technologies

### Core Framework
- **FastAPI 0.110.1**: Modern Python web framework with automatic API documentation
- **Uvicorn 0.25.0**: ASGI server for running FastAPI applications
- **Pydantic 2.12.4**: Data validation and settings management
- **Python-dotenv 1.2.1**: Environment variable management

### Database
- **PostgreSQL**: Primary database (via DATABASE_URL configuration)
- **SQLAlchemy 2.0.25**: ORM for database operations
- **Alembic 1.13.1**: Database migration tool
- **psycopg2-binary 2.9.9**: PostgreSQL adapter for Python

### Authentication & Security
- **python-jose[cryptography] 3.5.0**: JWT token generation and validation
- **passlib[bcrypt] 1.7.4**: Password hashing with bcrypt
- **JWT_SECRET_KEY**: Environment-based secret for token signing

### HTTP & API
- **httpx 0.26.0**: Async HTTP client for external API calls (Hugging Face)
- **python-multipart 0.0.20**: Form data and file upload handling
- **CORS Middleware**: Configurable cross-origin resource sharing

### AI Services
- **Hugging Face Inference API**: External AI model hosting
  - **ASR Model**: openai/whisper-large-v3-turbo (speech-to-text)
  - **LLM Model**: SeaLLMs/SeaLLMs-v3-7B-Chat (conversation and feedback)
  - **TTS Model**: audo/seamless-m4t-v2-large (text-to-speech)
- **Mock Providers**: Development mode without external API calls

## Frontend Technologies

### Core Framework
- **React 19.0.0**: UI library for building interactive interfaces
- **React DOM 19.0.0**: React rendering for web
- **React Router DOM 7.5.1**: Client-side routing

### Build Tools
- **Vite 6.0.7**: Fast build tool and development server
- **@vitejs/plugin-react 4.3.4**: React support for Vite
- **PostCSS 8.4.49**: CSS processing
- **Autoprefixer 10.4.20**: Automatic vendor prefixing

### UI Framework & Components
- **Tailwind CSS 3.4.17**: Utility-first CSS framework
- **tailwindcss-animate 1.0.7**: Animation utilities
- **tailwind-merge 3.2.0**: Merge Tailwind classes intelligently
- **class-variance-authority 0.7.1**: Component variant management
- **clsx 2.1.1**: Conditional class name utility

### UI Component Libraries
- **Radix UI**: Headless UI components (20+ packages)
  - Dialog, Dropdown, Popover, Toast, Tabs, Select, etc.
- **shadcn/ui**: Pre-built components using Radix UI
- **Lucide React 0.507.0**: Icon library
- **cmdk 1.1.1**: Command menu component
- **Sonner 2.0.3**: Toast notifications
- **Vaul 1.1.2**: Drawer component

### Form Management
- **React Hook Form 7.56.2**: Form state management
- **@hookform/resolvers 5.0.1**: Validation resolvers
- **Zod 3.24.4**: Schema validation
- **input-otp 1.4.2**: OTP input component

### Utilities
- **Axios 1.8.4**: HTTP client for API requests
- **date-fns 4.1.0**: Date manipulation library
- **next-themes 0.4.6**: Theme management (dark/light mode)
- **embla-carousel-react 8.6.0**: Carousel component
- **react-resizable-panels 3.0.1**: Resizable panel layouts
- **react-day-picker 9.11.2**: Date picker component

## Development Tools

### Backend Development
```bash
# Virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload
# Or use convenience script
./start.sh

# Run tests
python test_api.py
python test_llm_parsing.py
python test_provider_selection.py
```

### Frontend Development
```bash
# Install dependencies
npm install

# Run development server
npm start
# Or
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Database Management
```bash
# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Migration message"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Project Scripts
```bash
# Start both backend and frontend
./dev-start.sh

# Stop all services
./dev-stop.sh
```

## Environment Configuration

### Backend (.env)
```
DATABASE_URL=postgresql://localhost/macca
HF_API_KEY=<your_huggingface_api_key>
HF_API_BASE_URL=https://api-inference.huggingface.co
HF_LLM_MODEL_ID=SeaLLMs/SeaLLMs-v3-7B-Chat
HF_ASR_MODEL_ID=openai/whisper-large-v3-turbo
HF_TTS_MODEL_ID=audo/seamless-m4t-v2-large
USE_MOCK_AI=false
CORS_ORIGINS=*
JWT_SECRET_KEY=<generated_secret_key>
LOG_LEVEL=INFO
```

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:8000
```

## API Documentation
- **Swagger UI**: Available at `http://localhost:8000/docs` when backend is running
- **ReDoc**: Alternative documentation at `http://localhost:8000/redoc`
- **OpenAPI Schema**: JSON schema at `http://localhost:8000/openapi.json`

## Version Control
- **Git**: Source control with `.gitignore` for Python and Node.js
- **Workspace**: VS Code workspace configuration in `macca.code-workspace`

## Logging
- **Backend**: Python logging to `logs/backend.log` with configurable LOG_LEVEL
- **Frontend**: Development logs to `logs/frontend.log`
