class ContactValidator:
    def __init__(self, attrs: dict[str, str]):
        self._attrs = attrs
        self._errors = []

    def call(self):
        self._name_validations()

    def is_success(self):
        return len(self._errors) == 0

    def show_errors(self):
        return self._errors

    def _name_validations(self):
        if self._attrs["name"].isspace():
            self._errors.append("имя не может быть пустым")
