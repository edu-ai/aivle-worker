import setuptools
from setuptools import setup

setup(
    name="aivle_worker",
    version="0.2.2",
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
)
