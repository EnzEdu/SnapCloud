CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_user TEXT NOT NULL,
    s3_bucket_nome TEXT NOT NULL,
    s3_bucket_regiao TEXT NOT NULL,
    file_name TEXT NOT NULL
)