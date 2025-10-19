from flask import Blueprint, request, jsonify, send_file, flash, redirect, url_for
from app.models.panel import Panel
from app import db
import os
import json
import shutil
from datetime import datetime
import tempfile

backup_bp = Blueprint('backup', __name__)

@backup_bp.route('/backup/export')
def export_backup():
    """Export all panel data as JSON backup file"""
    try:
        # Get all panels
        panels = Panel.query.all()
        
        # Create backup data structure
        backup_data = {
            'version': '1.0.0',
            'exported_at': datetime.utcnow().isoformat(),
            'panels': []
        }
        
        # Convert panels to dictionary format
        for panel in panels:
            backup_data['panels'].append({
                'name': panel.name,
                'domain': panel.domain,
                'panel_type': panel.panel_type,
                'login_url': panel.login_url,
                'username': panel.username,
                'password': panel.password,
                'host_provider': panel.host_provider,
                'notes': panel.notes,
                'created_at': panel.created_at.isoformat() if panel.created_at else None
            })
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        json.dump(backup_data, temp_file, indent=2)
        temp_file.close()
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'webpanel_manager_backup_{timestamp}.json'
        
        return send_file(
            temp_file.name,
            as_attachment=True,
            download_name=filename,
            mimetype='application/json'
        )
        
    except Exception as e:
        flash(f'Error creating backup: {str(e)}', 'danger')
        return redirect(url_for('main.dashboard'))

@backup_bp.route('/backup/import', methods=['POST'])
def import_backup():
    """Import panel data from JSON backup file"""
    try:
        if 'backup_file' not in request.files:
            flash('No file selected', 'danger')
            return redirect(url_for('main.dashboard'))
        
        file = request.files['backup_file']
        if file.filename == '':
            flash('No file selected', 'danger')
            return redirect(url_for('main.dashboard'))
        
        if not file.filename.endswith('.json'):
            flash('Please select a valid JSON backup file', 'danger')
            return redirect(url_for('main.dashboard'))
        
        # Read and parse JSON file
        backup_data = json.load(file)
        
        # Validate backup format
        if 'panels' not in backup_data:
            flash('Invalid backup file format', 'danger')
            return redirect(url_for('main.dashboard'))
        
        # Check if user wants to replace existing data
        replace_existing = request.form.get('replace_existing') == 'true'
        
        if replace_existing:
            # Clear existing panels
            Panel.query.delete()
            db.session.commit()
        
        # Import panels
        imported_count = 0
        skipped_count = 0
        
        for panel_data in backup_data['panels']:
            # Check if panel already exists (by name and domain)
            existing_panel = Panel.query.filter_by(
                name=panel_data['name'],
                domain=panel_data['domain']
            ).first()
            
            if existing_panel and not replace_existing:
                skipped_count += 1
                continue
            
            # Create new panel
            panel = Panel(
                name=panel_data['name'],
                domain=panel_data['domain'],
                panel_type=panel_data['panel_type'],
                login_url=panel_data['login_url'],
                username=panel_data['username'],
                password=panel_data['password'],
                host_provider=panel_data.get('host_provider'),
                notes=panel_data.get('notes')
            )
            
            # Set created_at if available
            if panel_data.get('created_at'):
                try:
                    panel.created_at = datetime.fromisoformat(panel_data['created_at'].replace('Z', '+00:00'))
                except:
                    pass  # Use default created_at
            
            db.session.add(panel)
            imported_count += 1
        
        db.session.commit()
        
        if imported_count > 0:
            flash(f'Successfully imported {imported_count} panels', 'success')
        if skipped_count > 0:
            flash(f'Skipped {skipped_count} duplicate panels', 'warning')
        
        return redirect(url_for('main.dashboard'))
        
    except json.JSONDecodeError:
        flash('Invalid JSON file format', 'danger')
        return redirect(url_for('main.dashboard'))
    except Exception as e:
        flash(f'Error importing backup: {str(e)}', 'danger')
        return redirect(url_for('main.dashboard'))

@backup_bp.route('/backup/database')
def export_database():
    """Export the entire SQLite database file"""
    try:
        db_path = '/app/data/webpanel_manager.db'
        
        if not os.path.exists(db_path):
            flash('Database file not found', 'danger')
            return redirect(url_for('main.dashboard'))
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'webpanel_manager_database_{timestamp}.db'
        
        return send_file(
            db_path,
            as_attachment=True,
            download_name=filename,
            mimetype='application/octet-stream'
        )
        
    except Exception as e:
        flash(f'Error exporting database: {str(e)}', 'danger')
        return redirect(url_for('main.dashboard'))

@backup_bp.route('/backup/restore-database', methods=['POST'])
def restore_database():
    """Restore from SQLite database file"""
    try:
        if 'database_file' not in request.files:
            flash('No database file selected', 'danger')
            return redirect(url_for('main.dashboard'))
        
        file = request.files['database_file']
        if file.filename == '':
            flash('No database file selected', 'danger')
            return redirect(url_for('main.dashboard'))
        
        if not file.filename.endswith('.db'):
            flash('Please select a valid SQLite database file', 'danger')
            return redirect(url_for('main.dashboard'))
        
        # Backup current database
        db_path = '/app/data/webpanel_manager.db'
        backup_path = f'/app/data/webpanel_manager_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
        
        if os.path.exists(db_path):
            shutil.copy2(db_path, backup_path)
        
        # Save uploaded file
        file.save(db_path)
        
        flash('Database restored successfully. Previous database backed up.', 'success')
        return redirect(url_for('main.dashboard'))
        
    except Exception as e:
        flash(f'Error restoring database: {str(e)}', 'danger')
        return redirect(url_for('main.dashboard'))
