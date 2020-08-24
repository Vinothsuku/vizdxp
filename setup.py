import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vizdxp",
    version="0.0.4",
    author="vinoth sukumaran",
    author_email="vizdxp@gmail.com",
    description="Simple data visualization web app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Vinothsuku/vizdxp",
    packages=setuptools.find_packages(),
    data_files=[('', ['vizdxp/style.css'])],
    install_requires=['streamlit>=0.65.2', 'pandas>=1.1.0', 'numpy>=1.19.1', 'plotly>=4.9.0'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    python_requires='>=3.6',
    entry_points={"console_scripts": ["vizdxp=vizdxp.__main__:main"]},
)
