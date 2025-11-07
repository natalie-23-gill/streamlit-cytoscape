import setuptools
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="streamlit-cytoscape",
    version="0.1.0",
    author="st-cytoscape",
    author_email="",
    description="A flexible Streamlit component for interactive graph visualization using Cytoscape.js with enhanced customization options",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/natalie-23-gill/st-cytoscape",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "streamlit>=1.0.0",
    ],
)
