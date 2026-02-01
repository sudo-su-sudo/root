from setuptools import setup, find_packages

setup(
    name="ai-swarm-orchestrator",
    version="0.1.0",
    description="Autonomous AI Swarm Orchestrator for high-level requests",
    packages=find_packages(),
    install_requires=[
        "pydantic>=2.0.0",
    ],
    extras_require={
        "test": ["pytest>=7.0.0"],
    },
    python_requires=">=3.8",
)
