#!/usr/bin/env python3
"""Test suite for client module."""
import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value."""
        test_payload = {
            "repos_url": f"https://api.github.com/orgs/{org_name}/repos"
        }
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        result = client.org

        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, test_payload)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the expected value."""
        test_payload = {
            "repos_url": "https://api.github.com/orgs/google/repos"
        }

        with patch.object(GithubOrgClient, 'org',
                          new_callable=PropertyMock) as mock_org:
            mock_org.return_value = test_payload
            client = GithubOrgClient("google")
            result = client._public_repos_url

            self.assertEqual(result, test_payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns the expected list of repos."""
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = test_payload

        with patch.object(GithubOrgClient, '_public_repos_url',
                          new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/google/repos"
            client = GithubOrgClient("google")
            result = client.public_repos()

            expected_repos = ["repo1", "repo2", "repo3"]
            self.assertEqual(result, expected_repos)
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/google/repos"
            )

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license returns the expected value."""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD[0][0],
        "repos_payload": TEST_PAYLOAD[0][1],
        "expected_repos": TEST_PAYLOAD[0][2],
        "apache2_repos": TEST_PAYLOAD[0][3],
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test class for GithubOrgClient."""

    @classmethod
    def setUpClass(cls):
        """Set up class fixtures before running tests."""
        config = {
            'return_value.json.side_effect': [
                cls.org_payload,
                cls.repos_payload,
                cls.org_payload,
                cls.repos_payload,
            ]
        }
        cls.get_patcher = patch('requests.get', **config)
        cls.mock_get = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """Tear down class fixtures after running tests."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos method."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos method with license filter."""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )


if __name__ == '__main__':
    unittest.main()
