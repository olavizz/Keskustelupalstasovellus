Sovelluksen tila:

- Sovellukseen pystyy kirjautumaan ja tekemään käyttäjän.
- Sovellukseen pystyy lisäämään keskusteluaiheen ja liittymään keskusteluun ja myös lähettää viestejä.
- Viesteissä näkyvät lähettäjän nimi sekä kellonaika
- Sovelluksessa on evästeet käytössä, jolloin keskustelupalstalle ei pääse ilman kirjautumista.
- Sovelluksesta pystyy kirjautumaan ulos.

- Sovelluksesta uupuu vielä toimintoja.

Kuinka käyttää sovellusta:

1. Sovellusta ei voi testata tuotannossa vaan vain paikallisesti.

2. requirements.txt tiedostosta löytyy tarvittavat riippuvuudet, jotka on syytä asentaa.

3. app.py tiedostosta löytyy kohta -- app.config["SQLALCHEMY_DATABASE_URL"] , johon osoitteeksi kannattaa laittaa itselleen omaan tietokantaan sopiva osoite.

4. SECRET_KEY on syytä muodostaa .env tiedostoon. esim. mallia SECRET_KEY=123, muuten ei kirjautuminen onnistu.

5. Sovelluksen tulisi lähteä käyntiin venv tilasta, komentoa flask run käyttäessä.
   

# Keskustelupalstasovellus

- Käyttäjä voi kirjautua sisään tunnuksella ja salasanalla, sekä sinne voi tehdä uuden käyttäjän
- Käyttäjä voi liittyä olemassa oleviin keskusteluaiheisiin, nähdä palstan aikaisemmat keskustelut ja kirjoittaa palstalle
- Käyttäjä voi nähdä muiden käyttäjien käyttäjänimet sekä lähetettyjen julkaisujen kellonajat
- Käyttäjä voi muokata sekä poistaa omia julkaisujaan
- Käyttäjä voi myös vastailla muille, jolloin syntyy keskusteluketju
- Ylläpitäjä voi poistaa sekä lisätä aiheita
- Ylläpitäjä voi myös poistaa muiden käyttäjien julkaisuja
  