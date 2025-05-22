from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ocm-mcp-server",
    version="0.1.0",
    author="Deepak Chourasia",
    author_email="deepak.chourasia@example.com",
    description="Server implementation for OCM and MCP integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dchourasia/OCM-MCP-Server",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
