import pytest
from unittest.mock import MagicMock
from dmesh.cli.setup.config_writer import ConfigWriter
from dmesh.cli.setup.feedback import Feedback

def test_config_writer_spec_extra_path(tmp_path, monkeypatch):
    # Mock PROJECT_CONFIG_PATH
    import dmesh.cli.setup.config_writer
    test_config_path = tmp_path / "base.toml"
    monkeypatch.setattr(dmesh.cli.setup.config_writer, "PROJECT_CONFIG_PATH", test_config_path)
    
    feedback = MagicMock(spec=Feedback)
    writer = ConfigWriter(feedback)
    
    # Write config with extra path
    writer.write_pg(
        host="localhost",
        port=5432,
        user="test_user",
        password="test_password",
        dbname="test_db",
        topology="filesystem",
        filesystem_persistency=True,
        data_products_filesystem_root="tmp/root",
        data_products_filesystem_extra_path="foo/bar"
    )
    
    # Verify content
    content = test_config_path.read_text()
    assert 'data_products_filesystem_root = "tmp/root"' in content
    assert 'data_products_filesystem_extra_path = "foo/bar"' in content
    
def test_config_writer_no_spec_extra_path(tmp_path, monkeypatch):
    # Mock PROJECT_CONFIG_PATH
    import dmesh.cli.setup.config_writer
    test_config_path = tmp_path / "base.toml"
    monkeypatch.setattr(dmesh.cli.setup.config_writer, "PROJECT_CONFIG_PATH", test_config_path)
    
    feedback = MagicMock(spec=Feedback)
    writer = ConfigWriter(feedback)
    
    # Write config without extra path
    writer.write_pg(
        host="localhost",
        port=5432,
        user="test_user",
        password="test_password",
        dbname="test_db",
        topology="filesystem",
        filesystem_persistency=True,
        data_products_filesystem_root="tmp/root",
        data_products_filesystem_extra_path=None
    )
    
    # Verify content
    content = test_config_path.read_text()
    assert 'data_products_filesystem_root = "tmp/root"' in content
    assert 'data_products_filesystem_extra_path' not in content
