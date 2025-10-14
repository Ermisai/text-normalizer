from setuptools import setup, find_packages

setup(
    name="text_normalizer",
    version="0.1.0",
    author="Lucas Gris",
    author_email="lucas.gris@egresso.ufg.br",
    description="Biblioteca de normalização de texto em português (datas, números, moedas, horários, CPFs etc.)",
    long_description=open("README.md", encoding="utf-8").read(),
    url="https://github.com/Ermisai/text-normalizer",  # opcional, se tiver repositório
    packages=find_packages(),
    install_requires=[
        "num2words>=0.5.12"
    ],
    python_requires=">=3.8",
)
