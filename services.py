from app import Contact
from sqlalchemy import asc, desc


class GetContactService:
    FILTERS = {
        "name": Contact.name.like,
        "email": Contact.email.like
    }

    def __init__(self, args: dict[str, str]):
        self.args = args
        self.result = Contact.query
        self.order = self.args.get('order', 'asc')
        self.sort_by = getattr(Contact, self.args.get('sort_by', 'name'))

    def call(self):
        for param, value in self.args.items():
            if param in self.FILTERS:
                self.result = self.result.filter(self.FILTERS[param](f"%{value}%"))
        self._sort()
        return self._group_by_groups(self.result.all())

    def _sort(self):
        if self.order == "asc":
            self.result = self.result.order_by(asc(self.sort_by))
        else:
            self.result = self.result.order_by(desc(self.sort_by))

    def _group_by_groups(self, contacts: list[Contact]):
        result = {}
        for contact in contacts:
            if contact.group_name not in result:
                result[contact.group_name] = [contact]
            else:
                result[contact.group_name].append(contact)
        return result
