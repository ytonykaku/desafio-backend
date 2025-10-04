import os
import shutil
import git
from datetime import datetime, date
from sqlalchemy.orm import Session
from app.repositories import author_repository, repository_repository
from app.models.analysis import Analysis

class RepositoryNotFoundError(Exception):
    """Exceção para quando o repositório não é encontrado."""
    pass

def analyze_repository(db: Session, user: str, repository_name: str) -> str:
    repo_url: str = f'https://github.com/{user}/{repository_name}.git'
    repo_dir: str = f'temp_repo_{user}_{repository_name}_{datetime.now().timestamp()}'

    try:
        repo_clone = git.Repo.clone_from(repo_url, repo_dir)

        repo_obj = repository_repository.get_by_url(db, url=repo_url)
        if not repo_obj:
            repo_obj = repository_repository.create(db, name=repository_name, url=repo_url)
        
        commits_per_author: dict[str, int] = {}
        work_days_per_author: dict[str, set[date]] = {}
        for commit in repo_clone.iter_commits():
            author_name = commit.author.name
            commit_date = commit.committed_datetime.date()
            commits_per_author[author_name] = commits_per_author.get(author_name, 0) + 1
            work_days_per_author.setdefault(author_name, set()).add(commit_date)

        response_lines: list[str] = []
        for author_name, commits_count in commits_per_author.items():
            author_obj = author_repository.get_by_name(db, name=author_name)
            if not author_obj:
                author_obj = author_repository.create(db, name=author_name)

            days_count: int = len(work_days_per_author.get(author_name, set()))
            avg_commits: float = commits_count / days_count if days_count > 0 else 0
            
            analysis_obj = Analysis(
                analyze_date=datetime.now(),
                average_commits=avg_commits,
                repository_id=repo_obj.id,
                author_id=author_obj.id
            )
            db.add(analysis_obj)
            response_lines.append(
                f'{author_name} realizou {commits_count} commits com uma média de {avg_commits:.2f} commits por dia.'
            )
        
        db.commit()
        return "<br>".join(response_lines)
    
    except git.exc.GitCommandError:
        raise RepositoryNotFoundError(f"Repositório não encontrado ou privado em '{repo_url}'.")
    finally:
        if os.path.exists(repo_dir):
            shutil.rmtree(repo_dir)