class ContactValidator:
    def __init__(self, attrs: dict[str, str]):
        self._attrs = attrs
        self._errors = []

    def call(self):
        self._name_validations()

    def is_success(self):
        return not self._errors

    def show_errors(self):
        return self._errors

    def _name_validations(self):
        if self._attrs["name"].isspace():
            self._errors.append("имя не может быть пустым")
