from setuptools import setup, find_packages

setup(
    name="sc-telemetry",
    version="0.1.0",
    description="Star Citizen D-BOX telemetry hub",
    author="Romain Fleury",
    author_email="romain@example.com",
    url="https://github.com/RomainFleury/sc-telemetry-hub",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "sc-telemetry=sc_telemetry.cli:main",
        ],
    },
)
