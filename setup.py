import setuptools

with open("README.md", "r") as fp:
    long_description = fp.read()

setuptools.setup(
    name="polito_dl",
    version="2.0.0-alpha",
    license="GPLv3",
    author="Giuseppe Lumia",
    author_email="glumia@protonmail.com",
    description=(
        "Command-line tool and library to download Polytechnic of Turin's online "
        "lessons from didattica.polito.it"
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/glumia/polito_dl",
    packages=["polito_dl"],
    keywords=["polito", "politecnico", "torino"],
    classifiers=[
        "Development Status :: 3 - Alpha",
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
