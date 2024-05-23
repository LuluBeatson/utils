import toml  # or import tomli as toml for Python 3.11
import pathlib
import sys

# Load pyproject.toml file
pyproject_path = "pyproject.toml"
with open(pyproject_path) as f:
    pyproject_content = toml.load(f)

# Extract scripts
scripts = pyproject_content["tool"]["poetry"]["scripts"]

bash_functions = []

for name, reference in scripts.items():
    module, func = reference.split(":")
    bash_functions.append(
        f"""
function {name} {{
    $UTILS_PYTHON_PATH -m {module} "$@"
}}
"""
    )

bash_file_content = """
# This file contains bash function wrappers for Poetry-script commands in this project.
# Copy and paste the contents of this file into your .bashrc or .bash_profile to use

export UTILS_PYTHON_PATH={poetry_python}

{bash_functions}
""".format(
    poetry_python=sys.executable, bash_functions="\n".join(bash_functions)
)

# Write bash_functions to a bash file
bash_file_path = pathlib.Path("scripts.sh")
with open(bash_file_path, "w") as bash_file:
    bash_file.write(bash_file_content)

print(f"Bash functions created and saved to {bash_file_path}")
