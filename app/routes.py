def includeme(config):
    # Journal
    config.add_route("get_all_journals", "/journals", request_method="GET")
    config.add_route("create_journal", "/journal", request_method="POST")
    config.add_route("journal_find_by_id", "/journal/{id}", request_method="GET")
    config.add_route("update_journal", "/journal/{id}", request_method="PATCH")
    config.add_route("delete_journal", "/journal/{id}", request_method="DELETE")

    # Media
    config.add_route("upload_image", "/image", request_method="POST")
    config.add_route("upload_document", "/document", request_method="POST")
    config.add_route("delete_image", "/image/{filename}", request_method="DELETE")
    config.add_route("delete_document", "/document/{filename}", request_method="DELETE")
    config.add_route("view_image", "/image/{filename}", request_method="GET")
    config.add_route("view_document", "/document/{filename}", request_method="GET")

    # Article
    config.add_route("get_all_articles", "/articles", request_method="GET")
    config.add_route("create_article", "/{journal_id}/article", request_method="POST")
    config.add_route("article_find_by_id", "/article/{id}", request_method="GET")
    config.add_route(
        "article_find_by_doi", "/{journal_id}/article/doi/{doi}", request_method="GET"
    )
    config.add_route(
        "update_article", "/{journal_id}/article/{id}", request_method="PATCH"
    )
    config.add_route(
        "delete_article", "/{journal_id}/article/{id}", request_method="DELETE"
    )

    # Request OAI
    config.add_route("request_oai", "/request-oai/{journal_id}", request_method="POST")

    config.scan("app.controllers")
