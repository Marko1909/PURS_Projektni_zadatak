from flask import Flask, request, session, redirect, url_for, make_response, render_template, g
import jinja2
import MySQLdb


app = Flask("Flask aplikacija")


app.secret_key = '_5#y2L"F4Q8z-n-xec]/'

@app.before_request
def before_request_func():
    g.connection = MySQLdb.connect(host="localhost", user="app", passwd="1234", db="Projektni")
    g.cursor = g.connection.cursor()

    if request.path == '/login' or request.path.startswith('/static'):
        return
    if session.get('username') is None:
        return redirect(url_for('login'))
    

@app.after_request
def after_request_func(response):
    g.connection.commit()
    g.connection.close()
    return response


@app.get('/')
def index():
    id = request.args.get('id')
    if id == None or id == '1':   
        g.cursor.execute(render_template('getStatuse.sql', id_korisnika=session.get('id')))
        list_statusa = g.cursor.fetchall()

        response = render_template('index.html', naslov='Početna stranica', username=session.get('username').capitalize(), ovlasti = session.get('ovlasti'), statusi=list_statusa)
        return response, 200
    

    elif id == '2' and session.get('ovlasti') == '1':
        g.cursor.execute(render_template('getKorisnike.sql'))
        list_korisnika = g.cursor.fetchall()

        response = render_template('index.html', naslov='Početna stranica', username=session.get('username').capitalize(), korisnici=list_korisnika)
        return response, 200


@app.get('/login')
def login():
    response = render_template('login.html', naslov='Stranica za prijavu')
    return response, 200


@app.get('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('login'))


@app.post('/login')
def provjera():
    g.cursor.execute(render_template('selectKorisnik.sql', user=request.form.get('username'), pasw=request.form.get('password')))
    korisnik = g.cursor.fetchall()

    if korisnik != ():
        session['username'] = korisnik[0][3]
        session['id'] = korisnik[0][0]
        session['ovlasti'] = korisnik[0][5]
        return redirect(url_for('index'))
    else:
        return render_template('login.html', naslov='Stranica za prijavu', poruka='Uneseni su pogrešni podatci!')
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)