from pathlib import Path

from setuptools import find_packages, setup


def parse_requirements_file(path):
    return [line.rstrip() for line in open(path, "r")]


reqs_main = parse_requirements_file("requirements.txt")

with open("README.md", "r") as f:
    long_description = f.read()

init_str = Path("math2notion/__init__.py").read_text()
version = init_str.split("__version__ = ")[1].rstrip().strip('"')

setup(
    name="math2notion",
    version=version,
    author="Honglong Tian",
    description="An extremely simple converter from LaTeX or Markdown to Notion "
                "that resolves issues with mathematical formulas.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FrankTianTT/math2notion",
    packages=["math2notion"],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Office/Business :: News/Diary',
        'Topic :: System :: Filesystems',
        'Topic :: Text Processing :: Markup :: Markdown',
        'Topic :: Utilities'
    ],
    install_requires=reqs_main,
    include_package_data=True,
    python_requires=">=3.6",
    zip_safe=False,
)
