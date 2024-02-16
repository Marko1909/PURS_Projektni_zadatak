SELECT id_korisnika, rfid, id_vrata FROM dozvole_korisnika
LEFT JOIN korisnik ON dozvole_korisnika.id_korisnika = korisnik.id
LEFT JOIN kartice ON korisnik.id_kartice = kartice.id