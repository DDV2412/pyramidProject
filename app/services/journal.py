from app.repository.journal import JournalRepository
from pyramid.request import Request


class JournalService:
    def __init__(self, request: Request):
        self.journal_repo = JournalRepository(request)

    def create_journal(self, journal_data):
        return self.journal_repo.create_journal(journal_data)

    def find_by_id(self, journal_id):
        return self.journal_repo.find_by_id(journal_id)

    def get_all_journals(self):
        return self.journal_repo.find_all_journals()

    def update_journal(self, journal_id, updates):
        self.journal_repo.update_journal(journal_id, updates)

    def delete_journal(self, journal_id):
        self.journal_repo.delete_journal(journal_id)


