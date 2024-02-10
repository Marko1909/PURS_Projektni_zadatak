SELECT CONCAT(ime, ' ', prezime) as korisnik, prostorija, datum, odobrenje FROM status_korisnika
LEFT JOIN korisnik ON status_korisnika.id_korisnika = korisnik.id
LEFT JOIN vrata ON status_korisnika.id_vrata = vrata.id
LEFT JOIN rezultat ON status_korisnika.id_rezultata = rezultat.id
WHERE id_korisnika = '{{id_korisnika}}'