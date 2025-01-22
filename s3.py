from flask_sqlalchemy import SQLAlchemy
from rds import RDS_DATABASE
import boto3

S3_BUCKET_NAME = "snapcloud-bucket-1"
S3_BUCKET_REGION = "sa-east-1"
s3 = boto3.resource("s3")

class Imagem(RDS_DATABASE.Model):
    id = RDS_DATABASE.Column(RDS_DATABASE.Integer, primary_key=True)
    s3_bucket_nome = RDS_DATABASE.Column(RDS_DATABASE.String(100))
    s3_bucket_regiao = RDS_DATABASE.Column(RDS_DATABASE.String(100))
    file_name = RDS_DATABASE.Column(RDS_DATABASE.String(100))
    file_size = RDS_DATABASE.Column(RDS_DATABASE.Integer)
    bucket_file_name = RDS_DATABASE.Column(RDS_DATABASE.String(100))
    upload_date = RDS_DATABASE.Column(RDS_DATABASE.String(100))
    mime_type = RDS_DATABASE.Column(RDS_DATABASE.String(100))
    width = RDS_DATABASE.Column(RDS_DATABASE.Integer)
    height = RDS_DATABASE.Column(RDS_DATABASE.Integer)
    color_depth = RDS_DATABASE.Column(RDS_DATABASE.Integer)
    resolution = RDS_DATABASE.Column(RDS_DATABASE.Integer)
    exif_data = RDS_DATABASE.Column(RDS_DATABASE.String(500))
    description = RDS_DATABASE.Column(RDS_DATABASE.String(1000))
    tags = RDS_DATABASE.Column(RDS_DATABASE.String(500))