from setuptools import setup, find_packages

setup(
    name="codeattack",
    version="0.1.0",
    packages=find_packages(where="."),
    package_dir={"": "."},
    install_requires=[
        "openai",
        "numpy",
        "tqdm",
    ],
    python_requires=">=3.6",
) 