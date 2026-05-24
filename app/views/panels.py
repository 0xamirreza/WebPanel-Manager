from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models.panel import Panel
from app import db
from app.utils.date_utils import parse_jalali_date

panels_bp = Blueprint('panels', __name__)

@panels_bp.route('/add', methods=['GET', 'POST'])
def add_panel():
    if request.method == 'POST':
        name = request.form['name']
        domain = request.form['domain']
        panel_type = request.form['panel_type']
        login_url = request.form['login_url']
        username = request.form['username']
        password = request.form['password']
        host_provider = request.form.get('host_provider', '')
        notes = request.form.get('notes', '')
        start_date_raw = request.form.get('start_date', '').strip()
        end_date_raw = request.form.get('end_date', '').strip()
        try:
            start_date = parse_jalali_date(start_date_raw) if start_date_raw else None
            end_date = parse_jalali_date(end_date_raw) if end_date_raw else None
        except Exception:
            flash('Invalid Jalali date format. Use YYYY/MM/DD.', 'danger')
            return redirect(url_for('panels.add_panel'))

        if start_date and end_date and end_date < start_date:
            flash('End date cannot be earlier than start date.', 'danger')
            return redirect(url_for('panels.add_panel'))
        
        # Create new panel
        panel = Panel(
            name=name,
            domain=domain,
            panel_type=panel_type,
            login_url=login_url,
            username=username,
            password=password,
            host_provider=host_provider,
            notes=notes,
            start_date=start_date,
            end_date=end_date
        )
        
        db.session.add(panel)
        db.session.commit()
        
        flash('Panel added successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('add_panel.html')

@panels_bp.route('/edit/<int:panel_id>', methods=['GET', 'POST'])
def edit_panel(panel_id):
    panel = Panel.query.get_or_404(panel_id)
    
    if request.method == 'POST':
        panel.name = request.form['name']
        panel.domain = request.form['domain']
        panel.panel_type = request.form['panel_type']
        panel.login_url = request.form['login_url']
        panel.username = request.form['username']
        panel.password = request.form['password']
        panel.host_provider = request.form.get('host_provider', '')
        panel.notes = request.form.get('notes', '')
        start_date_raw = request.form.get('start_date', '').strip()
        end_date_raw = request.form.get('end_date', '').strip()
        try:
            panel.start_date = parse_jalali_date(start_date_raw) if start_date_raw else None
            panel.end_date = parse_jalali_date(end_date_raw) if end_date_raw else None
        except Exception:
            flash('Invalid Jalali date format. Use YYYY/MM/DD.', 'danger')
            return redirect(url_for('panels.edit_panel', panel_id=panel.id))

        if panel.start_date and panel.end_date and panel.end_date < panel.start_date:
            flash('End date cannot be earlier than start date.', 'danger')
            return redirect(url_for('panels.edit_panel', panel_id=panel.id))
        
        db.session.commit()
        flash('Panel updated successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('edit_panel.html', panel=panel)

@panels_bp.route('/delete/<int:panel_id>', methods=['POST'])
def delete_panel(panel_id):
    panel = Panel.query.get_or_404(panel_id)
    db.session.delete(panel)
    db.session.commit()
    flash('Panel deleted successfully!', 'success')
    return redirect(url_for('main.dashboard'))

@panels_bp.route('/login/<int:panel_id>')
def login_panel(panel_id):
    panel = Panel.query.get_or_404(panel_id)
    return render_template('auto_login.html', panel=panel)
