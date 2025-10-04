import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
from app.services.git_analyzer import analyze_repository, RepositoryNotFoundError
from app.models.author import Author
from app.models.repository import Repository

class MockCommit:
    """Uma classe mock para simular um objeto de commit do GitPython."""
    def __init__(self, author_name, date_str):
        self.author = MagicMock()
        self.author.name = author_name
        self.committed_datetime = datetime.strptime(date_str, '%Y-%m-%d')

# Lista de commits mockados para ser usada nos testes
mock_commits_list = [
    MockCommit("Autor A", "2023-10-01"),
    MockCommit("Autor B", "2023-10-01"),
    MockCommit("Autor A", "2023-10-02"),
    MockCommit("Autor A", "2023-10-02"),
]

@patch('app.services.git_analyzer.shutil.rmtree')
@patch('app.services.git_analyzer.git.Repo.clone_from')
@patch('app.services.git_analyzer.repository_repository.create')
@patch('app.services.git_analyzer.repository_repository.get_by_url')
@patch('app.services.git_analyzer.author_repository.create')
@patch('app.services.git_analyzer.author_repository.get_by_name')
def test_analyze_repository_success(
    mock_author_get_by_name,
    mock_author_create,
    mock_repo_get_by_url,
    mock_repo_create,
    mock_clone_from,
    mock_rmtree
):
    """
    Testa o caso de sucesso do serviço de análise
    """
    mock_repo_instance = MagicMock()
    mock_repo_instance.iter_commits.return_value = mock_commits_list
    mock_clone_from.return_value = mock_repo_instance

    mock_repo_get_by_url.return_value = None
    mock_author_get_by_name.return_value = None

    mock_repo_create.return_value = Repository(id=1, name='repo', url='https://github.com/user/repo.git')
    mock_author_create.side_effect = [
        Author(id=101, name='Autor A'),
        Author(id=102, name='Autor B')
    ]

    mock_db_session = MagicMock()

    result = analyze_repository(mock_db_session, "user", "repo")

    assert "Autor A realizou 3 commits com uma média de 1.50 commits por dia." in result
    assert "Autor B realizou 1 commits com uma média de 1.00 commits por dia." in result

    assert mock_db_session.add.call_count == 2
    assert mock_db_session.commit.call_count == 1

@patch('app.services.git_analyzer.shutil.rmtree')
@patch('app.services.git_analyzer.git.Repo.clone_from')
def test_analyze_repository_git_error(mock_clone_from, mock_rmtree):
    """Testa o tratamento de erro quando o clone do repositório falha."""
    from git.exc import GitCommandError
    mock_clone_from.side_effect = GitCommandError("clone", "failed")
    
    mock_db_session = MagicMock()
    with pytest.raises(RepositoryNotFoundError):
        analyze_repository(mock_db_session, "user", "repo")