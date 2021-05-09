from flask import Flask, render_template, url_for, request, send_from_directory, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/postgres'
#app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class State(db.Model):
	__tablename__ = 'State'
	city_name = db.Column(db.String(255), unique=True, nullable=False, primary_key=True)
	author = db.Column(db.String(255), nullable=False)
	state = db.relationship('Weather', cascade = 'all, save-update, delete, delete-orphan')

	def __init__(self, city_name, author):
		self.city_name = city_name
		self.author = author


class Weather(db.Model):
	record_id = db.Column(db.Integer, primary_key=True)
	City_name = db.Column(db.String(255), db.ForeignKey('State.city_name'))
	date = db.Column(db.String(255),nullable=False)
	temp = db.Column(db.Float, nullable=False)
	Raindrop = db.Column(db.Float, nullable=False)

	def __init__(self, record_id, City_name, date, temp, Raindrop):
		self.record_id = record_id
		self.City_name = City_name
		self.date = date
		self.temp = temp
		self.Raindrop = Raindrop

db.create_all()


db.session.commit()



@app.route('/')
def Index():
    data = Weather.query.all()
    data_state = State.query.all()
 
    return render_template("index.html", report = data, state=data_state)

@app.route('/insert', methods = ['POST'])
def insert():
	if request.method == 'POST':
		record_id = request.form['record_id']
		City_name = request.form['City_name']
		date = request.form['date']
		temp = request.form['temp']
		Raindrop = request.form['Raindrop']
		result = Weather(record_id, City_name, date, temp, Raindrop)
		db.session.add(result)
		db.session.commit()
	return redirect(url_for('Index'))
 

@app.route('/update', methods = ['GET', 'POST'])
def update():
	if request.method == 'POST':
		data = Weather.query.get(request.form.get('id'))
		data.record_id = request.form['record_id']
		data.City_name = request.form['City_name']
		data.date = request.form['date']
		data.temp = request.form['temp']
		data.Raindrop = request.form['Raindrop']
		db.session.commit()
	return redirect(url_for('Index'))
 

 
 

@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
	data = Weather.query.get(id)
	db.session.delete(data)
	db.session.commit()
	return redirect(url_for('Index'))



if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 8000)