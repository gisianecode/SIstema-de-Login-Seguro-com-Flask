from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'uma-chave-muito-segura-e-secreta-aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# --- MODELO DO USUÁRIO (BANCO DE DADOS) ---
class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    senha_hash = db.Column(db.String(256), nullable=False)
    
    # Sistema de Bloqueio (Segurança)
    tentativas_falhas = db.Column(db.Integer, default=0)
    bloqueado_ate = db.Column(db.DateTime, nullable=True)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# --- VALIDAÇÃO FORTE DE SENHA ---
def senha_eh_forte(senha):
    if len(senha) < 8: return False
    if not any(c.isupper() for c in senha): return False
    if not any(c.islower() for c in senha): return False
    if not any(c.isdigit() for c in senha): return False
    return True

# --- ROTAS ---

@app.route('/')
@login_required
def home():
    return f"<h1>Bem-vindo, {current_user.username}! Você está em uma área segura.</h1><a href='/logout'>Sair</a>"

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        senha = request.form.get('senha')
        
        if Usuario.query.filter_by(username=username).first():
            flash('Usuário já existe.', 'danger')
            return redirect(url_for('cadastro'))
            
        if not senha_eh_forte(senha):
            flash('A senha deve ter no mínimo 8 caracteres, incluindo maiúsculas, minúsculas e números.', 'danger')
            return redirect(url_for('cadastro'))
            
        # Criptografia segura da senha (Gera o Hash)
        nova_senha_hash = generate_password_hash(senha, method='scrypt')
        novo_usuario = Usuario(username=username, senha_hash=nova_senha_hash)
        
        db.session.add(novo_usuario)
        db.session.commit()
        
        flash('Cadastro realizado com sucesso! Faça o login.', 'success')
        return redirect(url_for('login'))
        
    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        senha = request.form.get('senha')
        
        # Mensagem genérica para evitar enumeração de usuários
        mensagem_erro_generica = "Usuário ou senha incorretos."
        
        usuario = Usuario.query.filter_by(username=username).first()
        
        if usuario:
            # Verifica se a conta está bloqueada por tempo
            if usuario.bloqueado_ate and datetime.now() < usuario.bloqueado_ate:
                minutos_restantes = int((usuario.bloqueado_ate - datetime.now()).total_seconds() / 60) + 1
                flash(f"Conta temporariamente bloqueada. Tente novamente em {minutos_restantes} minutos.", 'danger')
                return redirect(url_for('login'))
            
            # Verifica a senha
            if check_password_hash(usuario.senha_hash, senha):
                # Sucesso: Reseta o contador de falhas
                usuario.tentativas_falhas = 0
                usuario.bloqueado_ate = None
                db.session.commit()
                
                login_user(usuario, remember=True) # Login persistente (Session Cookie)
                return redirect(url_for('home'))
            else:
                # Erro: Incrementa falhas
                usuario.tentativas_falhas += 1
                if usuario.tentativas_falhas >= 5:
                    usuario.bloqueado_ate = datetime.now() + timedelta(minutes=15) # Bloqueia por 15 min
                    flash("Múltiplas tentativas incorretas. Conta bloqueada por 15 minutos.", 'danger')
                else:
                    flash(mensagem_erro_generica, 'danger')
                db.session.commit()
        else:
            # Mesmo se o usuário não existir, mostramos o erro genérico para o hacker não saber se o usuário é real
            flash(mensagem_erro_generica, 'danger')
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Cria o banco de dados automaticamente
    app.run(debug=True)