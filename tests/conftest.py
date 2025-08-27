"""Common test fixtures and configuration."""

import pytest
from pathlib import Path
from typer.testing import CliRunner

@pytest.fixture(scope="module")
def runner():
    """Return a CLI runner."""
    return CliRunner()


@pytest.fixture
def sample_job_yaml():
    """Return sample job YAML content."""
    return """
job_id: 123456
new_settings:
  name: test-job-prod
  tags:
    team: data-science
  access_control_list:
    - group_name: Group - DS ML Engineering
      permission_level: CAN_MANAGE
  tasks:
    - task_key: main
      spark_python_task:
        python_file: dbfs:/path/to/script.py
"""


@pytest.fixture
def sample_databricks_config():
    """Return sample databricks config content."""
    return """
[DEFAULT]
host = https://example.databricks.com
token = dapi123456789
"""


@pytest.fixture
def temp_job_file(tmp_path, sample_job_yaml):
    """Create a temporary job YAML file."""
    jobs_dir = tmp_path / "jobs"
    jobs_dir.mkdir()
    job_file = jobs_dir / "test-job.yaml"
    job_file.write_text(sample_job_yaml)
    return job_file


@pytest.fixture
def temp_config_file(tmp_path, sample_databricks_config):
    """Create a temporary databricks config file."""
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    config_file = config_dir / "databrickscfg"
    config_file.write_text(sample_databricks_config)
    return config_file