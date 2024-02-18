from flask import Flask, request, session, redirect, url_for, make_response, render_template, g
import jinja2, json, MySQLdb


app = Flask("Flask aplikacija")


app.secret_key = '_5#y2L"F4Q8z-n-xec]/'

@app.before_request
def before_request_func():
    g.connection = MySQLdb.connect(host="localhost", user="app", passwd="1234", db="Projektni")
    g.cursor = g.connection.cursor()

    if request.path == '/provjera':
        pass
    elif request.path == '/login' or request.path.startswith('/static'):
        return
    elif session.get('username') is None:
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


    elif id == '2':
        g.cursor.execute(render_template('getKorisnike.sql'))
        list_korisnika = g.cursor.fetchall()

        response = render_template('index.html', naslov='Početna stranica', username=session.get('username').capitalize(), ovlasti = session.get('ovlasti'), korisnici=list_korisnika)
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


@app.get('/korisnik/<int:id_korisnik>')
def uredi_korisnika(id_korisnik):
    g.cursor.execute(render_template('getStatuse.sql', id_korisnika=id_korisnik))
    list_status = g.cursor.fetchall()

    g.cursor.execute(render_template('getProstorije.sql'))
    list_prostorija = g.cursor.fetchall()

    g.cursor.execute(render_template('getVrata.sql'))
    list_vrata = g.cursor.fetchall()

    response = render_template('index.html', naslov='Početna stranica', username=session.get('username').capitalize(), ovlasti = session.get('ovlasti'), prostorije=list_prostorija, vrata=list_vrata, id_korisnika=id_korisnik, statusi=list_status)
    return response, 200


@app.route('/add_korisnik', methods=['POST'])
def add_korisnik():
    if request.method == 'POST':
        ime = request.form.get('ime')
        prezime = request.form.get('prezime')
        username = request.form.get('username')
        password = request.form.get('password')
        id_ovlasti = request.form.get('tip')
        rfid_kartice = request.form.get('rfid')

        # Tu treba spremit rfid_kartice u bazu pod kartice (rfid), onda treba povuc te sve katice iz baze i usporedit s ovom upisanom kako
        # bi dobio id te nove kartice koji onda spremas ispod u korisnika

        query = render_template('addKorisnik.sql', ime=ime, prezime=prezime, username=username, password=password, id_ovlasti=id_ovlasti, id_kartice=id_kartice)
        g.cursor.execute(query)

        return redirect(url_for('index'))



@app.route('/dozvola/<int:id_vrata>', methods=['POST'])
def delete_dozvolu(id_vrata):
    id_podatka = request.args.get('id_podatka')

    if id_podatka == '' or id_podatka == '1' and id_stupca is not None:
        query = render_template('deleteTemp.sql', id_temp=id_stupca)
        g.cursor.execute(query)
        if id_podatka == '1':
            return redirect(url_for('index', id=id_podatka))
        else:
            return redirect(url_for('index'))

    elif id_podatka == '2' and id_stupca is not None:
        query = render_template('deleteVlaga.sql', id_vlage=id_stupca)
        g.cursor.execute(query)
        return redirect(url_for('index', id=id_podatka))

    else:
        return
       

@app.post('/provjera')
def provjera_kartice():
    response = make_response()
    uid = request.data.decode("utf-8")
    rfid = uid[8:19]
    id_vrata = uid[29:-1]

    # Provjera dozvola korisnika
    g.cursor.execute(render_template('getDozvole.sql'))
    list_dozvola = g.cursor.fetchall()

    response.data = 'Odbijeno'
    rezultat = 2

    for dozvole in list_dozvola:
        if str(dozvole[1]) == rfid:
            id_korisnika = dozvole[0]

            if str(dozvole[2]) == id_vrata:
                response.data = 'Dozvoljeno'
                rezultat = 1

    # Spremanje pokušaja otvaranja vrata
    query = render_template('writeStatus.sql', value_kor = id_korisnika, value_vrata = int(id_vrata), value_rez = rezultat)
    g.cursor.execute(query)

    response.status_code = 201
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)