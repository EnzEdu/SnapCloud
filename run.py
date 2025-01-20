from utilities import create_tables
import os
from utilities import create_folders

if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()  # Cria as tabelas do banco de dados
    # app.run(debug=True)
    create_tables(drop_data_base=True)
    create_folders()