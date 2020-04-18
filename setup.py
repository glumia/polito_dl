import setuptools

with open("README.md", "r") as fp:
    long_description = fp.read()

setuptools.setup(
    name="polito_dl",
    version="2.0.0",
    author="Giuseppe Lumia",
    author_email="glumia@protonmail.com",
    description=(
        "A library and CLI tool to get direct download URLs of video lectures on "
        "PoliTo's portal"
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/glumia/polito_dl",
    packages=["polito_dl"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests", "bs4", "click"],
    entry_points="""
        [console_scripts]
        polito_dl=polito_dl.cli:main
    """,
)
