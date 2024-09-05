from flask import render_template, request, redirect, url_for

from models import Contact
from app import app, db
from validators import ContactValidator


@app.route('/', methods=["GET"])
def index():
    contacts = Contact.query.all()

    return render_template("index.html", contacts=contacts)


@app.route('/to_new_contact_form')
def new_contact_form():
    return render_template("new_contact.html")


@app.route('/create', methods=["POST"])
def create_contact():
    if request.method == "POST":
        validator = ContactValidator(request.form.to_dict())
        validator.call()
        if validator.is_success():
            contact = Contact(
                name=request.form["name"],
                phone_number=request.form["phone_number"],
                email=request.form["email"],
                address=request.form["address"]
            )
            db.session.add(contact)
            db.session.commit()
        return render_template(
            "new_contact.html",
            success=validator.is_success(),
            errors=validator.show_errors()
        )


@app.route("/to_edit_contact_form/<int:contact_id>")
def edit_contact_form(contact_id):
    contact = Contact.query.get_or_404(contact_id)

    return render_template("edit_contact.html", contact=contact)


@app.route("/delete_contact/<int:contact_id>")
def delete_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)

    db.session.delete(contact)
    db.session.commit()

    return redirect(url_for('index'))


@app.route("/update_contact/<int:contact_id>", methods=["POST"])
def update_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    validator = ContactValidator(request.form.to_dict())
    validator.call()

    if validator.is_success():
        contact.name = request.form["name"]
        contact.phone_number = request.form["phone_number"]
        contact.email = request.form["email"]
        contact.address = request.form["address"]
        db.session.commit()

    return render_template(
            "edit_contact.html",
            success=validator.is_success(),
            errors=validator.show_errors(),
            contact=contact
        )
