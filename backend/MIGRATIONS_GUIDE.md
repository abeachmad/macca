# Database Migrations Guide

## Initial Setup

### 1. Install PostgreSQL

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

**Ubuntu/Debian:**
```bash
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**Windows:**
Download and install from https://www.postgresql.org/download/windows/

### 2. Create Database

```bash
# Using psql
psql -U postgres
CREATE DATABASE macca;
CREATE USER macca_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE macca TO macca_user;
\q

# Or using createdb command
createdb macca
```

### 3. Configure Environment

Edit `backend/.env`:
```bash
DATABASE_URL=postgresql://macca_user:your_password@localhost/macca
```

## Running Migrations

### First Time Setup

```bash
cd backend

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Generate initial migration
alembic revision --autogenerate -m "Initial schema"

# Review the generated migration in app/db/migrations/versions/
# Make sure it looks correct

# Apply migration
alembic upgrade head

# Verify
alembic current
```

### After Model Changes

Whenever you modify models in `app/db/models.py`:

```bash
# Generate migration
alembic revision --autogenerate -m "Description of changes"

# Review the migration file
# Check app/db/migrations/versions/<timestamp>_description.py

# Apply migration
alembic upgrade head
```

## Common Migration Commands

```bash
# Show current version
alembic current

# Show migration history
alembic history

# Upgrade to latest
alembic upgrade head

# Upgrade to specific version
alembic upgrade <revision_id>

# Downgrade one version
alembic downgrade -1

# Downgrade to specific version
alembic downgrade <revision_id>

# Downgrade to base (empty database)
alembic downgrade base
```

## Troubleshooting

### "Target database is not up to date"

```bash
# Check current version
alembic current

# Check what migrations exist
alembic history

# Upgrade to head
alembic upgrade head
```

### "Can't locate revision identified by..."

```bash
# Stamp the database with current version
alembic stamp head

# Or start fresh
alembic downgrade base
alembic upgrade head
```

### "Multiple head revisions are present"

```bash
# Merge the heads
alembic merge heads -m "Merge migrations"
alembic upgrade head
```

### Connection Errors

Check your `DATABASE_URL` in `.env`:
```bash
# Format
postgresql://username:password@host:port/database

# Example
postgresql://macca_user:password123@localhost:5432/macca
```

## Development Workflow

### Using SQLite for Development

For quick development without PostgreSQL:

```bash
# In .env
DATABASE_URL=sqlite:///./dev.db

# Run migrations
alembic upgrade head

# Start server
./start.sh
```

### Using PostgreSQL for Production

```bash
# In .env
DATABASE_URL=postgresql://user:pass@localhost/macca

# Run migrations
alembic upgrade head

# Start server
./start.sh
```

## Testing

Tests use SQLite automatically:

```bash
# test_api.py sets DATABASE_URL to sqlite:///./test.db
python test_api.py
```

## Schema Overview

Current database schema:

### Users Table
- `id` (String/UUID) - Primary key
- `email` (String) - Unique, indexed
- `password_hash` (String) - Hashed password
- `name` (String) - User's name
- `goal` (String) - Learning goal
- `level` (String) - English level (A1-C2)
- `explanation_language` (String) - Preferred language for explanations
- `created_at` (DateTime) - Account creation timestamp
- `updated_at` (DateTime) - Last update timestamp

### Sessions Table
- `id` (String/UUID) - Primary key
- `user_id` (String/UUID) - Foreign key to users
- `mode` (String) - Session mode (live_conversation, guided_lesson, pronunciation_coach)
- `topic` (String) - Session topic
- `lesson_id` (String) - Associated lesson ID
- `started_at` (DateTime) - Session start time
- `ended_at` (DateTime) - Session end time
- `duration_seconds` (Integer) - Session duration
- `summary` (Text) - Session summary

### Utterances Table
- `id` (String/UUID) - Primary key
- `session_id` (String/UUID) - Foreign key to sessions
- `user_id` (String/UUID) - Foreign key to users
- `role` (String) - Speaker role (user, assistant)
- `audio_url` (String) - URL to audio file
- `transcript` (Text) - Text transcript
- `raw_llm_json` (JSON) - Raw LLM response (for assistant)
- `created_at` (DateTime) - Creation timestamp

### FeedbackIssues Table
- `id` (String/UUID) - Primary key
- `user_id` (String/UUID) - Foreign key to users
- `session_id` (String/UUID) - Foreign key to sessions
- `utterance_id` (String/UUID) - Foreign key to utterances
- `type` (String) - Issue type (grammar, vocabulary, pronunciation)
- `issue_code` (String) - Specific issue code
- `detail` (JSON) - Detailed issue information
- `created_at` (DateTime) - Creation timestamp

### VocabularyItems Table
- `id` (String/UUID) - Primary key
- `user_id` (String/UUID) - Foreign key to users
- `word` (String) - Vocabulary word
- `translation` (String) - Translation
- `example` (Text) - Example sentence
- `source` (String) - Source (conversation, lesson, manual)
- `strength` (Float) - Learning strength (0-1)
- `last_reviewed_at` (DateTime) - Last review timestamp
- `created_at` (DateTime) - Creation timestamp

## Backup and Restore

### Backup

```bash
# PostgreSQL
pg_dump -U macca_user macca > backup.sql

# Or with compression
pg_dump -U macca_user macca | gzip > backup.sql.gz
```

### Restore

```bash
# PostgreSQL
psql -U macca_user macca < backup.sql

# Or from compressed
gunzip -c backup.sql.gz | psql -U macca_user macca
```

## Production Deployment

### Pre-deployment Checklist

- [ ] Backup production database
- [ ] Test migrations on staging database
- [ ] Review all migration files
- [ ] Check for data loss in down migrations
- [ ] Verify foreign key constraints
- [ ] Test rollback procedure

### Deployment Steps

```bash
# 1. Backup
pg_dump -U user production_db > backup_$(date +%Y%m%d).sql

# 2. Run migrations
alembic upgrade head

# 3. Verify
alembic current

# 4. Test application
curl http://localhost:8000/api/

# 5. If issues, rollback
alembic downgrade -1
```

## References

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
