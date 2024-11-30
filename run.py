from app import app, db

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Cria as tabelas do banco de dados
    app.run(debug=True)
