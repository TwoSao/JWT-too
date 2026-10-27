# JWT Mini-API

## Kirjeldus

Rakendus on loodud Pythonis, kasutades Flaski ja PyJWT teeki. Rakendus võimaldab kasutajal sisse logida ning kasutada JWT-tokeniga kaitstud lõpp-punkte.

## Kasutajad testimiseks

| Kasutajanimi | Parool | Roll |
|---|---|---|
| mari | maasikas1 | student |
| juhan | admin123 | admin |

## Paigaldamine

1. Paigalda Python 3.
2. Ava terminal projekti kaustas.
3. Paigalda vajalikud teegid:

```powershell
python -m pip install Flask PyJWT
```

## Käivitamine

Määra salajane võti keskkonnamuutujana:

```powershell
$env:JWT_SECRET_KEY = "minu_test_saladuslik_voti_2026"
```

Käivita rakendus:

```powershell
python app.py
```

Server töötab aadressil `http://127.0.0.1:5000`.

## Lõpp-punktid

- `POST /login` – kontrollib kasutajanime ja parooli ning tagastab JWT-tokeni, mis kehtib 5 minutit.
- `GET /profiil` – tagastab tokeni andmed, kui token on kehtiv.
- `GET /admin` – võimaldab juurdepääsu ainult administraatori rolliga kasutajale.

## Turvalisus

- Salajane võti loetakse keskkonnamuutujast `JWT_SECRET_KEY`.
- Kasutatakse ainult algoritmi `HS256`.
- Vigase või puuduva tokeni korral tagastatakse HTTP 401.
- Ebapiisavate õiguste korral tagastatakse HTTP 403.

## Testimine

Rakenduse testimiseks kasuta PowerShelli või Postmani. Testjuhtumid ja nende tulemused on dokumenteeritud Notioni andmebaasis **JWT testjuhud**.
