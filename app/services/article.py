from app.repository.article import ArticleRepository
from pyramid.request import Request


class ArticleService:
    def __init__(self, request: Request):
        self.article_repo = ArticleRepository(request)

    def create_article(self, article_data):
        return self.article_repo.create_article(article_data)

    def find_by_id(self, article_id):
        return self.article_repo.find_by_id(article_id)

    def find_by_doi(self, doi):
        return self.article_repo.find_by_doi(doi)

    def get_all_articles(
        self,
        page,
        per_page,
        search,
        sort_field,
        sort_order,
        subject_filter,
        journal_filter,
        author_filter,
        singleYear,
        minYear,
        maxYear,
        searchWithin,
        featured,
        advancedQuery,
    ):
        return self.article_repo.find_all_articles(
            page,
            per_page,
            search,
            sort_field,
            sort_order,
            subject_filter,
            journal_filter,
            author_filter,
            singleYear,
            minYear,
            maxYear,
            searchWithin,
            featured,
            advancedQuery,
        )

    def update_article(self, article_id, updates):
        self.article_repo.update_article(article_id, updates)

    def delete_article(self, article_id):
        self.article_repo.delete_article(article_id)

    def create_or_update_article(self, article):
        doi = article.get("doi")
        last_update = article.get("last_update")
        existing_article = self.article_repo.find_by_doi(doi)

        if existing_article:
            if existing_article["last_update"] == last_update:
                return last_update
            else:
                self.article_repo.update_article(existing_article["articleId"], article)
        else:
            if doi:
                self.article_repo.create_article(article)
            else:
                return
