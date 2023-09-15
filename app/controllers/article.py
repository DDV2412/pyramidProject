from pyramid.response import Response
from pyramid.view import view_config
from app.utils.exception_handler import handle_not_found, handle_bad_request
from app.services.article import ArticleService
from app.services.journal import JournalService


class ArticleController:
    def __init__(self, request):
        self.request = request
        self.article_service = ArticleService(request)
        self.journal_service = JournalService(request)

    @view_config(route_name="get_all_articles", renderer="json", request_method="GET")
    def get_all_articles(self):
        try:
            page = int(self.request.params.get("page", 1))
            per_page = int(self.request.params.get("per_page", 15))
            search = self.request.params.get("search", None)
            sort_field = self.request.params.get("sort_field", None)
            sort_order = self.request.params.get("sort_order", None)
            subject_filter = self.request.params.get("subject_filter", None)
            journal_filter = self.request.params.get("journal_filter", None)
            author_filter = self.request.params.get("author_filter", None)
            singleYear = self.request.params.get("singleYear", None)
            minYear = self.request.params.get("minYear", None)
            maxYear = self.request.params.get("maxYear", None)
            searchWithin = self.request.params.get("searchWithin", None)
            featured = self.request.params.get("featured", False)
            advancedQuery = self.request.params.get("advancedQuery", None)

            articles = self.article_service.get_all_articles(
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

            return Response(
                json_body={
                    "status": "success",
                    "data": articles,
                },
                status_code=200,
            )
        except Exception as e:
            return Response(
                json_body={
                    "status": "error",
                    "message": e.args,
                },
                status_code=500,
            )

    @view_config(route_name="create_article", renderer="json", request_method="POST")
    def create_article(self):
        try:
            journal_id = self.request.matchdict.get("journal_id")

            journal = self.journal_service.find_by_id(journal_id)

            handle_not_found(journal)

            article_data = self.request.json_body

            article_data["journal"] = journal

            article = self.article_service.create_article(article_data)
            return Response(
                json_body={"status": "success", "data": article}, status_code=200
            )
        except Exception as e:
            return Response(
                json_body={
                    "status": "error",
                    "message": "Application is busy restarting on the web server.",
                },
                status_code=500,
            )

    @view_config(route_name="article_find_by_id", renderer="json", request_method="GET")
    def find_by_id(self):
        try:
            article_id = self.request.matchdict.get("id")
            article = self.article_service.find_by_id(article_id)

            handle_not_found(article)

            return Response(
                json_body={"status": "success", "data": article}, status_code=200
            )
        except Exception as e:
            return Response(
                json_body={
                    "status": "error",
                    "message": "Application is busy restarting on the web server.",
                },
                status_code=500,
            )

    @view_config(
        route_name="article_find_by_doi", renderer="json", request_method="GET"
    )
    def find_by_doi(self):
        try:
            journal_id = self.request.matchdict.get("journal_id")

            journal = self.journal_service.find_by_id(journal_id)

            handle_not_found(journal)

            doi = self.request.matchdict.get("doi")
            article = self.article_service.find_by_doi(doi)

            handle_not_found(article)

            return Response(
                json_body={"status": "success", "data": article}, status_code=200
            )
        except Exception as e:
            return Response(
                json_body={
                    "status": "error",
                    "message": "Application is busy restarting on the web server.",
                },
                status_code=500,
            )

    @view_config(route_name="update_article", renderer="json", request_method="PATCH")
    def update_article(self):
        try:
            journal_id = self.request.matchdict.get("journal_id")

            journal = self.journal_service.find_by_id(journal_id)

            handle_not_found(journal)

            article_id = self.request.matchdict.get("id")
            article_data = self.request.json_body

            article_data["journal"] = journal

            article = self.article_service.find_by_id(article_id)
            handle_not_found(article)

            self.article_service.update_article(article_id, article_data)

            return Response(
                json_body={
                    "status": "success",
                    "message": "Article updated successfully",
                },
                status_code=200,
            )
        except Exception as e:
            return Response(
                json_body={
                    "status": "error",
                    "message": "Application is busy restarting on the web server.",
                },
                status_code=500,
            )

    @view_config(route_name="delete_article", renderer="json", request_method="DELETE")
    def delete_article(self):
        try:
            journal_id = self.request.matchdict.get("journal_id")

            journal = self.journal_service.find_by_id(journal_id)

            handle_not_found(journal)

            article_id = self.request.matchdict.get("id")
            article = self.article_service.find_by_id(article_id)

            handle_not_found(article)

            self.article_service.delete_article(article_id)

            return Response(
                json_body={
                    "status": "success",
                    "message": "Article deleted successfully",
                },
                status_code=200,
            )
        except Exception as e:
            return Response(
                json_body={
                    "status": "error",
                    "message": "Application is busy restarting on the web server.",
                },
                status_code=500,
            )
