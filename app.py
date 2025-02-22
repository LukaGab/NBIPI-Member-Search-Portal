from flask import Flask, redirect, render_template, flash, request
from flask_sqlalchemy import SQLAlchemy
import logging
import os
from models import Member, db
import csv


logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///members.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQL_ENGINE_OPTIONS"] = {
    "pool_recycle":300, 
    "pool_pre_ping":True
    }

db.init_app(app)

def import_member(file_path="members.csv"):
    with app.app_context():

        # ✅ Check if file exists before proceeding
        if not os.path.exists(file_path):
            print(f"Error: {file_path} not found!")
            return  # Exit early

        with open(file_path, newline='', encoding='utf-8') as file:
            data = list(csv.DictReader(file))  # Convert to list to check content
            
            if not data:
                print("Error: CSV file is empty!")
                return  # Exit early if empty
            
            member_list = []
            for row in data:
                email = row["email"].strip() if row["email"].strip() else None
                member_number = row["member_number"].strip()

                if Member.query.filter_by(member_number=member_number).first():
                    print(f"Skipping duplicate member_number: {member_number}")
                    continue

                if email and Member.query.filter_by(email=email).first():
                    print(f"Skipping duplicate email: {email}")
                    continue

                # ✅ Create a new Member instance
                new_member = Member(
                    member_number=row["member_number"],
                    last_name=row["last_name"],
                    first_name=row["first_name"],
                    email=email
                )
                member_list.append(new_member)

            # ✅ Add all valid members at once
            if member_list:
                db.session.add_all(member_list)
                db.session.commit()
                print(f"✅ Successfully added {len(member_list)} members.")
            else:
                print("No valid members to add.")


@app.route('/', methods=['POST', 'GET'])
def index():
    results = []

    if request.method == 'POST':
        last_name = request.form.get("last_name", "").strip()
        member_number = request.form.get("member_number", "").strip()

        print(f"Search parameters - Last name: {last_name}, Member number: {member_number}")

        if not last_name and not member_number:
            flash('Please enter either a last name or a member registration number.', 'error')
            return render_template("index.html", results=results)
        
        if not last_name:
            flash('Both last name and member registration number are required.', 'error')
            return render_template("index.html", results=results)
        
        if not member_number:
            flash('Both last name and member registration number are required.', 'error')
            return render_template("index.html", results=results)
        
        if member_number:
            member = Member.query.filter_by(
                member_number=member_number,
                last_name=last_name
                ).first()
            
            print(f"Member number search result: {member}") 
            
            if member:
                results.append(member.to_dict())
            else:
                flash('No member found with the provided last name and member registration number', 'error')

        print(f"Final results: {results}")

    return render_template('index.html', results=results)


if __name__ == '__main__':
    import_member()
    app.run(debug=True)