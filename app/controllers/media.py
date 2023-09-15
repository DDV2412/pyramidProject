import os
from pyramid.response import Response
from pyramid.view import view_config
from app.utils.exception_handler import handle_not_found, handle_bad_request


class MediaController:
    def __init__(self, request):
        self.request = request

    @view_config(route_name="upload_image", renderer="json", request_method="POST")
    def upload_image(self):
        try:
            image = self.request.POST.get("image")
            if image is not None:
                content_type = image.type.lower()
                if content_type not in ("image/jpeg", "image/png"):
                    return handle_bad_request(False, "Invalid image format")

                filename = image.filename.replace(" ", "-").lower()
                base_directory = os.path.dirname(
                    os.path.dirname(os.path.abspath(__file__))
                )
                storage_path = os.path.join(
                    base_directory, "storage", "images", filename
                )
                with open(storage_path, "wb") as f:
                    f.write(image.file.read())
                return Response(
                    json_body={
                        "status": "success",
                        "url": self.request.host_url + "/image/" + filename,
                    },
                    status_code=200,
                )
            else:
                return handle_bad_request(False, "No image data received")
        except Exception as e:
            return handle_bad_request(False, str(e))

    @view_config(route_name="upload_document", renderer="json", request_method="POST")
    def upload_document(self):
        try:
            document = self.request.POST["document"]
            if document is not None:
                content_type = document.type.lower()
                if content_type != "application/pdf":
                    return handle_bad_request(False, "Invalid document format")

                filename = document.filename.replace(" ", "-").lower()
                base_directory = os.path.dirname(
                    os.path.dirname(os.path.abspath(__file__))
                )
                storage_path = os.path.join(
                    base_directory, "storage", "documents", storage_path
                )
                with open(storage_path, "wb") as f:
                    f.write(document.file.read())
                return Response(
                    json_body={
                        "status": "success",
                        "url": self.request.host_url + "/document/" + filename,
                    },
                    status_code=200,
                )
            else:
                return handle_bad_request(False, "No document data received")
        except Exception as e:
            return handle_bad_request(False, str(e))

    @view_config(route_name="delete_image", renderer="json", request_method="DELETE")
    def delete_image(self):
        try:
            filename = self.request.matchdict["filename"]
            base_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            storage_path = os.path.join(base_directory, "storage", "images", filename)
            if os.path.exists(storage_path):
                os.remove(storage_path)
                return Response(
                    json_body={
                        "status": "success",
                        "message": "Image deleted successfully",
                    },
                    status_code=200,
                )
            else:
                return handle_not_found("Image not found")
        except Exception as e:
            return handle_bad_request(False, str(e))

    @view_config(route_name="delete_document", renderer="json", request_method="DELETE")
    def delete_document(self):
        try:
            filename = self.request.matchdict["filename"]
            base_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            storage_path = os.path.join(
                base_directory, "storage", "documents", filename
            )
            if os.path.exists(storage_path):
                os.remove(storage_path)
                return Response(
                    json_body={
                        "status": "success",
                        "message": "Document deleted successfully",
                    },
                    status_code=200,
                )
            else:
                return handle_not_found("Document not found")
        except Exception as e:
            return handle_bad_request(False, str(e))

    @view_config(route_name="view_image", request_method="GET")
    def view_image(self):
        try:
            filename = self.request.matchdict["filename"]
            base_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            storage_path = os.path.join(base_directory, "storage", "images", filename)
            if os.path.exists(storage_path):
                response = Response(content_type="image/jpeg")
                with open(storage_path, "rb") as f:
                    response.body = f.read()
                return response
            else:
                return handle_not_found("Image not found")
        except Exception as e:
            return handle_bad_request(False, str(e))

    @view_config(route_name="view_document", request_method="GET")
    def view_document(self):
        try:
            filename = self.request.matchdict["filename"]
            base_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            storage_path = os.path.join(
                base_directory, "storage", "documents", filename
            )
            if os.path.exists(storage_path):
                response = Response(content_type="application/pdf")
                with open(storage_path, "rb") as f:
                    response.body = f.read()
                return response
            else:
                return handle_not_found("Document not found")
        except Exception as e:
            return handle_bad_request(False, str(e))
