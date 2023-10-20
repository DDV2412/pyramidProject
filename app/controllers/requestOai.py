from pyramid.response import Response
from pyramid.view import view_config
from app.services.request_oai import RequestOAI
from app.services.journal import JournalService
from app.services.article import ArticleService
from app.utils.exception_handler import handle_not_found
import json


class requestOAI:
    def __init__(self, request):
        self.request = request
        self.oai_service = RequestOAI(request)
        self.journal_service = JournalService(request)
        self.article_service = ArticleService(request)

    @view_config(route_name="request_oai", renderer="json", request_method="POST")
    def request_oai(self):
        try:
            journal_id = self.request.matchdict.get("journal_id")

            journal = self.journal_service.find_by_id(journal_id)

            handle_not_found(journal)

            results = self.oai_service.request_oai(
                journal["site_url"], journal["abbreviation"]
            )

            for result in results["results"]:
                doi = result.get("doi")
                if doi is None or not doi.strip():
                    continue

                # Set journal info into each result
                result["journal"] = journal

                # Create or update the article
                self.article_service.create_or_update_article(result)

            return Response(
                json_body={"status": "success", "data": "Request OAI successfully"},
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
