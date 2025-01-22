from flask_sqlalchemy import SQLAlchemy

# Instancia o componente de banco de dados
RDS_DATABASE = SQLAlchemy()

class Usuario(RDS_DATABASE.Model):
    id = RDS_DATABASE.Column(RDS_DATABASE.Integer, primary_key=True)
    full_name = RDS_DATABASE.Column(RDS_DATABASE.String(100))
    username = RDS_DATABASE.Column(RDS_DATABASE.String(100))
    password = RDS_DATABASE.Column(RDS_DATABASE.String(300))
    email = RDS_DATABASE.Column(RDS_DATABASE.String(100))
    description = RDS_DATABASE.Column(RDS_DATABASE.String(256))
    creation_date = RDS_DATABASE.Column(RDS_DATABASE.String(100))
    id_profile_picture = RDS_DATABASE.Column(RDS_DATABASE.Integer)
