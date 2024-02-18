from flask import Flask, request, session, redirect, url_for, make_response, render_template, g
import jinja2, json, MySQLdb


app = Flask("Flask aplikacija")


app.secret_key = '_5#y2L"F4Q8z-n-xec]/'


# Izvršavanje potrebnih radnji prije zahtjeva
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


# Izvršavanje potrebnih radnji nakon zahtjeva
@app.after_request
def after_request_func(response):
    g.connection.commit()
    g.connection.close()
    return response


# Prikazivanje početne stranice i prosljeđivanje na stranice home i korisnici
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


# Prikaz stranice za login
@app.get('/login')
def login():
    response = render_template('login.html', naslov='Stranica za prijavu')
    return response, 200


# Odjava korisnika sa stranice
@app.get('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('login'))


# Provjera korisničkih podataka u loginu i prosljeđivanje na početnu stranicu
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


# Prikaz stranice s korisničkim podacima (pristupno samo adminu)
@app.get('/korisnik/<int:id_korisnik>')
def uredi_korisnika(id_korisnik):
    g.cursor.execute(render_template('getStatuse.sql', id_korisnika=id_korisnik))
    list_status = g.cursor.fetchall()

    g.cursor.execute(render_template('getSveProstorije.sql'))
    list_prostorija = g.cursor.fetchall()

    g.cursor.execute(render_template('getVrata.sql'))
    list_vrata = g.cursor.fetchall()

    response = render_template('index.html', naslov='Početna stranica', username=session.get('username').capitalize(), ovlasti = session.get('ovlasti'), prostorije=list_prostorija, vrata=list_vrata, id_korisnika=id_korisnik, statusi=list_status)
    return response, 200


# Dodavanje/spremanje novog korisnika u bazu podataka
@app.route('/add_korisnik', methods=['POST'])
def add_korisnik():
    if request.method == 'POST':
        ime = request.form.get('ime')
        prezime = request.form.get('prezime')
        username = request.form.get('username')
        password = request.form.get('password')
        id_ovlasti = request.form.get('tip')
        rfid_kartice = request.form.get('rfid')

        query = render_template('addRFID.sql', rfid=rfid_kartice)
        g.cursor.execute(query)

        g.cursor.execute(render_template('getRFID.sql', rfid=rfid_kartice))
        id_nove_kartice = g.cursor.fetchall()

        query = render_template('addKorisnik.sql', ime=ime, prezime=prezime, username=username, password=password, id_ovlasti=id_ovlasti, id_kartice=id_nove_kartice[0][0])
        g.cursor.execute(query)

        return redirect(url_for('index', id=2))


# Brisanje dozvola pojedinog korisnika
@app.route('/dozvola/<int:id_vrata>', methods=['POST'])
def delete_dozvolu(id_vrata):
    id_korisnika = request.args.get('id_korisnika')

    if id_vrata and id_korisnika is not None:
        query = render_template('deleteDozvola.sql', id_korisnika=id_korisnika, id_vrata=id_vrata)
        g.cursor.execute(query)

        return redirect(url_for('uredi_korisnika', id_korisnik=id_korisnika))
       

# Dodavanje dozvole pojedinom korisniku
@app.route('/add_dozvolu', methods=['POST'])
def add_dozvolu():
    if request.method == 'POST':
        id_vrata = request.form.get('izbor_dozvola')
        id_korisnika = request.args.get('id_korisnika')
        
        if id_vrata != "":
            g.cursor.execute(render_template('getProstorije.sql', id_vrata=id_vrata, id_korisnika=id_korisnika))
            list_prostorija = g.cursor.fetchall()
            print(list_prostorija)
            if list_prostorija == ():
                query = render_template('addDozvolu.sql', id_korisnika=id_korisnika, id_vrata=id_vrata)
                g.cursor.execute(query)

                return redirect(url_for('uredi_korisnika', id_korisnik=id_korisnika))
            
            else:
                return redirect(url_for('uredi_korisnika', id_korisnik=id_korisnika))
            
        else:
            return redirect(url_for('uredi_korisnika', id_korisnik=id_korisnika))


# Provjera dozvole očitane kartice i spremanje pokušaja ulaska
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