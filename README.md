# MechServAI – AI-avusteinen toiminnanohjaus ja vikadiagnostiikan demo autokorjaamolle

## Projektin tavoite
Tässä projektissa oli tarkoitus tehdä autokorjaamolla käytettävä toiminnanohjausjärjestelmä, mikä hyödyntää tekoälyä vikojen diagnosoimisessa. Projektissa käytettiin n8n-sovellusta paikallisesti asennettuna Dockerin kautta työnkulun tekemisessä.

---

## Käyttöönotto ja käynnistys (CMD-komennot)

### 1) Aktivoi virtuaaliympäristö ja käynnistä Streamlit (asiakas/työnjohtaja)
```bash
servai-env\Scripts\activate
cd C:\Users\Käyttäjä\mechServAI
python -m streamlit run asiakas_app.py
```

### 2) Käynnistä n8n Dockerissa ja avaa käyttöliittymä
```bash
docker start n8n
```
Avataan selaimessa osoitteessa http://localhost:5678

### 3) Käynnistä API-palvelu
```bash
uvicorn api_app:app --reload --port 8000
```

### 4) Käynnistä Streamlit (mekaanikko)
```bash
python -m streamlit run mekaanikko_app.py
```

## Projektin alkuperäinen ohjeistus

Projektin alkuperäinen tavoite oli toteuttaa AI-pohjainen toiminnanohjaus autokorjaamolle. Ajatuksena oli, että kun asiakas varaa autokorjaamon tiskillä (tai vaihtoehtoisesti sähköisesti) ajan esimerkiksi jakohihnan vaihtoon, korjaamoesimies syöttää (tai asiakas täyttää) auton tiedot sekä tarvittavan työn. Tämän perusteella MechServAI etsii kyseiseen automalliin sopivan ohjeajan, hakee varaosaohjelmista sopivat osat hintoineen ja tekee ehdotuksen sopivasta ajankohdasta, mekaanikosta sekä nosturipaikasta.

Kun varaus on muodostettu, mekaanikolle toimitetaan omaan sovellukseen auton tiedot, varattu kalenteriaika sekä huolto-ohjeet kyseiselle automallille. Työn valmistuttua mekaanikko kuittaa työn valmiiksi ja lisää selostuksen tehdystä työstä, jolloin tieto välittyy sekä asiakkaalle että tiskille. Samalla muodostuu työmääräin, johon voidaan liittää myös mahdolliset lisätyöt ja muut huomiot.

## Tehtävänannon muutos (tilaajan toive)

Projektin tilaajan toiveesta työnkulkua muutettiin siten, että tekoäly ei tee lopullisia päätöksiä itsenäisesti. Sen sijaan agentti tuottaa ehdotuksen, jonka ihminen hyväksyy ennen kuin se etenee mekaanikon näkymään. Kun mekaanikko kuittaa työn tehdyksi omassa sovelluksessaan, viesti ja toteumatiedot palautuvat takaisin autokorjaamon johtajan/työnjohtajan näkymään. Tässä kokonaisuudessa tärkeimmäksi nousi nimenomaan työn selvittäminen ja siitä johdettu ehdotus.

## Näkökulman muutos: asiakkaasta työnjohtajaksi

Projektissa painopiste siirrettiin “asiakkaan näkökulmasta” selkeämmin työnjohtajan käyttöön. Käytännössä työnjohtaja syöttää asiakkaan oire- tai ongelmakuvauksen, ja tekoälyagentti ehdottaa tämän perusteella mahdollisia toimenpiteitä ja työtehtäviä. Kun todennäköinen vika tai suunta on päätetty, työnjohtaja kirjoittaa vian kuvauksen järjestelmään.

Tämän jälkeen JavaScript-logiikka etsii avainsanojen perusteella työtä vastaavat hinnat, työajat, nosturitarpeet ja muut resurssit. Näistä muodostetaan ehdotus takaisin työnjohtajan näkymään. Mikäli työnjohtaja hyväksyy ehdotuksen, järjestelmä lähettää mekaanikolle työmääräimen. Kun mekaanikko suorittaa työn, hän kirjaa toteuman (mitä tehtiin, pitivätkö alkutiedot paikkansa, tuliko muutoksia suunnitelmaan tai lisätöitä), ja tehty työ tallennetaan kuvauksineen tehtyihin töihin.

## Yhteenveto

MechServAI on AI-avusteinen toiminnanohjausjärjestelmän demo autokorjaamolle. Siinä työnjohtaja hyödyntää tekoälyagenttia vikojen ja toimenpiteiden ehdottamiseen, n8n orkestroi työnkulun (työajat, varaosat, hinnat ja resurssit), ja ihminen hyväksyy ehdotuksen ennen kuin se siirtyy mekaanikolle. Mekaanikko kuittaa työn ja palauttaa toteumatiedot (kuvaus, muutokset ja mahdolliset lisätyöt) takaisin työnjohtajan käyttöön.
