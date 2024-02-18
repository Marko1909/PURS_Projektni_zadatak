SELECT id_korisnika, prostorija, id_vrata FROM dozvole_korisnika
LEFT JOIN vrata ON dozvole_korisnika.id_vrata = vrata.id
