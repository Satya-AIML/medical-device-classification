import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

project_name = "Bio_Device_Classifier"

# List of files to create for the modular code structure
list_of_files = [
    ".github/workflows/.gitkeep",  # For GitHub workflows
    f"src/{project_name}/__init__.py",  # Main init for the project
    f"src/{project_name}/data_processing/__init__.py",  # Init for data processing module
    f"src/{project_name}/data_processing/data_processing.py",  # Data processing logic
    f"src/{project_name}/embedding/__init__.py",  # Init for embedding module
    f"src/{project_name}/embedding/embedding.py",  # Embedding logic
    f"src/{project_name}/pinecone_utils/__init__.py",  # Init for Pinecone utils module
    f"src/{project_name}/pinecone_utils/pinecone_utils.py",  # Pinecone operations
    f"src/{project_name}/model/__init__.py",  # Init for model module
    f"src/{project_name}/model/model.py",  # Model logic (split, accuracy, etc.)
    f"src/{project_name}/config/__init__.py",  # Configuration management
    f"src/{project_name}/config/configuration.py",  # Configuration settings
    f"src/{project_name}/constants/__init__.py",
    f"src/{project_name}/constants/constants.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/utils/common.py",
    f"src/{project_name}/logging/__init__.py",
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/config/configuration.py",
    f"src/{project_name}/pipeline/configuration.py",
    f"src/{project_name}/pipeline/__init__.py",
    f"src/{project_name}/entity/__init__.py",
    "app.py",  # Web app entry point (optional)
    "main.py",  # Main script to run the project
    "requirements.txt",  # External libraries requirements
    "Dockerfile",  # Docker configuration (if needed)
    "setup.py",  # Setup script for installing the package
    "README.md"  # Project readme file
]

for file in list_of_files:
    file_path = Path(file)
    file_dir, file_name = os.path.split(file_path)

    if file_dir != "":
        os.makedirs(file_dir, exist_ok=True)
        logging.info(f"Created directory: {file_dir} for the file: {file_name}")

    if(not os.path.exists(file_path)) or (os.path.getsize(file_path) == 0):
        with open(file_path, "w") as f:
            pass
        logging.info(f"Creating empty file at: %s" % file_path)

    else:
        logging.info(f"File already exists at: %s" % file_path)


