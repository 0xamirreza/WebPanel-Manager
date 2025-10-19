# Changelog

## [1.0.0] - 2024-12-19

### Added
- Web panel manager dashboard
- Support for multiple panel types (cPanel, DirectAdmin, Plesk, etc.)
- Add, edit, delete panel functionality
- Auto-login to panels
- Password visibility toggle
- Copy username/password to clipboard
- Host provider and notes fields
- Panel information modal
- **Backup & Restore functionality**
  - Export JSON backup with all panel data
  - Export complete SQLite database file
  - Import JSON backup with duplicate handling
  - Restore from database file with automatic backup
- **Environment Configuration**
  - `.env` file support for secure configuration
  - Environment variable management
  - Secure secret key handling
- Docker containerization
- Data persistence with SQLite
- Responsive Bootstrap UI
- FontAwesome icons
- Custom favicon

### Technical
- Flask MVT architecture
- SQLAlchemy ORM
- Docker Compose setup with `.env` support
- Health checks
- Non-root user execution
- Static file separation
- Environment variable configuration
