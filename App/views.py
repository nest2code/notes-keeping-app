from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, current_user
from .models import Note, db, UserMixin, User
from .auth import login
import json
import jsonify

views = Blueprint('views', __name__)

add = 0


@views.route('/', methods=["POST", "GET"])
@login_required
def home():
    if request.method == "POST":
        description = request.form.get('description')
        note = request.form.get('note')
        if len(description) == 0 and len(note) == 0:
            flash('fields cannot be empty', category='success')
        else:

            new_note = Note(heading=description, data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note Added successfully', category='success')
            return redirect(url_for('views.index'))
    return render_template('index.html', user=current_user)


@views.route('/index', methods=["POST", "GET"])
@login_required
def index():
    if request.method == 'POST':
        try:
            note_id = request.json.get('noteId')
            if note_id:
                note = Note.query.get(note_id)
                if note:
                    if note.user_id == current_user.id:
                        db.session.delete(note)
                        db.session.commit()
                        flash('Note deleted', category='success')
                        return jsonify({'message': 'Note deleted successfully'}), 200
                    else:
                        return jsonify({'error': 'Unauthorized'}), 403
                else:
                    return jsonify({'error': 'Note not found'}), 404
            else:
                return jsonify({'error': 'Invalid request'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return render_template('home.html', user=current_user)