from setuptools import setup, find_packages

setup(
    name="CSGOInvCacheConverter",
    version="0.1",
    packages=find_packages(),
    install_requires=["Pillow>=3.0.0"],

    author="Warren Nelson",
    author_email="nelsonw2014@gmail.com",
    description="Conversion Utility for Inventory Cache Files into a readable format",
    license="MIT",
    keywords="cs csgo cs:go inventory cache image manipulation conversion convert"
)

