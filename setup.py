import sys
from pathlib import Path

import semver
from setuptools import find_packages, setup
from setuptools.dist import Distribution as _Distribution

__name__ = "walldo"
vp = Path(__file__).parent / "src" / __name__ / "version.py"
__version__ = semver.VersionInfo.parse(vp.read_text().strip().split('"')[1])


def version():
    if len(sys.argv) > 1 and sys.argv[1] >= "bdist_wheel":
        nv = f"{__version__.bump_patch()}"
        vp.write_text(f'__version__ = "{nv}"\n')
        return nv
    return f"{__version__}"


class Distribution(_Distribution):
    def is_pure(self):
        return True


setup(
    name=__name__,
    version=version(),
    author="cacko",
    author_email="alex@cacko.net",
    distclass=Distribution,
    url=f"http://pypi.cacko.net/simple/{__name__}/",
    description="whatever",
    install_requires=[
        "appdirs>=1.4.4",
        "apscheduler>=3.10.1",
        "better-exceptions>=0.3.3",
        "certifi>=2023.5.7",
        "charset-normalizer>=3.1.0",
        "click>=8.1.3",
        "colorama>=0.4.6",
        "corelog>=0.0.8",
        "greenlet>=2.0.2",
        "idna>=3.4",
        "markdown-it-py>=3.0.0",
        "mdurl>=0.1.2",
        "pydantic>=1.10.9",
        "pygments>=2.15.1",
        "pytz>=2023.3",
        "requests>=2.31.0",
        "rich>=13.4.2",
        "semver>=3.0.1",
        "six>=1.16.0",
        "sqlalchemy>=2.0.17",
        "structlog>=23.1.0",
        "typing-extensions>=4.6.3",
        "tzlocal>=5.0.1",
        "urllib3>=2.0.3",
    ],
    setup_requires=["wheel"],
    python_requires=">=3.11",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points="""
        [console_scripts]
        walldo=walldo.cli:run
    """,
)
