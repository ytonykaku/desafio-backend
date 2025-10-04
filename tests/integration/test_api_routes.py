# tests/integration/test_api_routes.py

import pytest
from app import create_app
from app.services.git_analyzer import RepositoryNotFoundError

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_git_analysis_success(client, monkeypatch):
    monkeypatch.setattr(
        'app.services.git_analyzer.analyze_repository',
        lambda *args, **kwargs: 'Análise mockada com sucesso.'
    )
    response = client.get('/analisador-git?usuario=test&repositorio=test')
    assert response.status_code == 200
    assert b'An\xc3\xa1lise mockada com sucesso.' in response.data

def test_git_analysis_repo_not_found(client, monkeypatch):
    def mock_raise_error(*args, **kwargs):
        raise RepositoryNotFoundError("Repo não encontrado.")
    monkeypatch.setattr(
        'app.services.git_analyzer.analyze_repository',
        mock_raise_error
    )
    response = client.get('/analisador-git?usuario=bad&repositorio=repo')
    assert response.status_code == 400
    assert b'Repo n\xc3\xa3o encontrado.' in response.data

def test_search_commit_averages_success(client, monkeypatch):
    class MockAnalysis:
        average_commits = 2.5
    class MockAuthor:
        name = "Autor Teste"
    class MockRepository:
        name = "repo-teste"
    mock_query_result = [(MockAnalysis(), MockAuthor(), MockRepository())]
    
    monkeypatch.setattr('sqlalchemy.orm.Query.all', lambda self: mock_query_result)
    
    response = client.get('/analisador-git/buscar?autor1=Teste')
    assert response.status_code == 200
    expected_string = b'Autor Teste (no reposit\xc3\xb3rio repo-teste) possui uma m\xc3\xa9dia de 2.50 commits por dia.'
    assert expected_string in response.data

def test_search_commit_averages_no_results(client, monkeypatch):
    monkeypatch.setattr('sqlalchemy.orm.Query.all', lambda self: [])
    response = client.get('/analisador-git/buscar?autor1=ninguem')
    assert response.status_code == 200
    assert b'Nenhum resultado encontrado para os autores informados.' in response.data