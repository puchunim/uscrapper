import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    requirements = fh.read().splitlines()

setuptools.setup(
    name="uscrapper",
    version="0.3.3c",
    author="Pedro Spezziale",
    author_email="pedro_s_m_rodrigues@hotmail.com",
    description="Simple scrapper for UnionMangas.top's mangas and webtoons",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/puchunim/uscrapper",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)