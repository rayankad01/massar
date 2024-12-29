import os
import subprocess
import sys
import time
from cryptography.fernet import Fernet
import secrets


def print_project_info():
    """Displays information about the project."""
    print("\n🛠️  Project Information:")
    print(" ____________________________________________")
    print("|Name: Massar                                |")
    print("|Link: https://github.com/rayankad01/massar/ |")
    print("|Creator: rayankad01                         |")
    print("|Version: MVP                                |")
    print("|____________________________________________|")
    print("\n")



def check_python_version():
    """Checks that the Python version is compatible."""
    if sys.version_info < (3, 7):
        sys.exit("Python 3.7 or higher is required. Please update your installation.")


def create_virtualenv():
    """Creates a virtual environment if necessary."""
    print("Creating virtual environment...")
    if not os.path.exists('.env'):
        subprocess.run([sys.executable, '-m', 'venv', '.env'], check=True)
        print("Virtual environment created.")
    else:
        print("Virtual environment already exists.")


def install_python_dependencies():
    """Installs Python dependencies."""
    print("Installing Python dependencies...")
    subprocess.run(['.env/bin/pip', 'install', '--upgrade', 'pip'], check=True)
    subprocess.run(['.env/bin/pip', 'install', '-r', 'requirements.txt'], check=True)
    print("Python dependencies installed.")


def setup_env_file():
    """Creates a .env file with default values if necessary."""
    if not os.path.exists('.venv'):
        print("Creating .env file...")
        secret_key = Fernet.generate_key().decode()
        django_secret_key = secrets.token_urlsafe(50)
        with open('.venv', 'w') as f:
            f.write(f'''DEBUG=True\nENCRYPTION_KEY="{secret_key}"\nDJANGO_SECRET_KEY="django-insecure-{django_secret_key}"''')
        print(".env file created successfully.")
    else:
        print("The .env file already exists.")


def install_tailwind():
    """Installs Tailwind CSS via npm if necessary."""
    print("Installing Tailwind CSS...")
    if not os.path.exists('node_modules'):
        subprocess.run(['npm', 'install', 'tailwindcss'], check=True)
        print("Tailwind CSS installed.")
    else:
        print("Tailwind CSS is already installed.")


def run_tailwind_build():
    """Compiles CSS files with Tailwind."""
    print("Compiling CSS files with Tailwind...")
    subprocess.run(['npx', 'tailwindcss', 'init'], check=True)
    print("Tailwind compilation completed.")


def apply_django_migrations():
    """Applies Django migrations."""
    print("Applying Django migrations...")
    subprocess.run(['.env/bin/python', 'manage.py', 'migrate'], check=True)
    print("Django migrations applied.")


def main():
    """Executes all setup steps."""
    print_project_info()
    time.sleep(5)
    check_python_version()
    create_virtualenv()
    install_python_dependencies()
    setup_env_file()
    install_tailwind()
    run_tailwind_build()
    apply_django_migrations()
    print("\n✅ Setup completed successfully!")



if __name__ == "__main__":
    main()
