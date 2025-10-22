from flask import Flask, url_for, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Notes(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  note = db.Column(db.String(100), nullable=False)
  date_created = db.Column(db.DateTime,
                           default=datetime.datetime.now(datetime.UTC))

  def __init__(self, note):
    self.note = note

  def __repr__(self):
    return 'Id: %r' % self.id


# with app.app_context():
#   db.create_all()


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/add', methods=["GET", "POST"])
def add():
  note = request.form['note']
  new_note = Notes(note=note)

  try:
    db.session.add(new_note)
    db.session.commit()
    return redirect('/notes')
  except:
    return "Could not add note"


@app.route('/notes')
def view():
  notes = Notes.query.order_by(Notes.date_created).all()
  return render_template('notes.html', notes=notes)


if __name__ == "__main__":
  app.run(debug=True)
