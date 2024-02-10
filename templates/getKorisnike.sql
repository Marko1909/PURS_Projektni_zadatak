SELECT korisnik.id, CONCAT(ime, ' ', prezime) as korisnik, ovlast, rfid FROM korisnik
LEFT JOIN ovlasti ON korisnik.id_ovlasti = ovlasti.id
LEFT JOIN kartice ON korisnik.id_kartice = kartice.id
