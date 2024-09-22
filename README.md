Sovelluksen tila:

- Sovellukseen pystyy kirjautumaan ja tekemään käyttäjän.
- Sovellukseen pystyy lisäämään keskusteluaiheen ja liittymään keskusteluun ja myös lähettää viestejä.
- Sovelluksesta pystyy kirjautumaan ulos.

- Sovelluksesta uupuu vielä toimintoja.

Kuinka käyttää sovellusta:

1. Sovellusta ei voi testa tuotannossa vaan vain paikallisesti.

2. app.py tiedostosta löytyy kohta -- app.config["SQLALCHEMY_DATABASE_URI"] , johon osoitteeksi kannattaa laittaa itselleen omaan tietokantaan sopiva osoite.

3. SECRET_KEY on syytä muodostaa .env tiedostoon. esim. mallia SECRET_KEY=123, muuten ei kirjautuminen onnistu.

4. Sovelluksen tulisi lähteä käyntiin venv tilasta, komentoa flask run käyttäessä.
   

# Keskustelupalstasovellus

- Käyttäjä voi kirjautua sisään tunnuksella ja salasanalla, sekä sinne voi tehdä uuden käyttäjän
- Käyttäjä voi liittyä olemassa oleviin keskusteluaiheisiin, nähdä palstan aikaisemmat keskustelut ja kirjoittaa palstalle
- Käyttäjä voi nähdä muiden käyttäjien käyttäjänimet sekä lähetettyjen julkaisujen kellonajat
- Käyttäjä voi muokata sekä poistaa omia julkaisujaan
- Käyttäjä voi myös vastailla muille, jolloin syntyy keskusteluketju
- Ylläpitäjä voi poistaa sekä lisätä aiheita
- Ylläpitäjä voi myös poistaa muiden käyttäjien julkaisuja
  