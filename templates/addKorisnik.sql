INSERT INTO korisnik (ime, prezime, username, password, id_ovlasti, id_kartice) VALUES 
    ('{{ ime }}', '{{ prezime }}', '{{ username }}', UNHEX(SHA2('{{ password }}', 256)), '{{ id_ovlasti }}', '{{ id_kartice }}',);
