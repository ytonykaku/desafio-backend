from flask import request, Blueprint
from app.database.database import SessionLocal
from app.services.git_analyzer import analyze_repository, RepositoryNotFoundError
from app.services import git_analyzer
from app.models.analysis import Analysis
from app.models.author import Author
from app.models.repository import Repository

git_analysis_bp = Blueprint('git_analysis', __name__)

@git_analysis_bp.route('/analisador-git', methods=['GET'])
def git_analysis_endpoint():
    user = request.args.get('usuario')
    repo_name = request.args.get('repositorio')

    if not user or not repo_name:
        return "Os parâmetros 'usuario' e 'repositorio' são obrigatórios.", 400

    db = SessionLocal()
    try:
        response_text = git_analyzer.analyze_repository(db, user, repo_name)
        return response_text
    except RepositoryNotFoundError as e:
        return str(e), 400
    finally:
        db.close()

@git_analysis_bp.route('/analisador-git/buscar', methods=['GET'])
def search_commit_averages_endpoint():
    authors_query = [arg for arg in request.args.values() if arg]
    
    if not authors_query:
        return "É necessário informar pelo menos um autor.", 400

    db = SessionLocal()
    try:
        unique_results = set()
        for author_name in authors_query:
            records = (
                db.query(Analysis, Author, Repository)
                .join(Author, Analysis.author_id == Author.id)
                .join(Repository, Analysis.repository_id == Repository.id)
                .filter(Author.name.ilike(f"%{author_name}%"))
                .all()
            )
            
            for analysis, author, repository in records:
                unique_results.add(
                    f'{author.name} (no repositório {repository.name}) possui uma média de {analysis.average_commits:.2f} commits por dia.'
                )
        
        if not unique_results:
            return "Nenhum resultado encontrado para os autores informados.", 200

        return "<br>".join(sorted(list(unique_results)))
    finally:
        db.close()