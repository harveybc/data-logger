from setuptools import find_packages, setup

setup(
    name="data-logger",
    version="0.2.0",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "data-logger=app.main:main",
        ],
        "pipeline.plugins": [
            "default=pipeline_plugins.default:PipelinePlugin",
        ],
        "web.plugins": [
            "adminlte=web_plugins.adminlte:Plugin",
        ],
    },
    install_requires=["flask>=2.0"],
    description="Puente de telemetría a ThingsBoard CE con plugins de pipeline y web.",
    license="MIT",
)
