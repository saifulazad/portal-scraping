import json
from unittest.mock import MagicMock, patch

import boto3
import pytest

from extractor.settings import BUCKET_NAME
from extractor.s3.utils import upload_jobs_details


@pytest.fixture
def mock_s3():
    return MagicMock(spec=boto3.resource("s3"))


@patch("extractor.s3.utils.boto3.resource")
def test_upload_jobs_details(mock_s3_resource):
    # Arrange
    key = "test.json"
    content = {"data": [312, 13, 212]}
    data = json.dumps(content).encode("utf-8")
    s3_response = MagicMock()
    s3_response.status_code = 200
    mock_s3 = mock_s3_resource.return_value
    mock_s3.Object.return_value.put.return_value = s3_response

    # Act
    upload_jobs_details(key, content)

    # Assert
    mock_s3_resource.assert_called_once_with("s3")
    mock_s3.Object.assert_called_once_with(BUCKET_NAME, f"jobs-details/{key}")
    mock_s3.Object.return_value.put.assert_called_once_with(Body=data)


@patch("extractor.s3.utils.boto3.resource")
def test_upload_jobs_details_error(mock_s3_resource):
    # Arrange
    key = "test.json"
    content = {"data": [312, 13, 212]}
    mock_s3 = mock_s3_resource.return_value
    mock_s3.Object.return_value.put.side_effect = Exception("test error")

    # Assert
    with pytest.raises(IOError):
        # Act
        upload_jobs_details(key, content)

    mock_s3_resource.assert_called_once_with("s3")
    mock_s3.Object.assert_called_once_with(BUCKET_NAME, f"jobs-details/{key}")
    mock_s3.Object.return_value.put.assert_called_once()
