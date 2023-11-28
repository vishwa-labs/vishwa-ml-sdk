import os
import setuptools

ROOT_DIR = os.path.dirname(__file__)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open(os.path.join(ROOT_DIR, "requirements.txt"), encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line]

setuptools.setup(
    name="xpulsai-python-sdk",
    version="0.0.1",
    author="xpuls.ai",
    description="Python SDK for Xpuls.ai",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xpuls-labs/xpuls-mlmonitor-python/tree/main/xpuls/sdk",
    packages=setuptools.find_packages(where="src"),
    namespace_packages=["xpuls"],
    package_dir={"": "src"},
    install_requires=requirements,
    python_requires=">=3.9, <4",
)
