from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models.panel import Panel
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def dashboard():
    panels = Panel.query.all()
    return render_template('dashboard.html', panels=panels)
