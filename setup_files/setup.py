from setuptools import setup, find_packages

setup(
    name="sankalpa",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.103.1",
        "uvicorn==0.23.2",
        "pydantic==2.3.0",
        "email-validator==2.0.0",
        "python-dotenv==1.0.0",
        "httpx==0.24.1",
    ],
    python_requires=">=3.10",
)