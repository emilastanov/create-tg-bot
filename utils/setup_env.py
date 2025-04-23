import os
import subprocess
import sys
import click


def setup_env(project_path, debug):
    pip_path = os.path.join(project_path, ".venv", "bin", "pip")
    if sys.platform == "win32":
        pip_path = os.path.join(project_path, ".venv", "Scripts", "pip.exe")

    try:
        subprocess.run([pip_path, "install", "-r", os.path.join(project_path, "requirements.txt")], check=True)
        if debug:
            click.echo("DEBUG > Dependencies installed successfully.")
    except Exception as e:
        click.echo(f"ERROR: Failed to install dependencies: {e}")

    try:
        subprocess.run(["alembic", "revision", "--autogenerate", "-m", "init"], cwd=project_path, check=True)
        subprocess.run(["alembic", "upgrade", "head"], cwd=project_path, check=True)
        if debug:
            click.echo("DEBUG > Successfully migrated.")
    except Exception as e:
        click.echo(f"ERROR: Migration failed: {e}")
