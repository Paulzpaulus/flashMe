class DuplicateEntryError(Exception):
    def __init__(self, detail: str = "Resource already exists"):
        self.detail = detail


class ResourceNotFoundError(Exception):
    def __init__(self, detail: str = "Resource not found"):
        self.detail = detail
