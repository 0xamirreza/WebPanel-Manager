# Changelog

## [2.0.0] - 2026-05-24

### Added
- **Offline-ready frontend assets**
  - Removed CDN dependency for Bootstrap, Bootstrap Icons, and Font Awesome
  - Added local vendor assets under `app/static/vendor`
  - Added asset version query string (`?v={{ version }}`) for cache busting
- **Service period tracking**
  - Added `start_date` and `end_date` fields for each panel
  - Added `remaining_days` display in dashboard cards and panel details modal
  - Added form validation for invalid date ranges
- **Jalali (Shamsi) date support**
  - Jalali date input format for service dates (`YYYY/MM/DD`)
  - Jalali date/time rendering in dashboard and panel detail modal
  - UTC to Tehran timezone conversion for created time display

### Changed
- Updated project version to `2.0.0`
- Improved `run.sh` to support both:
  - `docker compose` (Compose v2 plugin)
  - `docker-compose` (legacy binary)

### Technical
- Added lightweight startup schema migration for existing SQLite databases:
  - Auto-add `start_date` column if missing
  - Auto-add `end_date` column if missing
- Added `jdatetime` dependency for Jalali calendar conversion

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
- Footer with project information

### Technical
- Flask MVT architecture
- SQLAlchemy ORM
- Docker Compose setup with `.env` support
- Health checks
- Non-root user execution
- Static file separation
- Environment variable configuration
