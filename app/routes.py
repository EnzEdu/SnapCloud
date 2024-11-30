from flask import render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
from app import app, db
from app.forms import EditProfileForm

# Configurando o Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'home'

# cria um usuario para simulação
class MockUser(UserMixin):
    def __init__(self, id, full_name, email, description):
        self.id = id
        self.full_name = full_name
        self.email = email
        self.description = description

mock_user = MockUser(
    id=1,
    full_name="Mock User",
    email="mockuser@example.com",
    description="Usuário fictício para testes"
)

# Função para carregar o usuário simulado
@login_manager.user_loader
def load_user(user_id):
    return mock_user if int(user_id) == mock_user.id else None

@app.route('/')
def home():
    # Login automático do usuário simulado (para testes)
    login_user(mock_user)
    return "Bem-vindo ao Sistema de Gerenciamento Multimídia (SGM)!"  # Página inicial de teste, depois vincular à um template

@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        # Atualiza os dados do usuario simulado (em produção, seria o banco de dados)
        current_user.full_name = form.full_name.data
        current_user.email = form.email.data
        current_user.description = form.description.data

        flash("Perfil atualizado com sucesso!", "success")
        return redirect(url_for('home'))  # Redireciona ao dashboard (ajuste conforme necessário)

    # Preenche o formulário com os dados do usuário simulado
    form.full_name.data = current_user.full_name
    form.email.data = current_user.email
    form.description.data = current_user.description
    return render_template('edit_profile.html', form=form)
