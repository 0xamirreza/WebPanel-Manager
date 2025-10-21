# WebPanel Manager (WPM)

A modern, self-hosted web panel manager built with Flask, Bootstrap, and SQLite3. Centralize and manage multiple hosting control panels from a single, beautiful dashboard.

[![WebPanel Manager](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/0xamirreza/WebPanel-Manager)
[![Python](https://img.shields.io/badge/python-3.11+-green.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/flask-2.3.3-red.svg)](https://flask.palletsprojects.com)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://docker.com)

## ✨ Features

### 🎯 **Core Functionality**
- **Centralized Dashboard**: Manage all your web panels from one beautiful interface
- **Multiple Panel Support**: cPanel, DirectAdmin, Plesk, CyberPanel, Virtualmin, Webmin, Froxlor, AA Panel
- **Auto-Login**: One-click login to your panels with automatic form submission (Coming Soon)
- **CRUD Operations**: Add, edit, delete panel configurations with ease

### 🔐 **Security & Privacy**
- **Password Visibility Toggle**: Show/hide passwords with eye icon
- **One-Click Copy**: Copy usernames and passwords to clipboard
- **Secure Storage**: Passwords stored securely in SQLite database
- **Data Persistence**: All data persists between Docker restarts
- **Backup & Restore**: Export/import data with JSON or database file backup
- **Environment Configuration**: Secure `.env` file support for sensitive data

### 🎨 **User Experience**
- **Modern UI**: Bootstrap 5 with FontAwesome icons
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Interactive Cards**: Hover effects and smooth animations
- **Modal Dialogs**: Professional info and confirmation modals
- **Copy Feedback**: Visual feedback for successful clipboard operations

### 📊 **Panel Management**
- **Host Provider Tracking**: Record which hosting provider you're using
- **Notes System**: Add custom notes and reminders for each panel
- **Panel Information**: Detailed view with all panel data
- **Quick Actions**: Login, Info, Edit, Delete buttons for each panel

## 🚀 Quick Start

### Using Docker Compose (Recommended)

1. **Clone the repository:**
```bash
git clone https://github.com/0xamirreza/WebPanel-Manager.git
cd WebPanel-Manager
```

2. **Configure environment:**
```bash
cp env.example .env
# Edit .env file and change SECRET_KEY to a secure random string
```

3. **Run the application:**
```bash
./run.sh
```

4. **Access the dashboard:**
Open your browser and go to: `http://localhost:44553`

### Manual Installation

1. **Install Python 3.11+**
2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
python run.py
```

4. **Access the dashboard:**
Open your browser and go to: `http://localhost:44553`

## 📖 Usage Guide

### Adding a New Panel

1. Click **"Add New Panel"** on the dashboard
2. Fill in the required information:
   - **Panel Name**: A friendly name (e.g., "My cPanel Server")
   - **Domain**: The domain associated with the panel
   - **Panel Type**: Select from supported panel types
   - **Login URL**: Full URL to the panel login page
   - **Username & Password**: Your panel credentials
   - **Host Provider**: Optional hosting provider name
   - **Notes**: Optional notes and reminders

3. Click **"Add Panel"** to save

### Managing Panels

- **Login**: Click the green "Login" button to auto-login
- **View Details**: Click the blue info icon to see all panel information
- **Edit**: Click the edit icon to modify panel details
- **Delete**: Click the delete icon to remove a panel
- **Copy Credentials**: Click the copy icons to copy username/password

### Password Management

- **Show Password**: Click the eye icon to reveal the password
- **Hide Password**: Click the eye-slash icon to hide the password
- **Copy Password**: Click the copy icon to copy password to clipboard

### Backup & Restore

#### Creating Backups

1. **JSON Backup**: Click "Backup" → "Export JSON Backup" to download a JSON file containing all panel data
2. **Database Backup**: Click "Backup" → "Export Database File" to download the complete SQLite database

#### Restoring Data

1. **From JSON**: Click "Restore" → "Restore from JSON" and select a JSON backup file
   - Choose whether to replace existing panels or skip duplicates
   - Safe for selective restoration
2. **From Database**: Click "Restore" → "Restore Database" and select a database file
   - Completely replaces current database
   - Previous database is automatically backed up
   - Use with caution as this overwrites all current data

#### Backup Best Practices

- **Regular Backups**: Create backups before major changes
- **Multiple Formats**: Use both JSON and database backups for redundancy
- **Secure Storage**: Store backups in a secure location
- **Version Control**: Keep multiple backup versions with timestamps

## 🎛️ Supported Panel Types

| Panel Type | Description |
|------------|-------------|
| **cPanel** | Most popular web hosting control panel |
| **DirectAdmin** | Lightweight alternative to cPanel |
| **Plesk** | Professional hosting control panel |
| **CyberPanel** | Open-source web hosting control panel |
| **Virtualmin** | Web-based system administration |
| **Webmin** | System administration interface |
| **Froxlor** | Lightweight server management panel |
| **AA Panel** | Chinese hosting control panel |
| **Other** | Generic panel type for custom panels |

## 🏗️ Project Structure

```
WebPanel-Manager/
├── app/
│   ├── models/
│   │   └── panel.py          # Panel database model
│   ├── views/
│   │   ├── main.py           # Dashboard routes
│   │   └── panels.py         # Panel CRUD routes
│   ├── templates/
│   │   ├── dashboard.html    # Main dashboard
│   │   ├── add_panel.html    # Add panel form
│   │   ├── edit_panel.html   # Edit panel form
│   │   └── auto_login.html   # Auto-login page
│   ├── static/
│   │   ├── css/
│   │   │   └── main.css      # Custom styles
│   │   ├── js/
│   │   │   └── main.js       # JavaScript functionality
│   │   └── img/
│   │       └── favicon.ico   # Website favicon
│   └── __init__.py           # Flask app factory
├── data/
│   └── webpanel_manager.db   # SQLite database
├── Dockerfile                # Docker configuration
├── docker-compose.yml        # Docker Compose setup
├── requirements.txt          # Python dependencies
├── run.py                    # Application entry point
├── run.sh                    # Quick start script
└── README.md                 # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root (copy from `env.example`):

```bash
cp env.example .env
```

Required variables:
- `SECRET_KEY`: Flask secret key (change in production - make it long and random)
- `FLASK_ENV`: Flask environment (production/development)

Optional variables:
- `APP_HOST`: Application host (default: 0.0.0.0)
- `APP_PORT`: Application port (default: 44553)

### Database

The application uses SQLite3 for simplicity and portability:
- **Location**: `./data/webpanel_manager.db`
- **Persistence**: Data persists between Docker restarts
- **Backup**: Regular backups recommended

## 🐳 Docker Configuration

### Volumes
- `./data:/app/data` - Database persistence

### Ports
- `44553:44553` - Web interface

### Health Check
- Automatic health monitoring
- Restart on failure

## 🔒 Security Considerations

### Production Deployment

1. **Change Secret Key**: Update `SECRET_KEY` in `.env` file
2. **Use HTTPS**: Set up reverse proxy with SSL certificate
3. **Database Encryption**: Consider encrypting stored passwords
4. **Regular Backups**: Backup database regularly
5. **Access Control**: Consider adding authentication

### Data Protection

- Passwords are stored in the database (consider encryption for production)
- Database file is excluded from version control
- Use secure hosting environment

## 🛠️ Development

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- Git

### Local Development

1. **Clone repository**
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Run application**: `python run.py`
4. **Access**: `http://localhost:44553`

### Building Docker Image

```bash
docker-compose build --no-cache
```

## 📝 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Dashboard |
| GET | `/panels/add` | Add panel form |
| POST | `/panels/add` | Create new panel |
| GET | `/panels/edit/<id>` | Edit panel form |
| POST | `/panels/edit/<id>` | Update panel |
| POST | `/panels/delete/<id>` | Delete panel |
| GET | `/panels/login/<id>` | Auto-login to panel |
| GET | `/backup/export` | Export JSON backup |
| POST | `/backup/import` | Import JSON backup |
| GET | `/backup/database` | Export database file |
| POST | `/backup/restore-database` | Restore database file |

## 🤝 Contributing

1. Fork the [repository](https://github.com/0xamirreza/WebPanel-Manager)
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📋 Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed list of changes and version history.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Flask** - Web framework
- **Bootstrap** - CSS framework
- **FontAwesome** - Icons
- **SQLite** - Database
- **Docker** - Containerization

---

**Made with ❤️ by [@0xamirreza](https://github.com/0xamirreza)**
