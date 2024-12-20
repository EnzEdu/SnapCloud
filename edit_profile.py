from flask import request, Blueprint, session, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from utilities import allowed_file
import os
import sqlite3
from utilities import DB_NAME

bp = Blueprint("edit_profile", __name__)

# TODO: adicionar profile_picture
# TODO: refatorar
@bp.route('/edit_profile', methods = ["GET", "POST"])
def edit_profile():
    if session.get("id"):
        if request.method == 'POST':
            full_name = request.form["nome"]
            username = request.form["usuario"]
            password = request.form["senha"]
            email = request.form["email"]
            description = request.form["descricao"]
            # profile_picture = request.form[] # Foto de perfil foi removida do prototipo 1

            conn = sqlite3.connect(DB_NAME, timeout = 10)
            cursor = conn.cursor()

            is_the_password_the_same = password == session["hashed_password"]

            try:
                # senha menor do que 6 caracteres ou inalterada
                if len(password) < 6 or is_the_password_the_same:
                    sql = "UPDATE users SET full_name = ?, username = ?, email = ?, description = ? WHERE id = ?"
                    cursor.execute(sql, (full_name, username, email, description, session.get('id')))

                    if len(password) < 6:
                        flash("Não são permitidas senhas com menos de 6 caracteres", "erro")
                        return redirect(url_for('dashboard.dashboard'))
                
                else:
                    sql = "UPDATE users SET full_name = ?, username = ?, email = ?, password = ?, description = ? WHERE id = ?"
                    password = generate_password_hash(password) # hasheia a nova senha
                    cursor.execute(sql, (full_name, username, email, password, description, session.get('id')))
                
                # cursor.execute("UPDATE users SET full_name = ?, username = ?, email = ?, password = ?, description = ? WHERE id = ?", (full_name, username, email, password, description, session.get('id')))
                conn.commit()
                cursor.close()
                conn.close()
                session["hashed_password"] = password # salva a nova senha ou senha inalterada na sessão

            except sqlite3.IntegrityError as e:
                flash("Nome de usuario já em uso", "erro") # testando se usar o mesmo nome de usuario vai cair aqui
                return redirect(url_for('dashboard.dashboard'))

            flash("Dados válidos atualizados com sucesso", "sucesso")
            return redirect(url_for('dashboard.dashboard'))

        if request.method == 'GET':
            # Recupera as informações para mostrar na página de edição
            conn = sqlite3.connect(DB_NAME, timeout=10)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            user = cursor.execute("select * from users where id = ?", (session.get('id'), )).fetchone()
            session["hashed_password"] = user["password"] # Solução improvisada para verificar se a senha mudou. Isso é passado para o edit_profile.html
            cursor.close()
            conn.close()

            return render_template('edit_profile.html', user = user)
    
    else:
        flash("Você não está logado!", "erro")
        return redirect(url_for('auth.login'))


def update_profile_picture(profile_picture):
    if 'profile_picture' in request.files:
        file = request.files['profile_picture']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            profile_picture = os.path.join('static/uploads', filename)
            file.save(profile_picture)
    return profile_picture