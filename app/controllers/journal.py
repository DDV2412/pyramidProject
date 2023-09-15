from pyramid.response import Response
from pyramid.view import view_config
from app.utils.exception_handler import handle_not_found, handle_bad_request
from app.services.journal import JournalService


class JournalController:
    def __init__(self, request):
        self.request = request
        self.journal_service = JournalService(request)

    @view_config(route_name="get_all_journals", renderer="json", request_method="GET")
    def get_all_journals(self):
        try:
            journals = self.journal_service.get_all_journals()
            return Response(
                json_body={"status": "success", "data": journals}, status_code=200
            )
        except Exception as e:
            return Response(
                json_body={
                    "status": "error",
                    "message": "Application is busy restarting on the web server.",
                },
                status_code=500,
            )

    @view_config(route_name="create_journal", renderer="json", request_method="POST")
    def create_journal(self):
        try:
            journal_data = self.request.json_body

            journal = self.journal_service.create_journal(journal_data)
            return Response(
                json_body={"status": "success", "data": journal}, status_code=200
            )
        except Exception as e:
            return Response(
                json_body={
                    "status": "error",
                    "message": "Application is busy restarting on the web server.",
                },
                status_code=500,
            )

    @view_config(route_name="journal_find_by_id", renderer="json", request_method="GET")
    def find_by_id(self):
        try:
            journal_id = self.request.matchdict.get("id")
            journal = self.journal_service.find_by_id(journal_id)

            handle_not_found(journal)

            return Response(
                json_body={"status": "success", "data": journal}, status_code=200
            )
        except Exception as e:
            return Response(
                json_body={
                    "status": "error",
                    "message": "Application is busy restarting on the web server.",
                },
                status_code=500,
            )

    @view_config(route_name="update_journal", renderer="json", request_method="PATCH")
    def update_journal(self):
        try:
            journal_id = self.request.matchdict.get("id")
            journal_data = self.request.json_body

            journal = self.journal_service.find_by_id(journal_id)
            handle_not_found(journal)

            self.journal_service.update_journal(journal_id, journal_data)

            return Response(
                json_body={
                    "status": "success",
                    "message": "Journal updated successfully",
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

    @view_config(route_name="delete_journal", renderer="json", request_method="DELETE")
    def delete_journal(self):
        try:
            journal_id = self.request.matchdict.get("id")
            journal = self.journal_service.find_by_id(journal_id)

            handle_not_found(journal)

            self.journal_service.delete_journal(journal_id)

            return Response(
                json_body={
                    "status": "success",
                    "message": "Journal deleted successfully",
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
