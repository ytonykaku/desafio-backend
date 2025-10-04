import git
import pytest
from flask import Flask

import api


@pytest.fixture
def flask_app():
    app = Flask(__name__)
    return app


def test_git_analysis(flask_app):
    with flask_app.test_request_context(
        '/?usuario=gitpython-developers&repositorio=gitdb'
    ):
        result = api.git_analysis()
        assert 'Sebastian Thiel realizou 268 commits com uma média de 2.95 commits por dia.' in result

    with flask_app.test_request_context(
            '/?autor1=Sebastian'
    ):
        result = api.buscar_medias_de_commit()
        assert 'Sebastian Thiel possui uma média de 2.95 commits por dia.' in result


def test_git_analysis_no_repo(flask_app):
    with flask_app.test_request_context(
        '/?usuario=nonexistent-user&repositorio=nonexistent-repo'
    ):
        with pytest.raises(git.exc.GitCommandError):
            result = api.git_analysis()
