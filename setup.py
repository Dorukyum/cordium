from setuptools import setup

classifiers = [
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
]

with open("README.md", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="cordium",
    packages=["cordium"],
    version="1.0.0",
    license="MIT",
    description="A simple, asynchronous wrapper for the Discord API",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Dorukyum",
    url="https://github.com/Dorukyum/cordium",
    keywords="Discord, API",
    install_requires=["aiohttp"],
    classifiers=classifiers,
    project_urls={"Source": "https://github.com/Dorukyum/cordium"},
)
