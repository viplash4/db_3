from flask import Flask, render_template, url_for, request, send_from_directory, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://azsntminbzksta:d20a3fede137cde5449e700566c1cd739eabc664a72f8123b2d82abcfd0531cc@ec2-79-125-30-28.eu-west-1.compute.amazonaws.com:5432/d1fn7qjk172ekh'
#app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)




class Weather(db.Model):
	record_id = db.Column(db.Integer, primary_key=True)
	City_name = db.Column(db.String(255), nullable=False)
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
  
 
    return render_template("index.html", report = data)

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
	app.run()