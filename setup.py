from pathlib import Path

import setuptools
from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="aivle_worker",
    version="0.2.3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="Grader client for aiVLE submissions.",
    url="https://github.com/edu-ai/aivle-worker",
    author="Yuanhong Tan",
    author_email="tan.yuanhong@u.nus.edu",
    package_dir={"": "src"},
    include_package_data=True,
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=["requests", "celery", "python-dotenv", "py3nvml", "psutil", "pyzmq"],
    setup_requires=['wheel'],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'aivle-worker = aivle_worker.command_line:main'
        ]
    }
)
