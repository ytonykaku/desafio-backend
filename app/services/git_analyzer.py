import os
import shutil
import git
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.repository import Repository
from app.models.author import Author
from app.models.analysis import Analysis

def get_or_create(db: Session, model, **kwargs):
    instance = db.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance

def analyze_repository(db: Session, user: str, repository_name: str) -> str:
    repo_url = f'https://github.com/{user}/{repository_name}.git'
    repo_dir = f'temp_repo_{user}_{repository_name}_{datetime.now().timestamp()}'

    try:
        repo_obj = get_or_create(db, Repository, url=repo_url, name=repository_name)
        
        repo_clone = git.Repo.clone_from(repo_url, repo_dir)

        commits_per_author = {}
        work_days_per_author = {}

        for commit in repo_clone.iter_commits():
            author_name = commit.author.name
            commit_date = commit.committed_datetime.date()

            commits_per_author[author_name] = commits_per_author.get(author_name, 0) + 1
            work_days_per_author.setdefault(author_name, set()).add(commit_date)

        response_lines = []
        for author_name, commits_count in commits_per_author.items():
            author_obj = get_or_create(db, Author, name=author_name)

            days_count = len(work_days_per_author.get(author_name, set()))
            avg_commits = commits_count / days_count if days_count > 0 else 0
            
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

    finally:
        if os.path.exists(repo_dir):
            shutil.rmtree(repo_dir)