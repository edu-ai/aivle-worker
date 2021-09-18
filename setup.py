from setuptools import setup

setup(
    name="aivle_worker",
    version="0.1",
    description="Grader client for aiVLE submissions.",
    url="https://github.com/edu-ai/aivle-worker",
    author="Yuanhong Tan",
    author_email="tan.yuanhong@u.nus.edu",
    packages=["aivle-worker"],
    install_requires=["requests", "websockets", "celery"],
    # setup_requires=['wheel'],
    zip_safe=False,
)
