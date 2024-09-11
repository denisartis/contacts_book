from flask import render_template, request, redirect, url_for
from app import app, db

from validators import ContactValidator
from app import Contact
from services import GetContactService

GROUPS = ['Без группы', 'Работа', 'Друзья', 'Семья']


@app.route('/contacts', methods=["GET"])
def index():
    search_name = request.args.get('search_name')
    order = request.args.get('order')

    service = GetContactService({"name": search_name, "order": order})
    contacts = service.call()

    return render_template("index.html", contacts=contacts, groups=GROUPS)


@app.route('/to_find_contact_form', methods=["GET"])
def find_contact():
    return render_template("find.html")


@app.route('/to_new_contact_form', methods=["GET"])
def new_contact_form():
    return render_template("new_contact.html", groups=GROUPS)


@app.route('/contacts/create', methods=["POST"])
def create_contact():
    validator = ContactValidator(request.form.to_dict())
    validator.call()

    if validator.is_success():
        contact = Contact(
            name=request.form["name"],
            phone_number=request.form["phone_number"],
            email=request.form["email"],
            address=request.form["address"],
            group_name=request.form["group_name"]
        )
        db.session.add(contact)
        db.session.commit()

    return render_template(
        "new_contact.html",
        success=validator.is_success(),
        errors=validator.show_errors(),
        groups=GROUPS
    )


@app.route("/contacts/to_edit_contact_form/<int:contact_id>", methods=["GET"])
def edit_contact_form(contact_id):
    contact = Contact.query.get_or_404(contact_id)

    return render_template("edit_contact.html", contact=contact, groups=GROUPS)


@app.route("/contacts/update_contact/<int:contact_id>", methods=["POST"])
def update_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    validator = ContactValidator(request.form.to_dict())
    validator.call()

    if validator.is_success():
        contact.name = request.form["name"]
        contact.phone_number = request.form["phone_number"]
        contact.email = request.form["email"]
        contact.address = request.form["address"]
        contact.group_name = request.form["group_name"]
        db.session.commit()

    return render_template(
            "edit_contact.html",
            success=validator.is_success(),
            errors=validator.show_errors(),
            contact=contact,
            groups=GROUPS
    )


@app.route("/contacts/delete_contact/<int:contact_id>", methods=["GET"])
def delete_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)

    db.session.delete(contact)
    db.session.commit()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
