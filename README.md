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

Projektin alkuperäinen ohjeistus oli: AI-pohjainen toiminnanohjaus, jossa:

Asiakkaan varatessa autokorjaamon tiskillä (vaihtoehtoisesti kotona sähköisesti) aikaa autonsa jakohihnan vaihtoon, korjaamoesimiehen syöttäessä (vaihtoehtoisesti asiakkaan täyttäessä sähköisesti) auton tiedot ja tarvittava työ, MechServAI:

etsii kyseiseen autoon korjauksen ohjeajan

hakee varaosaohjelmista sopivat osat hintoineen

ehdottaa aikaa sopivalle mekaanikolle ja nosturipaikalle

Mekaanikolle menee omaan sovellukseen:

kyseisen auton tiedot

kalenteriaika vaihdolle

huolto-ohjeet kyseiselle automallille

Työn valmistuttua mekaanikko kuittaa sovellukseen työn valmiiksi selostuksineen, jolloin:

viesti menee asiakkaalle ja tiskille

työmääräin muodostuu ja sisältää mahdolliset lisätyöt ym.

## Tehtävänannon muutos (tilaajan toive)

Tehtävänantoa muokattiin projektin tilaajan halusta:

Agentti tekee ehdotuksen, ihminen hyväksyy ja se menee mekaanikon sivulle.

Kun mekaanikko kuittaa työn sivulla, niin viesti menee takaisin autokorjaamon johtajan sivulle.

Tärkein osa on työn selvittäminen.

## Näkökulman muutos: asiakkaasta työnjohtajaksi

Projektissa vaihdetaan “asiakkaan” näkökulma työnjohtajan näkökulmaan:

Tekoälyagentti voi ehdottaa mahdollisia toimenpiteitä/työtehtäviä asiakkaan kuvauksen perusteella.

Kun on päädytty mahdolliseen vikaan, työnjohtaja kirjoittaa vian kuvauksen.

JavaScript etsii työtä vastaavat hinnat, nosturit jne. avainsanojen perusteella.

Tästä tulee ehdotus takaisin työnjohtajan näkökulmaan, ja jos työnjohtajan mielestä kaikki on ok, niin lähetetään mekaanikon näkökulmaan työmääräin.

Kun mekaanikko on tehnyt työn, hän kirjoittaa työn kuvauksen (eli mitä tehtiin ja oliko alkutiedot väärät, muutokset suunnitelmaan jne.).

Tehty työ kuvauksineen tallennetaan tehtyihin töihin.

## Yhteenveto

MechServAI on AI-avusteinen toiminnanohjausjärjestelmän demo autokorjaamolle, jossa:

työnjohtaja hyödyntää tekoälyagenttia vikojen ja toimenpiteiden ehdottamiseen

n8n orkestroi työnkulun (työajat, varaosat, hinnat, resurssit)

ihminen hyväksyy ehdotuksen ennen kuin se siirtyy mekaanikolle

mekaanikko kuittaa työn ja palauttaa toteumat (kuvaus, muutokset, lisätyöt) takaisin työnjohtajalle
