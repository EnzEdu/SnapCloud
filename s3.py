from flask_sqlalchemy import SQLAlchemy
import boto3

SQLITE_DATABASE = SQLAlchemy()
s3 = boto3.resource("s3")

class Arquivo(SQLITE_DATABASE.Model):
    id = SQLITE_DATABASE.Column(SQLITE_DATABASE.Integer, primary_key=True)
    id_usuario = SQLITE_DATABASE.Column(SQLITE_DATABASE.Integer)
    s3_bucket_nome = SQLITE_DATABASE.Column(SQLITE_DATABASE.String(100))
    s3_bucket_regiao = SQLITE_DATABASE.Column(SQLITE_DATABASE.String(100))
    filename = SQLITE_DATABASE.Column(SQLITE_DATABASE.String(100))