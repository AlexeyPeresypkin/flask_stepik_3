from flask import session, redirect, Flask, render_template
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# Настраиваем приложение Flask# - Секретный код для сессий
app.config["SECRET_KEY"] = "secret_key"  # - Имя пользователя и пароль
app.config["USERNAME"] = "test"
app.config["PASSWORD"] = "test"

db = SQLAlchemy(app)
@app.route('/')
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    # Изменим название и длину поля для пароля
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(32), nullable=False)

    @property
    def password(self):# Запретим прямое обращение к паролюraise
        AttributeError("Вам не нужно знать пароль!")

    @password.setter
    def password(self, password):# Устанавливаем пароль через этот метод
        self.password_hash = generate_password_hash(password)

    def password_valid(self, password):# Проверяем пароль через этот метод
# Функция check_password_hash превращает password в хеш и сравнивает с хранимым
        return check_password_hash(self.password_hash, password)
