from setuptools import setup, find_packages
setup(
    name="kinect-theia",
    description="RapidCloud - Cloud Automation & Acceleration Framework",
    author="Igor Royzis",
    license="MIT",
    packages=["commands","modules"],
    include_package_data=True,
    install_requires=[
        'boto3>=1.11.13'
        'botocore>=1.14.13'
        'psycopg2>=2.8.4'
        'PyAthena>=1.10.1'
        'snowflake-connector-python>=2.2.4'
        'snowflake-sqlalchemy>=1.2.3'
        'SQLAlchemy>=1.3.15'
        'copy_tree'
    ],
    entry_points={"console_scripts": ["kc=kc.__main__:main"]},
)