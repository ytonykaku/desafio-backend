import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
from app.services.git_analyzer import analyze_repository, RepositoryNotFoundError

class MockCommit:
    def __init__(self, author_name, date_str):
        self.author = MagicMock()
        self.author.name = author_name
        self.committed_datetime = datetime.strptime(date_str, '%Y-%m-%d')

mock_commits_list = [
    MockCommit("Autor A", "2023-10-01"),
    MockCommit("Autor B", "2023-10-01"),
    MockCommit("Autor A", "2023-10-02"),
    MockCommit("Autor A", "2023-10-02"),
]

@patch('app.services.git_analyzer.git.Repo.clone_from')
@patch('app.services.git_analyzer.get_or_create')
def test_analyze_repository_success(_, mock_clone_from):
    mock_repo = MagicMock()
    mock_repo.iter_commits.return_value = mock_commits_list
    mock_clone_from.return_value = mock_repo
    
    mock_db_session = MagicMock()
    result = analyze_repository(mock_db_session, "user", "repo")

    assert "Autor A realizou 3 commits com uma média de 1.50 commits por dia." in result
    assert "Autor B realizou 1 commits com uma média de 1.00 commits por dia." in result
    
    assert mock_db_session.add.call_count == 2
    assert mock_db_session.commit.call_count == 1

@patch('app.services.git_analyzer.git.Repo.clone_from')
def test_analyze_repository_git_error(mock_clone_from):
    from git.exc import GitCommandError
    mock_clone_from.side_effect = GitCommandError("clone", "failed")
    
    mock_db_session = MagicMock()
    with pytest.raises(RepositoryNotFoundError):
        analyze_repository(mock_db_session, "user", "repo")