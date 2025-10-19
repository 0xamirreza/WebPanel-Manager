from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models.panel import Panel
from app import db

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
        
        # Create new panel
        panel = Panel(
            name=name,
            domain=domain,
            panel_type=panel_type,
            login_url=login_url,
            username=username,
            password=password,
            host_provider=host_provider,
            notes=notes
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
