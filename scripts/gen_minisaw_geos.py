#!/usr/bin/env python3
"""Publish MiniSawX landings + thank-you pages for LV, GR, BG, CZ, ES, LT, PL, PT."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GSH = Path("/Users/tommasoviscomi/gadgetspothub.com")
IT_LANDING = (ROOT / "mini-saw" / "index.html").read_text(encoding="utf-8")
IT_TY = (ROOT / "mini-saw" / "thank-you.html").read_text(encoding="utf-8")

GRH_UID = "018e3961-c73a-7965-8fc1-b1d91c869a42"
GRH_WEBHOOK = "https://hook.eu2.make.com/i7pmea9fmpnepx94e5z6dxfwvl1bnnlh"
GRH_KEY = "bb9bb46add2c9a64d7a6da26437ad8640be0540b"

GTAG = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=AW-18421446541"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'AW-18421446541');
</script>"""

ACQUISTO = """<!-- Event snippet for Acquisto conversion page -->
<script>
  gtag('event', 'conversion', {
      'send_to': 'AW-18421446541/NwLsCNDM2ewcEI3vg9BE',
      'transaction_id': ''
      // 'new_customer': true /* calculate dynamically, populate with true/false */,
  });
</script>"""

CACHE_IMGS = ("hero.webp", "benefit1.webp", "benefit2.webp", "benefit3.webp", "rw1.webp", "rw2.webp", "rw3.webp")

GSH_GEOS = {
    "es": {"src": "mini-saw-es", "lang": "es", "price": 69, "display": "69,00€", "old": "230,00€", "currency": "EUR", "cta": "Descubre más →",
           "desc": "MiniSawX: motosierra eléctrica telescópica. Corta ramas a 5 metros y madera de hasta 35 cm, sin escalera y sin gasolina. 2 baterías 48 V."},
    "cz": {"src": "mini-saw-cz", "lang": "cs", "price": 1799, "display": "1 799 Kč", "old": "5 990 Kč", "currency": "CZK", "cta": "Zjistit více →",
           "desc": "MiniSawX: elektrická teleskopická pila. Řeže větve v 5 metrech a dřevo až 35 cm, bez žebříku a bez benzínu. 2 baterie 48 V."},
    "lt": {"src": "mini-saw-lt", "lang": "lt", "price": 64, "display": "64,00€", "old": "213,00€", "currency": "EUR", "cta": "Sužinokite daugiau →",
           "desc": "MiniSawX: elektrinis teleskopinis pjūklas. Pjauna šakas 5 metrų aukštyje ir medieną iki 35 cm, be kopėčių ir be benzino. 2 baterijos 48 V."},
    "pl": {"src": "mini-saw-pl", "lang": "pl", "price": 399, "display": "399 zł", "old": "1 330 zł", "currency": "PLN", "cta": "Dowiedz się więcej →",
           "desc": "MiniSawX: elektryczna pilarka teleskopowa. Przycina gałęzie na 5 metrach i drewno do 35 cm, bez drabiny i bez benzyny. 2 baterie 48 V."},
    "pt": {"src": "mini-saw-pt", "lang": "pt", "price": 79, "display": "79,00€", "old": "263,00€", "currency": "EUR", "cta": "Saiba mais →",
           "desc": "MiniSawX: motosserra elétrica telescópica. Corta ramos a 5 metros e madeira até 35 cm, sem escada e sem gasolina. 2 baterias 48 V."},
}

# offer/lp from zafflow; GRH Adrice credentials (user can replace scripts later)
NEW_GEOS = {
    "lv": {
        "lang": "lv", "price": 79, "display": "79,00€", "old": "263,00€", "short": "79 €",
        "currency": "EUR", "offer": "3518", "lp": "3555", "cta": "Uzzināt vairāk →",
        "desc": "MiniSawX: elektriskais teleskopiskais zāģis. Zāģē zarus 5 metru augstumā un koku līdz 35 cm, bez kāpnēm un bez benzīna. 2 baterijas 48 V.",
        "cookie": ("Mēs izmantojam tehniskās un trešo pušu sīkdatnes, lai uzlabotu jūsu pieredzi un analītikai.", "Pieņemt", "Uzzināt vairāk"),
        "submit": "Nosūta...",
        "form": ("Vārds un uzvārds*", "Jānis Bērziņš", "Tālruņa numurs*", "+371 21 234 567", "Piegādes adrese*", "Brīvības iela 10, LV-1010 Rīga"),
    },
    "gr": {
        "lang": "el", "price": 89, "display": "89,00€", "old": "297,00€", "short": "89 €",
        "currency": "EUR", "offer": "3227", "lp": "3261", "cta": "Μάθετε περισσότερα →",
        "desc": "MiniSawX: ηλεκτρικό τηλεσκοπικό αλυσοπρίονο. Κόβει κλαδιά στα 5 μέτρα και ξύλο έως 35 εκ., χωρίς σκάλα και χωρίς βενζίνη. 2 μπαταρίες 48 V.",
        "cookie": ("Χρησιμοποιούμε τεχνικά cookies και cookies τρίτων για καλύτερη εμπειρία και ανάλυση.", "Αποδοχή", "Περισσότερα"),
        "submit": "Αποστολή...",
        "form": ("Ονοματεπώνυμο*", "Γιώργος Παπαδόπουλος", "Τηλέφωνο*", "+30 691 234 5678", "Διεύθυνση παράδοσης*", "Ερμού 15, 10563 Αθήνα"),
    },
    "bg": {
        "lang": "bg", "price": 89, "display": "89,00€", "old": "297,00€", "short": "89 €",
        "currency": "EUR", "offer": "3226", "lp": "3260", "cta": "Научете повече →",
        "desc": "MiniSawX: електрически телескопичен верижен трион. Реже клони на 5 метра и дърво до 35 см, без стълба и без бензин. 2 батерии 48 V.",
        "cookie": ("Използваме технически бисквитки и бисквитки на трети страни, за да подобрим вашето изживяване и за анализ.", "Приемам", "Научете повече"),
        "submit": "Изпращане...",
        "form": ("Име и фамилия*", "Иван Иванов", "Телефон*", "+359 88 123 4567", "Адрес за доставка*", "бул. Витоша 1, 1000 София"),
    },
}


def apply_pairs(text: str, pairs: list[tuple[str, str]]) -> str:
    ordered = sorted(pairs, key=lambda x: len(x[0]), reverse=True)
    for old, new in ordered:
        text = text.replace(old, new)
    return text


def cache_bust(html: str) -> str:
    for name in CACHE_IMGS:
        html = re.sub(
            rf"(/assets/img/products/saw3000x/{re.escape(name)})(?!\?v=)",
            r"\1?v=20260905",
            html,
        )
    return html


def swap_gtag(html: str, thank_you: bool) -> str:
    html = re.sub(
        r"<!-- Google tag \(gtag\.js\) -->\s*<script async src=\"https://www\.googletagmanager\.com/gtag/js\?id=AW-[^\"]+\"></script>\s*<script>.*?</script>",
        GTAG,
        html,
        count=1,
        flags=re.S,
    )
    html = html.replace("AW-18358316754", "AW-18421446541")
    html = re.sub(
        r"<!-- Event snippet for Purchase conversion page -->\s*<script>.*?</script>\s*",
        "",
        html,
        flags=re.S,
    )
    if thank_you and "NwLsCNDM2ewcEI3vg9BE" not in html:
        html = html.replace(
            "  gtag('config', 'AW-18421446541');\n</script>",
            "  gtag('config', 'AW-18421446541');\n</script>\n" + ACQUISTO,
            1,
        )
    return html


def branding(html: str) -> str:
    html = html.replace("https://gadgetspothub.com", "https://gadgetroomhub.com")
    html = html.replace("gadgetspothub.com", "gadgetroomhub.com")
    html = html.replace("gadgetspothub", "gadgetroomhub")
    html = html.replace("info@gadgetroomhub.com", "info@gadgetroomhub.com")
    html = html.replace("Saw 3000X", "MiniSawX")
    html = html.replace("Netmart LLC", "WHATECH MOBILE CO., LIMITED")
    html = html.replace(
        "County of Sussex 16192 Coastal Hwy, Lewes, DE 19958-3608, United States",
        "Room 505, 5th floor, Beverley Commercial Centre, 87-105 Chatham Road South, Hong Kong",
    )
    html = html.replace("County of Sussex 16192 Coastal Hwy", "Room 505, 5th floor, Beverley Commercial Centre")
    html = html.replace("Lewes, DE 19958-3608, United States", "87-105 Chatham Road South, Hong Kong")
    return html


FOOTERS = {
    "lv": {
        "heading": "Informācija",
        "contact": "Kontakti",
        "blurb": "Noderīgi produkti ikdienai, piegāde 24–48 stundās ar pēcmaksu.",
        "rights": "Visas tiesības aizsargātas",
        "links": [
            ("/lv/about-us.html", "Par mums"),
            ("/lv/contact-us.html", "Sazinieties ar mums"),
            ("/lv/privacy-policy.html", "Privātuma politika"),
            ("/lv/terms-conditions.html", "Noteikumi un nosacījumi"),
            ("/lv/cookie-policy.html", "Sīkdatņu politika"),
            ("/lv/shipping-policy.html", "Piegādes politika"),
            ("/lv/refund-policy.html", "Atmaksas politika"),
        ],
    },
    "gr": {
        "heading": "Πληροφορίες",
        "contact": "Επικοινωνία",
        "blurb": "Χρήσιμα προϊόντα για την καθημερινότητα, παράδοση σε 24–48 ώρες με αντικαταβολή.",
        "rights": "Με επιφύλαξη παντός δικαιώματος",
        "links": [
            ("/gr/about-us.html", "Σχετικά με εμάς"),
            ("/gr/contact-us.html", "Επικοινωνήστε μαζί μας"),
            ("/gr/privacy-policy.html", "Πολιτική Απορρήτου"),
            ("/gr/terms-conditions.html", "Όροι και Προϋποθέσεις"),
            ("/gr/cookie-policy.html", "Πολιτική cookie"),
            ("/gr/shipping-policy.html", "Πολιτική Αποστολής"),
            ("/gr/refund-policy.html", "Πολιτική επιστροφής"),
        ],
    },
    "bg": {
        "heading": "Информация",
        "contact": "Контакт",
        "blurb": "Полезни продукти за ежедневието, доставка за 24–48 часа с наложен платеж.",
        "rights": "Всички права запазени",
        "links": [
            ("/bg/about-us.html", "За нас"),
            ("/bg/contact-us.html", "Свържете се с нас"),
            ("/bg/privacy-policy.html", "Политика за поверителност"),
            ("/bg/terms-conditions.html", "Правила и условия"),
            ("/bg/cookie-policy.html", "Политика за бисквитки"),
            ("/bg/shipping-policy.html", "Политика за доставка"),
            ("/bg/refund-policy.html", "Политика за възстановяване"),
        ],
    },
}


def landing_footer(geo: str) -> str:
    f = FOOTERS[geo]
    links = "\n".join(f'          <li><a href="{href}">{label}</a></li>' for href, label in f["links"])
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="site-footer__grid">
      <div>
        <a href="/" class="site-logo" aria-label="gadgetroomhub.com home">
          <span class="site-logo__text"><span class="site-logo__text-primary">gadgetroomhub</span><span class="site-logo__text-accent">.com</span></span>
        </a>
        <p class="site-footer__blurb">{f["blurb"]}</p>
      </div>
      <div>
        <h4 class="site-footer__heading">{f["heading"]}</h4>
        <ul class="site-footer__list">
{links}
        </ul>
      </div>
      <div>
        <h4 class="site-footer__heading">{f["contact"]}</h4>
        <ul class="site-footer__list">
          <li><strong>WHATECH MOBILE CO., LIMITED</strong></li>
          <li>Room 505, 5th floor, Beverley Commercial Centre</li>
          <li>87-105 Chatham Road South, Hong Kong</li>
          <li><a href="mailto:info@gadgetroomhub.com">info@gadgetroomhub.com</a></li>
        </ul>
      </div>
    </div>
    <div class="site-footer__bottom">
      © <span data-year>2026</span> <strong>WHATECH MOBILE CO., LIMITED</strong> — {f["rights"]}.
      <a href="/">gadgetroomhub.com</a>
    </div>
  </div>
</footer>"""


def ty_footer(geo: str) -> str:
    f = FOOTERS[geo]
    links = "\n".join(f'        <li><a href="{href}">{label}</a></li>' for href, label in f["links"])
    return f"""<footer class="site-footer"><div class="container">
  <div class="site-footer__grid">
    <div>
      <a href="/" class="site-logo">
        <span class="site-logo__text" style="display:inline"><span class="site-logo__text-primary">gadgetroomhub</span><span class="site-logo__text-accent">.com</span></span>
      </a>
    </div>
    <div>
      <h4 class="site-footer__heading">{f["heading"]}</h4>
      <ul class="site-footer__list">
{links}
      </ul>
    </div>
    <div>
      <h4 class="site-footer__heading">{f["contact"]}</h4>
      <ul class="site-footer__list">
        <li><strong>WHATECH MOBILE CO., LIMITED</strong></li>
        <li>Room 505, 5th floor, Beverley Commercial Centre, 87-105 Chatham Road South, Hong Kong</li>
        <li><a href="mailto:info@gadgetroomhub.com">info@gadgetroomhub.com</a></li>
      </ul>
    </div>
  </div>
  <div class="site-footer__bottom">© <span data-year>2026</span> <strong>WHATECH MOBILE CO., LIMITED</strong> — {f["rights"]}. <a href="/">gadgetroomhub.com</a></div>
</div></footer>"""


LV = [
    ("MiniSawX — Motosega elettrica telescopica | 59,00€", "MiniSawX — Elektriskais teleskopiskais zāģis | 79,00€"),
    ("MiniSawX: taglia i rami a 5 metri e il legno fino a 35 cm, senza scala e senza benzina. 2 batterie 48 V. Pagamento alla consegna. Oggi 59,00€ invece di 196,00€.",
     "MiniSawX: zāģē zarus 5 metru augstumā un koku līdz 35 cm, bez kāpnēm un bez benzīna. 2 baterijas 48 V. Pēcmaksa. Šodien 79,00€, nevis 263,00€."),
    ("SUBMITTING_LABEL: 'Invio...'", "SUBMITTING_LABEL: 'Nosūta...'"),
    ("COOKIE_TEXT: 'Usiamo cookie tecnici e di terze parti per migliorare la tua esperienza e per analisi.'",
     "COOKIE_TEXT: 'Mēs izmantojam tehniskās un trešo pušu sīkdatnes, lai uzlabotu jūsu pieredzi un analītikai.'"),
    ("COOKIE_ACCEPT: 'Accetta'", "COOKIE_ACCEPT: 'Pieņemt'"),
    ("COOKIE_LEARN: 'Scopri di più'", "COOKIE_LEARN: 'Uzzināt vairāk'"),
    ("✅ Pagamento alla consegna · Spedizione gratuita 24/48h", "✅ Pēcmaksa · Bezmaksas piegāde 24/48h"),
    ("Taglia i rami più alti e i tronchi più grossi senza scala.", "Nozāģē augstākos zarus un resnākos stumbrus bez kāpnēm."),
    ("Senza benzina. Senza fatica. Fino a 5 metri.", "Bez benzīna. Bez piepūles. Līdz 5 metriem."),
    ("MiniSawX: motosega elettrica telescopica. In pochi secondi passa dal modo manuale compatto all’asta. Taglia il legno fino a <b>35 cm</b> di diametro, arriva a <b>5 metri</b> e pesa solo <b>700 g</b>. Fatta per il giardino, gli alberi da frutto e lo spazio intorno a casa.",
     "MiniSawX: elektriskais teleskopiskais zāģis. Dažās sekundēs pāriet no kompaktā rokas režīma uz kātu. Zāģē koku līdz <b>35 cm</b> diametrā, sasniedz <b>5 metrus</b> un sver tikai <b>700 g</b>. Radīts dārzam, augļu kokiem un pagalmam."),
    ("Kit completo MiniSawX", "Pilns MiniSawX komplekts"),
    ("🔥 Restano solo <strong>4 kit</strong> a questo prezzo", "🔥 Atlikuši tikai <strong>4 komplekti</strong> par šo cenu"),
    ("<strong>3.000 W e asta telescopica fino a 5 metri.</strong>\n            Dove un decespugliatore normale si ferma, la MiniSawX continua. Attraversa legno verde o secco, rami grossi e tronchi fino a 35 cm.",
     "<strong>3 000 W un teleskopiskais kāts līdz 5 metriem.</strong>\n            Kur parasts trimmeris apstājas, MiniSawX turpina. Iet cauri zaļam vai sausam kokam, resniem zariem un stumbriem līdz 35 cm."),
    ("<strong>2 batterie da 48 V e 8.000 mAh.</strong>\n            Una al lavoro, l’altra in carica in 45 min. Niente benzina, niente miscela, niente cavi tra i piedi.",
     "<strong>2 baterijas 48 V un 8 000 mAh.</strong>\n            Viena strādā, otra uzlādējas 45 min. Bez benzīna, bez maisījuma, bez vadiem zem kājām."),
    ("<strong>Pesa 700 g — la controlli con una mano.</strong>\n            Meno fatica su braccia, spalle e schiena, anche nei lavori più lunghi. Freno istantaneo.",
     "<strong>Sver 700 g — vadāma ar vienu roku.</strong>\n            Mazāka slodze rokām, pleciem un mugurai arī ilgākā darbā. Tūlītēja bremze."),
    ("<strong>AutoChain X™ lubrifica e tende da sola.</strong>\n            Olio sempre al posto giusto, tensione corretta, zero pause per regolare la catena.",
     "<strong>AutoChain X™ eļļo un spriego pati.</strong>\n            Eļļa vienmēr īstajā vietā, pareizs spriegums, nekādu paužu ķēdes regulēšanai."),
    ("<strong>4,9/5 — più di 8.730 giardini già sistemati.</strong>\n            Garanzia ufficiale 2 anni. 30 giorni per rese. Paghi solo quando arriva il corriere.",
     "<strong>4,9/5 — vairāk nekā 8 730 sakoptu dārzu.</strong>\n            Oficiāla 2 gadu garantija. 30 dienas atgriešanai. Maksā tikai, kad ierodas kurjers."),
    ("Sì, voglio la MiniSawX", "Jā, es gribu MiniSawX"),
    ("💵 Paghi alla consegna", "💵 Maksā piegādes brīdī"),
    ("↩️ 30 giorni di prova", "↩️ 30 dienu izmēģinājums"),
    ("🚚 Spedizione gratuita", "🚚 Bezmaksas piegāde"),
    ("ACQUISTO SICURO • SPEDIZIONE GRATUITA • GARANZIA COMPLETA", "DROŠS PIRKUMS • BEZMAKSAS PIEGĀDE • PILNA GARANTIJA"),
    ("<strong>Spedizione gratuita</strong><br>\n        Consegna in tutta Italia, in 24–48 ore.",
     "<strong>Bezmaksas piegāde</strong><br>\n        Piegāde visā Latvijā, 24–48 stundu laikā."),
    ("<strong>Pagamento alla consegna</strong><br>\n        Niente carta e niente anticipo: paghi solo quando arriva il pacco",
     "<strong>Pēcmaksa</strong><br>\n        Bez kartes un bez avansa: maksā tikai, kad paka ir klāt"),
    ("<strong>Acquisto protetto</strong><br>\n        I tuoi dati personali sono protetti al 100%",
     "<strong>Aizsargāts pirkums</strong><br>\n        Jūsu personas dati ir 100% aizsargāti"),
    ("<strong>Garanzia 2 anni</strong><br>\n        Puoi restituirlo senza pensieri entro 30 giorni",
     "<strong>2 gadu garantija</strong><br>\n        Variat atgriezt bez raizēm 30 dienu laikā"),
    ("Disponibilità in magazzino", "Pieejamība noliktavā"),
    ("RESTANO SOLO <span>4</span> KIT", "ATLIKUŠI TIKAI <span>4</span> KOMPLEKTI"),
    ("Importante!", "Svarīgi!"),
    ("Il magazzino si sta svuotando in fretta!", "Noliktava tukšojas ātri!"),
    ("In questo momento tante altre persone stanno guardando la MiniSawX: per questo i kit disponibili scendono così in fretta.",
     "Šobrīd MiniSawX skatās daudz citu cilvēku: tāpēc komplekti sarūk tik ātri."),
    ("Ordina ora e assicurati uno degli ultimi kit al prezzo di oggi, con −70%.",
     "Pasūtiet tagad un rezervējiet vienu no pēdējiem komplektiem par šodienas cenu ar −70%."),
    ("Prenota la MiniSawX a soli 59 €", "Rezervējiet MiniSawX tikai par 79 €"),
    ("Compila i tre campi. Ti chiamiamo entro 24 ore per confermare l’ordine e fissare la consegna. Paghi solo quando arriva il corriere.",
     "Aizpildiet trīs laukus. Mēs zvanīsim 24 stundu laikā, lai apstiprinātu pasūtījumu un piegādi. Maksājat tikai, kad ierodas kurjers."),
    ("Nome e Cognome*", "Vārds un uzvārds*"),
    ('placeholder="Mario Rossi"', 'placeholder="Jānis Bērziņš"'),
    ("Telefono*", "Tālruņa numurs*"),
    ('placeholder="+39 392 0745623"', 'placeholder="+371 21 234 567"'),
    ("Indirizzo di consegna*", "Piegādes adrese*"),
    ('placeholder="Via Torino 1, 12345 Roma Italia"', 'placeholder="Brīvības iela 10, LV-1010 Rīga"'),
    ("CONFERMA ORDINE", "APSTIPRINĀT PASŪTĪJUMU"),
    ("🔒 Nessun anticipo · Niente carta · Paghi solo alla consegna", "🔒 Bez avansa · Bez kartes · Maksā tikai piegādes brīdī"),
    ("Scala instabile e motosega a benzina: il rischio di ogni potatura", "Nestabilas kāpnes un benzīna zāģis: katras apgriešanas risks"),
    ("Quante volte sei già salito su una scala instabile solo per tagliare un ramo?",
     "Cik reižu jau esat kāpis nestabilās kāpnēs, lai nozāģētu tikai vienu zaru?"),
    ("Conosci la storia. La motosega a benzina fa un rumore assurdo, puzza di carburante e pesa 4 o 5 kg. Quella economica a batteria si blocca al primo tronco grosso. E per arrivare in cima all’albero da frutto… di nuovo la scala.",
     "Pazīstat stāstu. Benzīna zāģis trokšņo, smako pēc degvielas un sver 4–5 kg. Lētais akumulatora modelis iesprūst pie pirmā resnā stumbra. Un, lai sasniegtu augļu koka galotni… atkal kāpnes."),
    ("Allora ne compri un’altra. E il ciclo ricomincia.", "Tad pērkat nākamo. Un cikls sākas no jauna."),
    ("Nemmeno la versione a benzina ti salva: rumore, fumi, miscela, cavo di avviamento. Ogni potatura diventa una mattinata intera — e un rischio inutile in cima alla scala.",
     "Arī benzīna versija neglābj: troksnis, dūmi, maisījums, startera aukla. Katra apgriešana kļūst par veselu rītu — un lieku risku kāpņu galā."),
    ("Non è sfortuna.<br>\n          <strong>La verità è che la motosega tradizionale è nata per il suolo, non per la cima dell’albero — e quelle da pochi euro nascono per essere ricomprate.</strong>",
     "Tā nav veiksme.<br>\n          <strong>Patiesība ir tāda, ka tradicionālais zāģis radīts zemei, nevis koka galotnei — un lētie modeļi ir veidoti, lai tos pirktu atkal.</strong>"),
    ("Lubrificazione automatica della catena MiniSawX", "MiniSawX ķēdes automātiskā eļļošana"),
    ("La manutenzione che non devi più fare", "Apkope, kas vairs nav jādara"),
    ("AutoChain X™ cambia le regole della catena", "AutoChain X™ maina ķēdes noteikumus"),
    ("Con una motosega tradizionale passi il tempo a lubrificare e a tendere la catena. Senza olio, si surriscalda. Senza tensione, salta o si blocca. E il taglio si ferma a metà ramo.",
     "Ar tradicionālo zāģi jūs tērējat laiku, eļļojot un spriegojot ķēdi. Bez eļļas tā pārkarst. Bez sprieguma noslīd vai iesprūst. Un zāģējums apstājas zara vidū."),
    ("<strong>AutoChain X™ lubrifica e tende da sola.</strong>\n            Il sistema distribuisce l’olio senza sosta e tiene la tensione giusta. Le prestazioni restano stabili dal primo all’ultimo taglio.",
     "<strong>AutoChain X™ eļļo un spriego pati.</strong>\n            Sistēma nepārtraukti sadala eļļu un uztur pareizo spriegumu. Veiktspēja paliek stabila no pirmā līdz pēdējam griezumam."),
    ("<strong>È esattamente il sistema montato sulla MiniSawX.</strong>\n            Per questo continui a tagliare senza pause e senza regolazioni ogni dieci minuti.",
     "<strong>Tieši šī sistēma ir iebūvēta MiniSawX.</strong>\n            Tāpēc jūs turpināt zāģēt bez pauzēm un bez regulēšanas ik pēc desmit minūtēm."),
    ("È lo stesso ragionamento che separa un attrezzo che chiede attenzione continua da uno che semplicemente lavora: meno regolazioni, più taglio, meno manutenzione.",
     "Tas pats princips, kas atdala instrumentu, kuram vajag pastāvīgu uzmanību, no tā, kas vienkārši strādā: mazāk regulēšanas, vairāk zāģēšanas, mazāk apkopes."),
    ("Qui non è pubblicità. <b>È il sistema che fa il lavoro.</b>", "Šeit tas nav reklāmas sauklis. <b>Tā ir sistēma, kas dara darbu.</b>"),
    ("✅ I vantaggi concreti", "✅ Konkrētas priekšrocības"),
    ("Questa è la motosega che ti toglie la scala dal giardino", "Šis ir zāģis, kas izņem kāpnes no dārza"),
    ("Più potenza sui rami grossi, zero benzina, meno peso sulle braccia. E il giardino torna in ordine in un solo giorno.",
     "Vairāk jaudas resniem zariem, nulle benzīna, mazāks svars rokām. Un dārzs ir sakārtots vienā dienā."),
    ("MiniSawX con asta telescopica fino a 5 metri", "MiniSawX ar teleskopisko kātu līdz 5 metriem"),
    ("3.000 W e 5 metri — la cima dell’albero smette di essere un problema", "3 000 W un 5 metri — koka galotne vairs nav problēma"),
    ("Dove un decespugliatore normale si ferma, la MiniSawX continua. La lama attraversa legno verde e secco, rami grossi e tronchi fino a 35 cm. Vicino al suolo usi il modo manuale compatto. In cima, monti l’asta telescopica.",
     "Kur parasts trimmeris apstājas, MiniSawX turpina. Asmens iet cauri zaļam un sausam kokam, resniem zariem un stumbriem līdz 35 cm. Pie zemes lietojat kompakto rokas režīmu. Augšā uzliekat teleskopisko kātu."),
    ("Taglio da 35 cm. Potenza da 3.000 W. Altezza fino a 5 metri.", "Griezums 35 cm. Jauda 3 000 W. Augstums līdz 5 metriem."),
    ("I lavori più pesanti stanno in un solo giorno.", "Smagākie darbi ietilpst vienā dienā."),
    ("MiniSawX a batteria che taglia un tronco senza cavi", "MiniSawX ar bateriju, kas zāģē stumbru bez vadiem"),
    ("Due batterie da 48 V. Senza benzina e senza cavi", "Divas 48 V baterijas. Bez benzīna un bez vadiem"),
    ("Dimentica benzina, miscela e prolunghe che limitano i movimenti e si avvolgono ai piedi. Quando una batteria finisce, metti la seconda e vai avanti. Ricarica in 45 minuti.",
     "Aizmirstiet benzīnu, maisījumu un pagarinātājus, kas traucē un tinās ap kājām. Kad viena baterija beidzas, ievietojat otro un turpināt. Uzlāde 45 minūtēs."),
    ("48 V · 8.000 mAh · senza fili · carica in 45 min.", "48 V · 8 000 mAh · bez vadiem · uzlāde 45 min."),
    ("Ti muovi in tutta la proprietà senza dipendere da una presa.", "Pārvietojaties pa visu īpašumu, neatkarīgi no rozetes."),
    ("MiniSawX in una mano: 700 g, 48 V", "MiniSawX vienā rokā: 700 g, 48 V"),
    ("700 g. La controlli con una mano, senza distruggerti la schiena", "700 g. Vadāt ar vienu roku, nebojājot muguru"),
    ("Una motosega tradizionale pesa 4–5 kg. La MiniSawX pesa 700 g e riduce la fatica di braccia, spalle e schiena, anche nei lavori più lunghi. Il corpo compatto entra negli spazi stretti. Freno istantaneo.",
     "Tradicionālais zāģis sver 4–5 kg. MiniSawX sver 700 g un samazina slodzi rokām, pleciem un mugurai arī ilgākā darbā. Kompaktais korpuss ieiet šaurās vietās. Tūlītēja bremze."),
    ("700 g · una mano · freno istantaneo.", "700 g · viena roka · tūlītēja bremze."),
    ("Tagli con precisione dove l’attrezzo pesante non arriva nemmeno.", "Zāģējat precīzi tur, kur smagais instruments nepietiek."),
    ("Sì, voglio la MiniSawX ↓", "Jā, es gribu MiniSawX ↓"),
    ("💵 Paghi quando arriva", "💵 Maksā, kad atved"),
    ("🚚 Consegna in 24/48h", "🚚 Piegāde 24/48h"),
    ("↩️ Provalo 30 giorni", "↩️ Izmēģiniet 30 dienas"),
    ("Confronto senza filtri", "Salīdzinājums bez filtra"),
    ("Motosega tradizionale o MiniSawX?", "Tradicionālais zāģis vai MiniSawX?"),
    ("Gli stessi criteri. Senza fronzoli.", "Tie paši kritēriji. Bez liekiem vārdiem."),
    ("Tradizionale", "Tradicionālais"),
    ("⛽ Benzina, rumore e fumi", "⛽ Benzīns, troksnis un dūmi"),
    ("Batteria, senza benzina", "Baterija, bez benzīna"),
    ("🏋️ 4–5 kg", "🏋️ 4–5 kg"),
    ("Solo 700 g", "Tikai 700 g"),
    ("🪜 Ti serve una scala", "🪜 Vajag kāpnes"),
    ("Asta fino a 5 metri", "Kāts līdz 5 metriem"),
    ("🔧 Regolazioni continue", "🔧 Pastāvīga regulēšana"),
    ("🛢️ Rifornimento di benzina", "🛢️ Benzīna uzpilde"),
    ("Due batterie da 48 V", "Divas 48 V baterijas"),
    ("⭐ Più di 8.730 giardini", "⭐ Vairāk nekā 8 730 dārzi"),
    ("Chi la prova non la molla più", "Kas izmēģina, vairs nelaid vaļā"),
    ("C’è chi lascia la benzina e chi ha già bruciato soldi su versioni economiche: è questo che li porta a scegliere la MiniSawX.",
     "Vieni atstāj benzīnu, citi jau iztērējuši naudu lētajos modeļos: tāpēc viņi izvēlas MiniSawX."),
    ("Roberto G. — MiniSawX in uso", "Roberto G. — MiniSawX darbībā"),
    ("“La catena attraversa in fretta anche i rami secchi più grossi, senza fatica e senza bloccarsi. Pensavo di dover usare molta più forza, invece basta guidarla con una mano.”",
     "“Ķēde ātri iet cauri arī resnākajiem sausajiem zariem, bez piepūles un bez iesprūšanas. Domāju, ka vajadzēs daudz vairāk spēka, bet pietiek vadīt ar vienu roku.”"),
    ("✅ Una potenza sorprendente", "✅ Pārsteidzoša jauda"),
    ("David M. — MiniSawX in mano", "David M. — MiniSawX rokā"),
    ("“È potente, comoda da tenere in mano e facile da usare, anche per chi non aveva mai preso una motosega. In un pomeriggio ho potato tutti gli alberi da frutto del giardino.”",
     "“Tā ir jaudīga, ērta rokā un vienkārši lietojama pat tam, kurš nekad nav ņēmis zāģi. Vienā pēcpusdienā apgriezu visus dārza augļu kokus.”"),
    ("✅ Fa il suo lavoro", "✅ Dara savu darbu"),
    ("Miguel T. — MiniSawX con asta telescopica", "Miguel T. — MiniSawX ar teleskopisko kātu"),
    ("“L’asta telescopica arriva senza fatica ai rami più alti, quindi non devo più salire su una scala instabile. Ho finito in metà tempo e mi sono sentito molto più sicuro.”",
     "“Teleskopiskais kāts bez piepūles sasniedz augstākos zarus, tāpēc man vairs nav jākāpj nestabilās kāpnēs. Pabeidzu uz pusi īsākā laikā un jutos daudz drošāk.”"),
    ("✅ Più veloce e più sicura", "✅ Ātrāk un drošāk"),
    ("📦 Tutto incluso", "📦 Viss iekļauts"),
    ("Kit completo MiniSawX.<br>\n        Niente extra. Niente sorprese.", "Pilns MiniSawX komplekts.<br>\n        Nekādu piemaksu. Nekādu pārsteigumu."),
    ("Apri la scatola, monti e inizi a tagliare. Non manca niente.", "Atverat kasti, saliekat un sākat zāģēt. Nekā netrūkst."),
    ("Kit completo MiniSawX — tutto quello che c’è nel pacco", "Pilns MiniSawX komplekts — viss, kas ir pakā"),
    ("Cosa c’è nella scatola", "Kas ir kastē"),
    ("A cosa serve davvero", "Kam tas patiešām noder"),
    ("⚙️ Motosega elettrica MiniSawX", "⚙️ Elektriskais zāģis MiniSawX"),
    ("3.000 W in modalità compatta — il cuore del kit", "3 000 W kompaktajā režīmā — komplekta sirds"),
    ("🪜 Asta telescopica fino a 5 metri", "🪜 Teleskopiskais kāts līdz 5 metriem"),
    ("Arrivi in cima all’albero senza scala", "Sasniedzat koka galotni bez kāpnēm"),
    ("🔋 2 batterie da 48 V e 8.000 mAh", "🔋 2 baterijas 48 V un 8 000 mAh"),
    ("Una al lavoro, l’altra in carica — non ti fermi", "Viena strādā, otra uzlādējas — jūs neapstājaties"),
    ("⚡ Caricabatterie rapido", "⚡ Ātrais lādētājs"),
    ("45 minuti e torni a tagliare", "45 minūtes un atkal zāģējat"),
    ("⛓️ 2 catene di ricambio", "⛓️ 2 rezerves ķēdes"),
    ("Non resti a metà ramo senza catena", "Nepaliekiet zara vidū bez ķēdes"),
    ("🛢️ Serbatoio olio + AutoChain X™", "🛢️ Eļļas tvertne + AutoChain X™"),
    ("Lubrifica e tende da sola — manutenzione minima", "Eļļo un spriego pati — minimāla apkope"),
    ("🧰 Set di attrezzi e valigetta", "🧰 Instrumentu komplekts un koferis"),
    ("Tutto al suo posto, pronto da riporre", "Viss savā vietā, gatavs novietošanai"),
    ("🛡️ Garanzia ufficiale 2 anni", "🛡️ Oficiāla 2 gadu garantija"),
    ("Assistenza inclusa — 30 giorni per il reso", "Palīdzība iekļauta — 30 dienas atgriešanai"),
    ("❓ Le domande più frequenti", "❓ Biežākie jautājumi"),
    ("Qualche dubbio? È normale.<br>\n        Lo chiarisco tutto qui.", "Šaubas? Tas ir normāli.<br>\n        Šeit ir visas atbildes."),
    ("Prima di ordinare, le risposte alle domande di sempre: consegna, pagamento, benzina, rami alti e reso.",
     "Pirms pasūtīšanas atbildes uz ierastajiem jautājumiem: piegāde, apmaksa, benzīns, augsti zari un atgriešana."),
    ("Quando arriva l’ordine?", "Kad ierodas pasūtījums?"),
    ("La consegna richiede circa 1–2 giorni lavorativi. Spedizione gratuita in tutta Italia.",
     "Piegāde aizņem aptuveni 1–2 darba dienas. Bezmaksas piegāde visā Latvijā."),
    ("Devo pagare in anticipo?", "Vai jāmaksā avansā?"),
    ("No. Paghi direttamente al corriere al momento della consegna. Niente carta. Niente anticipo.",
     "Nē. Maksājat kurjeram piegādes brīdī. Bez kartes. Bez avansa."),
    ("Serve la benzina?", "Vai vajag benzīnu?"),
    ("No. La MiniSawX funziona solo a batteria: due da 48 V e 8.000 mAh. Niente miscela, niente fumi, niente cavo di avviamento.",
     "Nē. MiniSawX darbojas tikai ar bateriju: divas 48 V un 8 000 mAh. Bez maisījuma, bez dūmiem, bez startera auklas."),
    ("Riesco a tagliare i rami alti senza scala?", "Vai varu zāģēt augstos zarus bez kāpnēm?"),
    ("Sì. L’asta telescopica arriva fino a 5 metri. Vicino al suolo usi il modo manuale compatto. In cima all’albero, monti l’asta.",
     "Jā. Teleskopiskais kāts sasniedz 5 metrus. Pie zemes lietojat kompakto rokas režīmu. Koka galotnē uzliekat kātu."),
    ("E se poi non mi convince?", "Un ja tomēr neapmierina?"),
    ("Hai 30 giorni per chiedere il reso, secondo le condizioni di rimborso. Non rischi niente.",
     "Jums ir 30 dienas, lai lūgtu atgriešanu saskaņā ar atmaksas noteikumiem. Neriskējat neko."),
    ("✅ Paghi quando arriva", "✅ Maksā, kad atved"),
    ("INSERISCI I DATI DI CONSEGNA", "IEVADIET PIEGĀDES DATUS"),
    ("L’ordine parte subito. Paghi solo alla consegna, direttamente al corriere.",
     "Pasūtījums sākas uzreiz. Maksājat tikai piegādes brīdī, tieši kurjeram."),
]

LV_TY = [
    ("Ordine ricevuto — Attendi la chiamata di conferma | MiniSawX", "Pasūtījums saņemts — Gaidiet apstiprinājuma zvanu | MiniSawX"),
    ("Il tuo ordine MiniSawX è stato registrato. Manca solo un ultimo passaggio: rispondi alla chiamata di conferma del nostro operatore.",
     "Jūsu MiniSawX pasūtījums ir reģistrēts. Atlicis pēdējais solis: atbildiet uz mūsu operatora apstiprinājuma zvanu."),
    ("Il tuo ordine MiniSawX è stato registrato!", "Jūsu MiniSawX pasūtījums ir reģistrēts!"),
    ("Perfetto — il tuo ordine è in elaborazione. Manca solo <strong>un ultimo passaggio</strong> per completarlo e far partire la spedizione.",
     "Lieliski — jūsu pasūtījums tiek apstrādāts. Atlicis tikai <strong>viens pēdējais solis</strong>, lai to pabeigtu un sāktu piegādi."),
    ("MiniSawX — motosega elettrica telescopica", "MiniSawX — elektriskais teleskopiskais zāģis"),
    ("Kit completo · Pagamento alla consegna", "Pilns komplekts · Pēcmaksa"),
    ("👇 Cosa devi fare adesso", "👇 Kas jādara tagad"),
    ("📞 Rispondi alla chiamata di conferma", "📞 Atbildiet uz apstiprinājuma zvanu"),
    ("Un nostro operatore ti contatterà <strong>nelle prossime ore</strong> per confermare il tuo ordine MiniSawX.",
     "Mūsu operators sazināsies <strong>nākamo stundu laikā</strong>, lai apstiprinātu jūsu MiniSawX pasūtījumu."),
    ("Se non rispondi alla chiamata, l'ordine verrà automaticamente annullato.",
     "Ja neatbildēsiet uz zvanu, pasūtījums tiks automātiski atcelts."),
    ("🕒 Orari di contatto", "🕒 Saziņas laiks"),
    ("Lunedì – Sabato · 9:00 – 18:00", "Pirmdiena – sestdiena · 9:00 – 18:00"),
    ("📋 Cosa succede dopo", "📋 Kas notiek tālāk"),
    ("Rispondi alla chiamata e <strong>conferma i tuoi dati</strong>", "Atbildiet uz zvanu un <strong>apstipriniet savus datus</strong>"),
    ("La tua MiniSawX verrà spedita entro <strong>24–48 ore</strong>", "Jūsu MiniSawX tiks nosūtīta <strong>24–48 stundu</strong> laikā"),
    ("Consegna a domicilio e <strong>pagamento alla consegna</strong>", "Piegāde mājās un <strong>pēcmaksa</strong>"),
    ("🔒 Pagamento alla consegna", "🔒 Pēcmaksa"),
    ("🛡️ Garanzia 2 anni", "🛡️ 2 gadu garantija"),
    ("↩️ 30 giorni di prova", "↩️ 30 dienu izmēģinājums"),
]

GR = [
    ("MiniSawX — Motosega elettrica telescopica | 59,00€", "MiniSawX — Ηλεκτρικό τηλεσκοπικό αλυσοπρίονο | 89,00€"),
    ("MiniSawX: taglia i rami a 5 metri e il legno fino a 35 cm, senza scala e senza benzina. 2 batterie 48 V. Pagamento alla consegna. Oggi 59,00€ invece di 196,00€.",
     "MiniSawX: κόβει κλαδιά στα 5 μέτρα και ξύλο έως 35 εκ., χωρίς σκάλα και χωρίς βενζίνη. 2 μπαταρίες 48 V. Αντικαταβολή. Σήμερα 89,00€ αντί για 297,00€."),
    ("SUBMITTING_LABEL: 'Invio...'", "SUBMITTING_LABEL: 'Αποστολή...'"),
    ("COOKIE_TEXT: 'Usiamo cookie tecnici e di terze parti per migliorare la tua esperienza e per analisi.'",
     "COOKIE_TEXT: 'Χρησιμοποιούμε τεχνικά cookies και cookies τρίτων για καλύτερη εμπειρία και ανάλυση.'"),
    ("COOKIE_ACCEPT: 'Accetta'", "COOKIE_ACCEPT: 'Αποδοχή'"),
    ("COOKIE_LEARN: 'Scopri di più'", "COOKIE_LEARN: 'Περισσότερα'"),
    ("✅ Pagamento alla consegna · Spedizione gratuita 24/48h", "✅ Αντικαταβολή · Δωρεάν αποστολή 24/48h"),
    ("Taglia i rami più alti e i tronchi più grossi senza scala.", "Κόψτε τα ψηλότερα κλαδιά και τους πιο χοντρούς κορμούς χωρίς σκάλα."),
    ("Senza benzina. Senza fatica. Fino a 5 metri.", "Χωρίς βενζίνη. Χωρίς κόπο. Έως 5 μέτρα."),
    ("MiniSawX: motosega elettrica telescopica. In pochi secondi passa dal modo manuale compatto all’asta. Taglia il legno fino a <b>35 cm</b> di diametro, arriva a <b>5 metri</b> e pesa solo <b>700 g</b>. Fatta per il giardino, gli alberi da frutto e lo spazio intorno a casa.",
     "MiniSawX: ηλεκτρικό τηλεσκοπικό αλυσοπρίονο. Σε λίγα δευτερόλεπτα περνά από τη συμπαγή χειροκίνητη λειτουργία στον στύλο. Κόβει ξύλο έως <b>35 εκ.</b> διάμετρο, φτάνει τα <b>5 μέτρα</b> και ζυγίζει μόνο <b>700 γρ.</b>. Φτιαγμένο για τον κήπο, τα καρποφόρα και τον χώρο γύρω από το σπίτι."),
    ("Kit completo MiniSawX", "Πλήρες κιτ MiniSawX"),
    ("🔥 Restano solo <strong>4 kit</strong> a questo prezzo", "🔥 Μένουν μόνο <strong>4 κιτ</strong> σε αυτή την τιμή"),
    ("<strong>3.000 W e asta telescopica fino a 5 metri.</strong>\n            Dove un decespugliatore normale si ferma, la MiniSawX continua. Attraversa legno verde o secco, rami grossi e tronchi fino a 35 cm.",
     "<strong>3.000 W και τηλεσκοπικός στύλος έως 5 μέτρα.</strong>\n            Όπου σταματά ένα κανονικό χορτοκοπτικό, το MiniSawX συνεχίζει. Διαπερνά πράσινο ή ξερό ξύλο, χοντρά κλαδιά και κορμούς έως 35 εκ."),
    ("<strong>2 batterie da 48 V e 8.000 mAh.</strong>\n            Una al lavoro, l’altra in carica in 45 min. Niente benzina, niente miscela, niente cavi tra i piedi.",
     "<strong>2 μπαταρίες 48 V και 8.000 mAh.</strong>\n            Η μία στη δουλειά, η άλλη φορτίζει σε 45 λεπτά. Χωρίς βενζίνη, χωρίς μείγμα, χωρίς καλώδια στα πόδια."),
    ("<strong>Pesa 700 g — la controlli con una mano.</strong>\n            Meno fatica su braccia, spalle e schiena, anche nei lavori più lunghi. Freno istantaneo.",
     "<strong>Ζυγίζει 700 γρ. — το ελέγχετε με ένα χέρι.</strong>\n            Λιγότερη κούραση σε χέρια, ώμους και πλάτη, ακόμα και στις μακρύτερες δουλειές. Άμεσο φρένο."),
    ("<strong>AutoChain X™ lubrifica e tende da sola.</strong>\n            Olio sempre al posto giusto, tensione corretta, zero pause per regolare la catena.",
     "<strong>Το AutoChain X™ λιπαίνει και τεντώνει μόνο του.</strong>\n            Λάδι πάντα στη σωστή θέση, σωστή τάση, μηδέν παύσεις για ρύθμιση της αλυσίδας."),
    ("<strong>4,9/5 — più di 8.730 giardini già sistemati.</strong>\n            Garanzia ufficiale 2 anni. 30 giorni per rese. Paghi solo quando arriva il corriere.",
     "<strong>4,9/5 — πάνω από 8.730 κήποι ήδη έτοιμοι.</strong>\n            Επίσημη εγγύηση 2 ετών. 30 ημέρες για επιστροφές. Πληρώνετε μόνο όταν έρθει ο διανομέας."),
    ("Sì, voglio la MiniSawX", "Ναι, θέλω το MiniSawX"),
    ("💵 Paghi alla consegna", "💵 Πληρώνετε στην παράδοση"),
    ("↩️ 30 giorni di prova", "↩️ 30 ημέρες δοκιμής"),
    ("🚚 Spedizione gratuita", "🚚 Δωρεάν αποστολή"),
    ("ACQUISTO SICURO • SPEDIZIONE GRATUITA • GARANZIA COMPLETA", "ΑΣΦΑΛΗΣ ΑΓΟΡΑ • ΔΩΡΕΑΝ ΑΠΟΣΤΟΛΗ • ΠΛΗΡΗΣ ΕΓΓΥΗΣΗ"),
    ("<strong>Spedizione gratuita</strong><br>\n        Consegna in tutta Italia, in 24–48 ore.",
     "<strong>Δωρεάν αποστολή</strong><br>\n        Παράδοση σε όλη την Ελλάδα, σε 24–48 ώρες."),
    ("<strong>Pagamento alla consegna</strong><br>\n        Niente carta e niente anticipo: paghi solo quando arriva il pacco",
     "<strong>Αντικαταβολή</strong><br>\n        Χωρίς κάρτα και χωρίς προκαταβολή: πληρώνετε μόνο όταν φτάσει το δέμα"),
    ("<strong>Acquisto protetto</strong><br>\n        I tuoi dati personali sono protetti al 100%",
     "<strong>Προστατευμένη αγορά</strong><br>\n        Τα προσωπικά σας δεδομένα προστατεύονται 100%"),
    ("<strong>Garanzia 2 anni</strong><br>\n        Puoi restituirlo senza pensieri entro 30 giorni",
     "<strong>Εγγύηση 2 ετών</strong><br>\n        Μπορείτε να το επιστρέψετε χωρίς άγχος εντός 30 ημερών"),
    ("Disponibilità in magazzino", "Διαθεσιμότητα στην αποθήκη"),
    ("RESTANO SOLO <span>4</span> KIT", "ΜΕΝΟΥΝ ΜΟΝΟ <span>4</span> ΚΙΤ"),
    ("Importante!", "Σημαντικό!"),
    ("Il magazzino si sta svuotando in fretta!", "Η αποθήκη αδειάζει γρήγορα!"),
    ("In questo momento tante altre persone stanno guardando la MiniSawX: per questo i kit disponibili scendono così in fretta.",
     "Αυτή τη στιγμή πολλοί άλλοι κοιτούν το MiniSawX: γι’ αυτό τα κιτ μειώνονται τόσο γρήγορα."),
    ("Ordina ora e assicurati uno degli ultimi kit al prezzo di oggi, con −70%.",
     "Παραγγείλτε τώρα και κλείστε ένα από τα τελευταία κιτ στην τιμή της ημέρας, με −70%."),
    ("Prenota la MiniSawX a soli 59 €", "Κλείστε το MiniSawX μόνο με 89 €"),
    ("Compila i tre campi. Ti chiamiamo entro 24 ore per confermare l’ordine e fissare la consegna. Paghi solo quando arriva il corriere.",
     "Συμπληρώστε τα τρία πεδία. Σας καλούμε εντός 24 ωρών για επιβεβαίωση της παραγγελίας και της παράδοσης. Πληρώνετε μόνο όταν έρθει ο διανομέας."),
    ("Nome e Cognome*", "Ονοματεπώνυμο*"),
    ('placeholder="Mario Rossi"', 'placeholder="Γιώργος Παπαδόπουλος"'),
    ("Telefono*", "Τηλέφωνο*"),
    ('placeholder="+39 392 0745623"', 'placeholder="+30 691 234 5678"'),
    ("Indirizzo di consegna*", "Διεύθυνση παράδοσης*"),
    ('placeholder="Via Torino 1, 12345 Roma Italia"', 'placeholder="Ερμού 15, 10563 Αθήνα"'),
    ("CONFERMA ORDINE", "ΕΠΙΒΕΒΑΙΩΣΗ ΠΑΡΑΓΓΕΛΙΑΣ"),
    ("🔒 Nessun anticipo · Niente carta · Paghi solo alla consegna", "🔒 Χωρίς προκαταβολή · Χωρίς κάρτα · Πληρώνετε μόνο στην παράδοση"),
    ("Scala instabile e motosega a benzina: il rischio di ogni potatura", "Ασταθής σκάλα και αλυσοπρίονο βενζίνης: ο κίνδυνος κάθε κλαδέματος"),
    ("Quante volte sei già salito su una scala instabile solo per tagliare un ramo?",
     "Πόσες φορές έχετε ήδη ανέβει σε ασταθή σκάλα μόνο για να κόψετε ένα κλαδί;"),
    ("Conosci la storia. La motosega a benzina fa un rumore assurdo, puzza di carburante e pesa 4 o 5 kg. Quella economica a batteria si blocca al primo tronco grosso. E per arrivare in cima all’albero da frutto… di nuovo la scala.",
     "Ξέρετε την ιστορία. Το βενζινοκίνητο αλυσοπρίονο κάνει απίστευτο θόρυβο, μυρίζει καύσιμο και ζυγίζει 4 ή 5 κιλά. Το φθηνό μπαταρίας κολλάει στον πρώτο χοντρό κορμό. Και για να φτάσετε στην κορυφή της οπωροφόρας… πάλι η σκάλα."),
    ("Allora ne compri un’altra. E il ciclo ricomincia.", "Τότε αγοράζετε άλλο. Και ο κύκλος ξαναρχίζει."),
    ("Nemmeno la versione a benzina ti salva: rumore, fumi, miscela, cavo di avviamento. Ogni potatura diventa una mattinata intera — e un rischio inutile in cima alla scala.",
     "Ούτε η έκδοση βενζίνης σας σώζει: θόρυβος, καπνοί, μείγμα, κορδόνι εκκίνησης. Κάθε κλάδεμα γίνεται ολόκληρο πρωινό — και άσκοπος κίνδυνος στην κορυφή της σκάλας."),
    ("Non è sfortuna.<br>\n          <strong>La verità è che la motosega tradizionale è nata per il suolo, non per la cima dell’albero — e quelle da pochi euro nascono per essere ricomprate.</strong>",
     "Δεν είναι κακή τύχη.<br>\n          <strong>Η αλήθεια είναι ότι το παραδοσιακό αλυσοπρίονο γεννήθηκε για το έδαφος, όχι για την κορυφή του δέντρου — και τα φθηνά μοντέλα γεννιούνται για να τα ξαναγοράζετε.</strong>"),
    ("Lubrificazione automatica della catena MiniSawX", "Αυτόματη λίπανση αλυσίδας MiniSawX"),
    ("La manutenzione che non devi più fare", "Η συντήρηση που δεν χρειάζεται πια"),
    ("AutoChain X™ cambia le regole della catena", "Το AutoChain X™ αλλάζει τους κανόνες της αλυσίδας"),
    ("Con una motosega tradizionale passi il tempo a lubrificare e a tendere la catena. Senza olio, si surriscalda. Senza tensione, salta o si blocca. E il taglio si ferma a metà ramo.",
     "Με παραδοσιακό αλυσοπρίονο περνάτε τον χρόνο λιπάνοντας και τεντώνοντας την αλυσίδα. Χωρίς λάδι, υπερθερμαίνεται. Χωρίς τάση, πετάγεται ή κολλάει. Και το κόψιμο σταματά στη μέση του κλαδιού."),
    ("<strong>AutoChain X™ lubrifica e tende da sola.</strong>\n            Il sistema distribuisce l’olio senza sosta e tiene la tensione giusta. Le prestazioni restano stabili dal primo all’ultimo taglio.",
     "<strong>Το AutoChain X™ λιπαίνει και τεντώνει μόνο του.</strong>\n            Το σύστημα διανέμει το λάδι χωρίς παύση και κρατά τη σωστή τάση. Η απόδοση μένει σταθερή από το πρώτο ως το τελευταίο κόψιμο."),
    ("<strong>È esattamente il sistema montato sulla MiniSawX.</strong>\n            Per questo continui a tagliare senza pause e senza regolazioni ogni dieci minuti.",
     "<strong>Ακριβώς αυτό το σύστημα είναι τοποθετημένο στο MiniSawX.</strong>\n            Γι’ αυτό συνεχίζετε να κόβετε χωρίς παύσεις και χωρίς ρυθμίσεις κάθε δέκα λεπτά."),
    ("È lo stesso ragionamento che separa un attrezzo che chiede attenzione continua da uno che semplicemente lavora: meno regolazioni, più taglio, meno manutenzione.",
     "Είναι η ίδια λογική που χωρίζει ένα εργαλείο που ζητά συνεχή προσοχή από ένα που απλώς δουλεύει: λιγότερες ρυθμίσεις, περισσότερο κόψιμο, λιγότερη συντήρηση."),
    ("Qui non è pubblicità. <b>È il sistema che fa il lavoro.</b>", "Εδώ δεν είναι διαφήμιση. <b>Είναι το σύστημα που κάνει τη δουλειά.</b>"),
    ("✅ I vantaggi concreti", "✅ Τα συγκεκριμένα πλεονεκτήματα"),
    ("Questa è la motosega che ti toglie la scala dal giardino", "Αυτό είναι το αλυσοπρίονο που βγάζει τη σκάλα από τον κήπο"),
    ("Più potenza sui rami grossi, zero benzina, meno peso sulle braccia. E il giardino torna in ordine in un solo giorno.",
     "Περισσότερη ισχύς στα χοντρά κλαδιά, μηδέν βενζίνη, λιγότερο βάρος στα χέρια. Και ο κήπος τακτοποιείται σε μία μέρα."),
    ("MiniSawX con asta telescopica fino a 5 metri", "MiniSawX με τηλεσκοπικό στύλο έως 5 μέτρα"),
    ("3.000 W e 5 metri — la cima dell’albero smette di essere un problema", "3.000 W και 5 μέτρα — η κορυφή του δέντρου παύει να είναι πρόβλημα"),
    ("Dove un decespugliatore normale si ferma, la MiniSawX continua. La lama attraversa legno verde e secco, rami grossi e tronchi fino a 35 cm. Vicino al suolo usi il modo manuale compatto. In cima, monti l’asta telescopica.",
     "Όπου σταματά ένα κανονικό χορτοκοπτικό, το MiniSawX συνεχίζει. Η λεπίδα διαπερνά πράσινο και ξερό ξύλο, χοντρά κλαδιά και κορμούς έως 35 εκ. Κοντά στο έδαφος χρησιμοποιείτε τη συμπαγή χειροκίνητη λειτουργία. Στην κορυφή, τοποθετείτε τον τηλεσκοπικό στύλο."),
    ("Taglio da 35 cm. Potenza da 3.000 W. Altezza fino a 5 metri.", "Κοπή 35 εκ. Ισχύς 3.000 W. Ύψος έως 5 μέτρα."),
    ("I lavori più pesanti stanno in un solo giorno.", "Οι πιο βαριές δουλειές χωράνε σε μία μέρα."),
    ("MiniSawX a batteria che taglia un tronco senza cavi", "MiniSawX μπαταρίας που κόβει κορμό χωρίς καλώδια"),
    ("Due batterie da 48 V. Senza benzina e senza cavi", "Δύο μπαταρίες 48 V. Χωρίς βενζίνη και χωρίς καλώδια"),
    ("Dimentica benzina, miscela e prolunghe che limitano i movimenti e si avvolgono ai piedi. Quando una batteria finisce, metti la seconda e vai avanti. Ricarica in 45 minuti.",
     "Ξεχάστε βενζίνη, μείγμα και προεκτάσεις που περιορίζουν τις κινήσεις και τυλίγονται στα πόδια. Όταν τελειώνει η μία μπαταρία, βάζετε τη δεύτερη και συνεχίζετε. Φόρτιση σε 45 λεπτά."),
    ("48 V · 8.000 mAh · senza fili · carica in 45 min.", "48 V · 8.000 mAh · ασύρματο · φόρτιση σε 45 λεπτά."),
    ("Ti muovi in tutta la proprietà senza dipendere da una presa.", "Κινείστε σε όλο το οικόπεδο χωρίς να εξαρτάστε από πρίζα."),
    ("MiniSawX in una mano: 700 g, 48 V", "MiniSawX σε ένα χέρι: 700 γρ., 48 V"),
    ("700 g. La controlli con una mano, senza distruggerti la schiena", "700 γρ. Το ελέγχετε με ένα χέρι, χωρίς να καταστρέφετε την πλάτη"),
    ("Una motosega tradizionale pesa 4–5 kg. La MiniSawX pesa 700 g e riduce la fatica di braccia, spalle e schiena, anche nei lavori più lunghi. Il corpo compatto entra negli spazi stretti. Freno istantaneo.",
     "Ένα παραδοσιακό αλυσοπρίονο ζυγίζει 4–5 κιλά. Το MiniSawX ζυγίζει 700 γρ. και μειώνει την κούραση σε χέρια, ώμους και πλάτη, ακόμα και στις μακρύτερες δουλειές. Το συμπαγές σώμα μπαίνει σε στενούς χώρους. Άμεσο φρένο."),
    ("700 g · una mano · freno istantaneo.", "700 γρ. · ένα χέρι · άμεσο φρένο."),
    ("Tagli con precisione dove l’attrezzo pesante non arriva nemmeno.", "Κόβετε με ακρίβεια εκεί που το βαρύ εργαλείο δεν φτάνει καν."),
    ("Sì, voglio la MiniSawX ↓", "Ναι, θέλω το MiniSawX ↓"),
    ("💵 Paghi quando arriva", "💵 Πληρώνετε όταν φτάσει"),
    ("🚚 Consegna in 24/48h", "🚚 Παράδοση σε 24/48h"),
    ("↩️ Provalo 30 giorni", "↩️ Δοκιμάστε το 30 ημέρες"),
    ("Confronto senza filtri", "Σύγκριση χωρίς φίλτρα"),
    ("Motosega tradizionale o MiniSawX?", "Παραδοσιακό αλυσοπρίονο ή MiniSawX;"),
    ("Gli stessi criteri. Senza fronzoli.", "Τα ίδια κριτήρια. Χωρίς στολίδια."),
    ("Tradizionale", "Παραδοσιακό"),
    ("⛽ Benzina, rumore e fumi", "⛽ Βενζίνη, θόρυβος και καπνοί"),
    ("Batteria, senza benzina", "Μπαταρία, χωρίς βενζίνη"),
    ("Solo 700 g", "Μόνο 700 γρ."),
    ("🪜 Ti serve una scala", "🪜 Χρειάζεστε σκάλα"),
    ("Asta fino a 5 metri", "Στύλος έως 5 μέτρα"),
    ("🔧 Regolazioni continue", "🔧 Συνεχείς ρυθμίσεις"),
    ("🛢️ Rifornimento di benzina", "🛢️ Ανεφοδιασμός βενζίνης"),
    ("Due batterie da 48 V", "Δύο μπαταρίες 48 V"),
    ("⭐ Più di 8.730 giardini", "⭐ Πάνω από 8.730 κήποι"),
    ("Chi la prova non la molla più", "Όποιος το δοκιμάσει δεν το αφήνει"),
    ("C’è chi lascia la benzina e chi ha già bruciato soldi su versioni economiche: è questo che li porta a scegliere la MiniSawX.",
     "Άλλοι αφήνουν τη βενζίνη και άλλοι έχουν ήδη κάψει χρήματα σε φθηνές εκδόσεις: γι’ αυτό επιλέγουν το MiniSawX."),
    ("Roberto G. — MiniSawX in uso", "Roberto G. — MiniSawX σε χρήση"),
    ("“La catena attraversa in fretta anche i rami secchi più grossi, senza fatica e senza bloccarsi. Pensavo di dover usare molta più forza, invece basta guidarla con una mano.”",
     "«Η αλυσίδα περνά γρήγορα ακόμα και τα πιο χοντρά ξερά κλαδιά, χωρίς κόπο και χωρίς να κολλάει. Νόμιζα ότι θα χρειαζόμουν πολύ περισσότερη δύναμη, αλλά αρκεί να το οδηγώ με ένα χέρι.»"),
    ("✅ Una potenza sorprendente", "✅ Εκπληκτική ισχύς"),
    ("David M. — MiniSawX in mano", "David M. — MiniSawX στο χέρι"),
    ("“È potente, comoda da tenere in mano e facile da usare, anche per chi non aveva mai preso una motosega. In un pomeriggio ho potato tutti gli alberi da frutto del giardino.”",
     "«Είναι ισχυρό, άνετο στο χέρι και εύκολο στη χρήση, ακόμα και για όποιον δεν είχε πιάσει ποτέ αλυσοπρίονο. Σε ένα απόγευμα κλάδεψα όλα τα καρποφόρα του κήπου.»"),
    ("✅ Fa il suo lavoro", "✅ Κάνει τη δουλειά του"),
    ("Miguel T. — MiniSawX con asta telescopica", "Miguel T. — MiniSawX με τηλεσκοπικό στύλο"),
    ("“L’asta telescopica arriva senza fatica ai rami più alti, quindi non devo più salire su una scala instabile. Ho finito in metà tempo e mi sono sentito molto più sicuro.”",
     "«Ο τηλεσκοπικός στύλος φτάνει χωρίς κόπο στα ψηλότερα κλαδιά, οπότε δεν χρειάζεται πια να ανεβαίνω σε ασταθή σκάλα. Τελείωσα στον μισό χρόνο και ένιωσα πολύ πιο ασφαλής.»"),
    ("✅ Più veloce e più sicura", "✅ Πιο γρήγορο και πιο ασφαλές"),
    ("📦 Tutto incluso", "📦 Όλα συμπεριλαμβάνονται"),
    ("Kit completo MiniSawX.<br>\n        Niente extra. Niente sorprese.", "Πλήρες κιτ MiniSawX.<br>\n        Χωρίς έξτρα. Χωρίς εκπλήξεις."),
    ("Apri la scatola, monti e inizi a tagliare. Non manca niente.", "Ανοίγετε το κουτί, συναρμολογείτε και αρχίζετε να κόβετε. Δεν λείπει τίποτα."),
    ("Kit completo MiniSawX — tutto quello che c’è nel pacco", "Πλήρες κιτ MiniSawX — ό,τι υπάρχει στο δέμα"),
    ("Cosa c’è nella scatola", "Τι έχει στο κουτί"),
    ("A cosa serve davvero", "Σε τι χρησιμεύει πραγματικά"),
    ("⚙️ Motosega elettrica MiniSawX", "⚙️ Ηλεκτρικό αλυσοπρίονο MiniSawX"),
    ("3.000 W in modalità compatta — il cuore del kit", "3.000 W σε συμπαγή λειτουργία — η καρδιά του κιτ"),
    ("🪜 Asta telescopica fino a 5 metri", "🪜 Τηλεσκοπικός στύλος έως 5 μέτρα"),
    ("Arrivi in cima all’albero senza scala", "Φτάνετε στην κορυφή του δέντρου χωρίς σκάλα"),
    ("🔋 2 batterie da 48 V e 8.000 mAh", "🔋 2 μπαταρίες 48 V και 8.000 mAh"),
    ("Una al lavoro, l’altra in carica — non ti fermi", "Η μία στη δουλειά, η άλλη στη φόρτιση — δεν σταματάτε"),
    ("⚡ Caricabatterie rapido", "⚡ Ταχυφορτιστής"),
    ("45 minuti e torni a tagliare", "45 λεπτά και ξανακόβετε"),
    ("⛓️ 2 catene di ricambio", "⛓️ 2 ανταλλακτικές αλυσίδες"),
    ("Non resti a metà ramo senza catena", "Δεν μένετε στη μέση του κλαδιού χωρίς αλυσίδα"),
    ("🛢️ Serbatoio olio + AutoChain X™", "🛢️ Δοχείο λαδιού + AutoChain X™"),
    ("Lubrifica e tende da sola — manutenzione minima", "Λιπαίνει και τεντώνει μόνο του — ελάχιστη συντήρηση"),
    ("🧰 Set di attrezzi e valigetta", "🧰 Σετ εργαλείων και βαλιτσάκι"),
    ("Tutto al suo posto, pronto da riporre", "Όλα στη θέση τους, έτοιμα για φύλαξη"),
    ("🛡️ Garanzia ufficiale 2 anni", "🛡️ Επίσημη εγγύηση 2 ετών"),
    ("Assistenza inclusa — 30 giorni per il reso", "Υποστήριξη περιλαμβάνεται — 30 ημέρες για επιστροφή"),
    ("❓ Le domande più frequenti", "❓ Οι συχνότερες ερωτήσεις"),
    ("Qualche dubbio? È normale.<br>\n        Lo chiarisco tutto qui.", "Κάποια απορία; Είναι φυσιολογικό.<br>\n        Τα ξεκαθαρίζω όλα εδώ."),
    ("Prima di ordinare, le risposte alle domande di sempre: consegna, pagamento, benzina, rami alti e reso.",
     "Πριν παραγγείλετε, οι απαντήσεις στις γνωστές ερωτήσεις: παράδοση, πληρωμή, βενζίνη, ψηλά κλαδιά και επιστροφή."),
    ("Quando arriva l’ordine?", "Πότε φτάνει η παραγγελία;"),
    ("La consegna richiede circa 1–2 giorni lavorativi. Spedizione gratuita in tutta Italia.",
     "Η παράδοση χρειάζεται περίπου 1–2 εργάσιμες ημέρες. Δωρεάν αποστολή σε όλη την Ελλάδα."),
    ("Devo pagare in anticipo?", "Πρέπει να πληρώσω προκαταβολή;"),
    ("No. Paghi direttamente al corriere al momento della consegna. Niente carta. Niente anticipo.",
     "Όχι. Πληρώνετε απευθείας στον διανομέα τη στιγμή της παράδοσης. Χωρίς κάρτα. Χωρίς προκαταβολή."),
    ("Serve la benzina?", "Χρειάζεται βενζίνη;"),
    ("No. La MiniSawX funziona solo a batteria: due da 48 V e 8.000 mAh. Niente miscela, niente fumi, niente cavo di avviamento.",
     "Όχι. Το MiniSawX λειτουργεί μόνο με μπαταρία: δύο των 48 V και 8.000 mAh. Χωρίς μείγμα, χωρίς καπνούς, χωρίς κορδόνι εκκίνησης."),
    ("Riesco a tagliare i rami alti senza scala?", "Μπορώ να κόψω τα ψηλά κλαδιά χωρίς σκάλα;"),
    ("Sì. L’asta telescopica arriva fino a 5 metri. Vicino al suolo usi il modo manuale compatto. In cima all’albero, monti l’asta.",
     "Ναι. Ο τηλεσκοπικός στύλος φτάνει τα 5 μέτρα. Κοντά στο έδαφος χρησιμοποιείτε τη συμπαγή χειροκίνητη λειτουργία. Στην κορυφή του δέντρου, τοποθετείτε τον στύλο."),
    ("E se poi non mi convince?", "Κι αν τελικά δεν με πείθει;"),
    ("Hai 30 giorni per chiedere il reso, secondo le condizioni di rimborso. Non rischi niente.",
     "Έχετε 30 ημέρες για να ζητήσετε επιστροφή, σύμφωνα με τους όρους επιστροφής χρημάτων. Δεν ρισκάρετε τίποτα."),
    ("✅ Paghi quando arriva", "✅ Πληρώνετε όταν φτάσει"),
    ("INSERISCI I DATI DI CONSEGNA", "ΣΥΜΠΛΗΡΩΣΤΕ ΤΑ ΣΤΟΙΧΕΙΑ ΠΑΡΑΔΟΣΗΣ"),
    ("L’ordine parte subito. Paghi solo alla consegna, direttamente al corriere.",
     "Η παραγγελία ξεκινά αμέσως. Πληρώνετε μόνο στην παράδοση, απευθείας στον διανομέα."),
]

GR_TY = [
    ("Ordine ricevuto — Attendi la chiamata di conferma | MiniSawX", "Παραγγελία ελήφθη — Περιμένετε την κλήση επιβεβαίωσης | MiniSawX"),
    ("Il tuo ordine MiniSawX è stato registrato. Manca solo un ultimo passaggio: rispondi alla chiamata di conferma del nostro operatore.",
     "Η παραγγελία MiniSawX καταχωρήθηκε. Μένει μόνο ένα τελευταίο βήμα: απαντήστε στην κλήση επιβεβαίωσης του χειριστή μας."),
    ("Il tuo ordine MiniSawX è stato registrato!", "Η παραγγελία MiniSawX καταχωρήθηκε!"),
    ("Perfetto — il tuo ordine è in elaborazione. Manca solo <strong>un ultimo passaggio</strong> per completarlo e far partire la spedizione.",
     "Τέλεια — η παραγγελία σας επεξεργάζεται. Μένει μόνο <strong>ένα τελευταίο βήμα</strong> για να ολοκληρωθεί και να ξεκινήσει η αποστολή."),
    ("MiniSawX — motosega elettrica telescopica", "MiniSawX — ηλεκτρικό τηλεσκοπικό αλυσοπρίονο"),
    ("Kit completo · Pagamento alla consegna", "Πλήρες κιτ · Αντικαταβολή"),
    ("👇 Cosa devi fare adesso", "👇 Τι πρέπει να κάνετε τώρα"),
    ("📞 Rispondi alla chiamata di conferma", "📞 Απαντήστε στην κλήση επιβεβαίωσης"),
    ("Un nostro operatore ti contatterà <strong>nelle prossime ore</strong> per confermare il tuo ordine MiniSawX.",
     "Ένας χειριστής μας θα σας καλέσει <strong>τις επόμενες ώρες</strong> για να επιβεβαιώσει την παραγγελία MiniSawX."),
    ("Se non rispondi alla chiamata, l'ordine verrà automaticamente annullato.",
     "Αν δεν απαντήσετε στην κλήση, η παραγγελία ακυρώνεται αυτόματα."),
    ("🕒 Orari di contatto", "🕒 Ώρες επικοινωνίας"),
    ("Lunedì – Sabato · 9:00 – 18:00", "Δευτέρα – Σάββατο · 9:00 – 18:00"),
    ("📋 Cosa succede dopo", "📋 Τι γίνεται μετά"),
    ("Rispondi alla chiamata e <strong>conferma i tuoi dati</strong>", "Απαντήστε στην κλήση και <strong>επιβεβαιώστε τα στοιχεία σας</strong>"),
    ("La tua MiniSawX verrà spedita entro <strong>24–48 ore</strong>", "Το MiniSawX θα αποσταλεί εντός <strong>24–48 ωρών</strong>"),
    ("Consegna a domicilio e <strong>pagamento alla consegna</strong>", "Παράδοση κατ’ οίκον και <strong>αντικαταβολή</strong>"),
    ("🔒 Pagamento alla consegna", "🔒 Αντικαταβολή"),
    ("🛡️ Garanzia 2 anni", "🛡️ Εγγύηση 2 ετών"),
    ("↩️ 30 giorni di prova", "↩️ 30 ημέρες δοκιμής"),
]

BG = [
    ("MiniSawX — Motosega elettrica telescopica | 59,00€", "MiniSawX — Електрически телескопичен верижен трион | 89,00€"),
    ("MiniSawX: taglia i rami a 5 metri e il legno fino a 35 cm, senza scala e senza benzina. 2 batterie 48 V. Pagamento alla consegna. Oggi 59,00€ invece di 196,00€.",
     "MiniSawX: реже клони на 5 метра и дърво до 35 см, без стълба и без бензин. 2 батерии 48 V. Наложен платеж. Днес 89,00€ вместо 297,00€."),
    ("SUBMITTING_LABEL: 'Invio...'", "SUBMITTING_LABEL: 'Изпращане...'"),
    ("COOKIE_TEXT: 'Usiamo cookie tecnici e di terze parti per migliorare la tua esperienza e per analisi.'",
     "COOKIE_TEXT: 'Използваме технически бисквитки и бисквитки на трети страни, за да подобрим вашето изживяване и за анализ.'"),
    ("COOKIE_ACCEPT: 'Accetta'", "COOKIE_ACCEPT: 'Приемам'"),
    ("COOKIE_LEARN: 'Scopri di più'", "COOKIE_LEARN: 'Научете повече'"),
    ("✅ Pagamento alla consegna · Spedizione gratuita 24/48h", "✅ Наложен платеж · Безплатна доставка 24/48h"),
    ("Taglia i rami più alti e i tronchi più grossi senza scala.", "Отрежете най-високите клони и най-дебелите стволове без стълба."),
    ("Senza benzina. Senza fatica. Fino a 5 metri.", "Без бензин. Без усилие. До 5 метра."),
    ("MiniSawX: motosega elettrica telescopica. In pochi secondi passa dal modo manuale compatto all’asta. Taglia il legno fino a <b>35 cm</b> di diametro, arriva a <b>5 metri</b> e pesa solo <b>700 g</b>. Fatta per il giardino, gli alberi da frutto e lo spazio intorno a casa.",
     "MiniSawX: електрически телескопичен верижен трион. За секунди преминава от компактен ръчен режим към щангата. Реже дърво до <b>35 см</b> диаметър, достига <b>5 метра</b> и тежи само <b>700 г</b>. Направен за градината, овошките и двора."),
    ("Kit completo MiniSawX", "Пълен комплект MiniSawX"),
    ("🔥 Restano solo <strong>4 kit</strong> a questo prezzo", "🔥 Остават само <strong>4 комплекта</strong> на тази цена"),
    ("<strong>3.000 W e asta telescopica fino a 5 metri.</strong>\n            Dove un decespugliatore normale si ferma, la MiniSawX continua. Attraversa legno verde o secco, rami grossi e tronchi fino a 35 cm.",
     "<strong>3 000 W и телескопична щанга до 5 метра.</strong>\n            Където обикновеният тример спира, MiniSawX продължава. Преминава през зелено или сухо дърво, дебели клони и стволове до 35 см."),
    ("<strong>2 batterie da 48 V e 8.000 mAh.</strong>\n            Una al lavoro, l’altra in carica in 45 min. Niente benzina, niente miscela, niente cavi tra i piedi.",
     "<strong>2 батерии 48 V и 8 000 mAh.</strong>\n            Едната работи, другата се зарежда за 45 мин. Без бензин, без смес, без кабели под краката."),
    ("<strong>Pesa 700 g — la controlli con una mano.</strong>\n            Meno fatica su braccia, spalle e schiena, anche nei lavori più lunghi. Freno istantaneo.",
     "<strong>Тежи 700 г — управлявате го с една ръка.</strong>\n            По-малко натоварване за ръце, рамене и гръб, дори при по-дълга работа. Моментална спирачка."),
    ("<strong>AutoChain X™ lubrifica e tende da sola.</strong>\n            Olio sempre al posto giusto, tensione corretta, zero pause per regolare la catena.",
     "<strong>AutoChain X™ смазва и обтяга сам.</strong>\n            Маслото винаги е на правилното място, правилно натягане, нула паузи за веригата."),
    ("<strong>4,9/5 — più di 8.730 giardini già sistemati.</strong>\n            Garanzia ufficiale 2 anni. 30 giorni per rese. Paghi solo quando arriva il corriere.",
     "<strong>4,9/5 — над 8 730 вече подредени градини.</strong>\n            Официална 2-годишна гаранция. 30 дни за връщане. Плащате само когато куриерът пристигне."),
    ("Sì, voglio la MiniSawX", "Да, искам MiniSawX"),
    ("💵 Paghi alla consegna", "💵 Плащате при доставка"),
    ("↩️ 30 giorni di prova", "↩️ 30 дни проба"),
    ("🚚 Spedizione gratuita", "🚚 Безплатна доставка"),
    ("ACQUISTO SICURO • SPEDIZIONE GRATUITA • GARANZIA COMPLETA", "СИГУРНА ПОКУПКА • БЕЗПЛАТНА ДОСТАВКА • ПЪЛНА ГАРАНЦИЯ"),
    ("<strong>Spedizione gratuita</strong><br>\n        Consegna in tutta Italia, in 24–48 ore.",
     "<strong>Безплатна доставка</strong><br>\n        Доставка в цяла България, за 24–48 часа."),
    ("<strong>Pagamento alla consegna</strong><br>\n        Niente carta e niente anticipo: paghi solo quando arriva il pacco",
     "<strong>Наложен платеж</strong><br>\n        Без карта и без аванс: плащате само когато пратката пристигне"),
    ("<strong>Acquisto protetto</strong><br>\n        I tuoi dati personali sono protetti al 100%",
     "<strong>Защитена покупка</strong><br>\n        Личните ви данни са защитени 100%"),
    ("<strong>Garanzia 2 anni</strong><br>\n        Puoi restituirlo senza pensieri entro 30 giorni",
     "<strong>Гаранция 2 години</strong><br>\n        Можете да го върнете без притеснение в рамките на 30 дни"),
    ("Disponibilità in magazzino", "Наличност в склада"),
    ("RESTANO SOLO <span>4</span> KIT", "ОСТАВАТ САМО <span>4</span> КОМПЛЕКТА"),
    ("Importante!", "Важно!"),
    ("Il magazzino si sta svuotando in fretta!", "Складът се изпразва бързо!"),
    ("In questo momento tante altre persone stanno guardando la MiniSawX: per questo i kit disponibili scendono così in fretta.",
     "В момента много други хора гледат MiniSawX: затова комплектите намаляват толкова бързо."),
    ("Ordina ora e assicurati uno degli ultimi kit al prezzo di oggi, con −70%.",
     "Поръчайте сега и си осигурете един от последните комплекти на днешната цена, с −70%."),
    ("Prenota la MiniSawX a soli 59 €", "Резервирайте MiniSawX само за 89 €"),
    ("Compila i tre campi. Ti chiamiamo entro 24 ore per confermare l’ordine e fissare la consegna. Paghi solo quando arriva il corriere.",
     "Попълнете трите полета. Ще ви се обадим до 24 часа, за да потвърдим поръчката и доставката. Плащате само когато куриерът пристигне."),
    ("Nome e Cognome*", "Име и фамилия*"),
    ('placeholder="Mario Rossi"', 'placeholder="Иван Иванов"'),
    ("Telefono*", "Телефон*"),
    ('placeholder="+39 392 0745623"', 'placeholder="+359 88 123 4567"'),
    ("Indirizzo di consegna*", "Адрес за доставка*"),
    ('placeholder="Via Torino 1, 12345 Roma Italia"', 'placeholder="бул. Витоша 1, 1000 София"'),
    ("CONFERMA ORDINE", "ПОТВЪРДИ ПОРЪЧКАТА"),
    ("🔒 Nessun anticipo · Niente carta · Paghi solo alla consegna", "🔒 Без аванс · Без карта · Плащате само при доставка"),
    ("Scala instabile e motosega a benzina: il rischio di ogni potatura", "Нестабилна стълба и бензинов трион: рискът при всяка резитба"),
    ("Quante volte sei già salito su una scala instabile solo per tagliare un ramo?",
     "Колко пъти вече сте се качвали на нестабилна стълба само за да отрежете един клон?"),
    ("Conosci la storia. La motosega a benzina fa un rumore assurdo, puzza di carburante e pesa 4 o 5 kg. Quella economica a batteria si blocca al primo tronco grosso. E per arrivare in cima all’albero da frutto… di nuovo la scala.",
     "Познавате историята. Бензиновият трион вдига невъзможен шум, мирише на гориво и тежи 4–5 кг. Евтиният акумулаторен засяда още при първия дебел ствол. А за да стигнете върха на овошката… пак стълбата."),
    ("Allora ne compri un’altra. E il ciclo ricomincia.", "Тогава купувате още една. И цикълът започва отново."),
    ("Nemmeno la versione a benzina ti salva: rumore, fumi, miscela, cavo di avviamento. Ogni potatura diventa una mattinata intera — e un rischio inutile in cima alla scala.",
     "Дори бензиновата версия не спасява: шум, изпарения, смес, стартово въже. Всяка резитба става цяла сутрин — и излишен риск на върха на стълбата."),
    ("Non è sfortuna.<br>\n          <strong>La verità è che la motosega tradizionale è nata per il suolo, non per la cima dell’albero — e quelle da pochi euro nascono per essere ricomprate.</strong>",
     "Не е лош късмет.<br>\n          <strong>Истината е, че традиционният трион е създаден за земята, не за върха на дървото — а евтините модели са създадени, за да ги купувате отново.</strong>"),
    ("Lubrificazione automatica della catena MiniSawX", "Автоматично смазване на веригата MiniSawX"),
    ("La manutenzione che non devi più fare", "Поддръжката, която вече не правите"),
    ("AutoChain X™ cambia le regole della catena", "AutoChain X™ променя правилата на веригата"),
    ("Con una motosega tradizionale passi il tempo a lubrificare e a tendere la catena. Senza olio, si surriscalda. Senza tensione, salta o si blocca. E il taglio si ferma a metà ramo.",
     "С традиционен трион губите време да смазвате и обтягате веригата. Без масло прегрява. Без натягане изскача или засяда. И рязането спира по средата на клона."),
    ("<strong>AutoChain X™ lubrifica e tende da sola.</strong>\n            Il sistema distribuisce l’olio senza sosta e tiene la tensione giusta. Le prestazioni restano stabili dal primo all’ultimo taglio.",
     "<strong>AutoChain X™ смазва и обтяга сам.</strong>\n            Системата разпределя маслото без прекъсване и държи правилното натягане. Производителността остава стабилна от първия до последния разрез."),
    ("<strong>È esattamente il sistema montato sulla MiniSawX.</strong>\n            Per questo continui a tagliare senza pause e senza regolazioni ogni dieci minuti.",
     "<strong>Точно тази система е вградена в MiniSawX.</strong>\n            Затова продължавате да режете без паузи и без настройки на всеки десет минути."),
    ("È lo stesso ragionamento che separa un attrezzo che chiede attenzione continua da uno che semplicemente lavora: meno regolazioni, più taglio, meno manutenzione.",
     "Същият принцип разделя инструмент, който иска постоянно внимание, от такъв, който просто работи: по-малко настройки, повече рязане, по-малко поддръжка."),
    ("Qui non è pubblicità. <b>È il sistema che fa il lavoro.</b>", "Тук това не е реклама. <b>Това е системата, която върши работата.</b>"),
    ("✅ I vantaggi concreti", "✅ Конкретните предимства"),
    ("Questa è la motosega che ti toglie la scala dal giardino", "Това е трионът, който маха стълбата от градината"),
    ("Più potenza sui rami grossi, zero benzina, meno peso sulle braccia. E il giardino torna in ordine in un solo giorno.",
     "Повече мощност за дебели клони, нула бензин, по-малко тегло за ръцете. И градината е подредена за един ден."),
    ("MiniSawX con asta telescopica fino a 5 metri", "MiniSawX с телескопична щанга до 5 метра"),
    ("3.000 W e 5 metri — la cima dell’albero smette di essere un problema", "3 000 W и 5 метра — върхът на дървото вече не е проблем"),
    ("Dove un decespugliatore normale si ferma, la MiniSawX continua. La lama attraversa legno verde e secco, rami grossi e tronchi fino a 35 cm. Vicino al suolo usi il modo manuale compatto. In cima, monti l’asta telescopica.",
     "Където обикновеният тример спира, MiniSawX продължава. Острието минава през зелено и сухо дърво, дебели клони и стволове до 35 см. Близо до земята ползвате компактния ръчен режим. На върха слагате телескопичната щанга."),
    ("Taglio da 35 cm. Potenza da 3.000 W. Altezza fino a 5 metri.", "Рязане 35 см. Мощност 3 000 W. Височина до 5 метра."),
    ("I lavori più pesanti stanno in un solo giorno.", "Най-тежката работа се събира в един ден."),
    ("MiniSawX a batteria che taglia un tronco senza cavi", "MiniSawX на батерия, който реже ствол без кабели"),
    ("Due batterie da 48 V. Senza benzina e senza cavi", "Две батерии 48 V. Без бензин и без кабели"),
    ("Dimentica benzina, miscela e prolunghe che limitano i movimenti e si avvolgono ai piedi. Quando una batteria finisce, metti la seconda e vai avanti. Ricarica in 45 minuti.",
     "Забравете бензин, смес и удължители, които ограничават движенията и се мотаят в краката. Когато едната батерия свърши, слагате втората и продължавате. Зареждане за 45 минути."),
    ("48 V · 8.000 mAh · senza fili · carica in 45 min.", "48 V · 8 000 mAh · без кабели · зареждане за 45 мин."),
    ("Ti muovi in tutta la proprietà senza dipendere da una presa.", "Движите се из целия имот, без да зависите от контакт."),
    ("MiniSawX in una mano: 700 g, 48 V", "MiniSawX в една ръка: 700 г, 48 V"),
    ("700 g. La controlli con una mano, senza distruggerti la schiena", "700 г. Управлявате го с една ръка, без да съсипвате гърба"),
    ("Una motosega tradizionale pesa 4–5 kg. La MiniSawX pesa 700 g e riduce la fatica di braccia, spalle e schiena, anche nei lavori più lunghi. Il corpo compatto entra negli spazi stretti. Freno istantaneo.",
     "Традиционният трион тежи 4–5 кг. MiniSawX тежи 700 г и намалява натоварването на ръце, рамене и гръб, дори при по-дълга работа. Компактното тяло влиза в тесни места. Моментална спирачка."),
    ("700 g · una mano · freno istantaneo.", "700 г · една ръка · моментална спирачка."),
    ("Tagli con precisione dove l’attrezzo pesante non arriva nemmeno.", "Режете прецизно там, където тежкият инструмент дори не стига."),
    ("Sì, voglio la MiniSawX ↓", "Да, искам MiniSawX ↓"),
    ("💵 Paghi quando arriva", "💵 Плащате, когато пристигне"),
    ("🚚 Consegna in 24/48h", "🚚 Доставка за 24/48h"),
    ("↩️ Provalo 30 giorni", "↩️ Изпробвайте 30 дни"),
    ("Confronto senza filtri", "Сравнение без филтри"),
    ("Motosega tradizionale o MiniSawX?", "Традиционен трион или MiniSawX?"),
    ("Gli stessi criteri. Senza fronzoli.", "Същите критерии. Без излишни думи."),
    ("Tradizionale", "Традиционен"),
    ("⛽ Benzina, rumore e fumi", "⛽ Бензин, шум и изпарения"),
    ("Batteria, senza benzina", "Батерия, без бензин"),
    ("Solo 700 g", "Само 700 г"),
    ("🪜 Ti serve una scala", "🪜 Трябва ви стълба"),
    ("Asta fino a 5 metri", "Щанга до 5 метра"),
    ("🔧 Regolazioni continue", "🔧 Постоянни настройки"),
    ("🛢️ Rifornimento di benzina", "🛢️ Зареждане с бензин"),
    ("Due batterie da 48 V", "Две батерии 48 V"),
    ("⭐ Più di 8.730 giardini", "⭐ Над 8 730 градини"),
    ("Chi la prova non la molla più", "Който го пробва, вече не го пуска"),
    ("C’è chi lascia la benzina e chi ha già bruciato soldi su versioni economiche: è questo che li porta a scegliere la MiniSawX.",
     "Някои оставят бензина, други вече са изгорили пари за евтини версии: затова избират MiniSawX."),
    ("Roberto G. — MiniSawX in uso", "Roberto G. — MiniSawX в употреба"),
    ("“La catena attraversa in fretta anche i rami secchi più grossi, senza fatica e senza bloccarsi. Pensavo di dover usare molta più forza, invece basta guidarla con una mano.”",
     "„Веригата минава бързо дори през най-дебелите сухи клони, без усилие и без да засяда. Мислех, че ще трябва много повече сила, а е достатъчно да го водите с една ръка.“"),
    ("✅ Una potenza sorprendente", "✅ Изненадваща мощност"),
    ("David M. — MiniSawX in mano", "David M. — MiniSawX в ръка"),
    ("“È potente, comoda da tenere in mano e facile da usare, anche per chi non aveva mai preso una motosega. In un pomeriggio ho potato tutti gli alberi da frutto del giardino.”",
     "„Мощен е, удобен в ръка и лесен за ползване, дори за човек, който никога не е хващал трион. За един следобед подрязах всички овошки в градината.“"),
    ("✅ Fa il suo lavoro", "✅ Върши работата си"),
    ("Miguel T. — MiniSawX con asta telescopica", "Miguel T. — MiniSawX с телескопична щанга"),
    ("“L’asta telescopica arriva senza fatica ai rami più alti, quindi non devo più salire su una scala instabile. Ho finito in metà tempo e mi sono sentito molto più sicuro.”",
     "„Телескопичната щанга стига без усилие до най-високите клони, така че вече не се качвам на нестабилна стълба. Приключих за наполовина време и се чувствах много по-сигурен.“"),
    ("✅ Più veloce e più sicura", "✅ По-бързо и по-безопасно"),
    ("📦 Tutto incluso", "📦 Всичко е включено"),
    ("Kit completo MiniSawX.<br>\n        Niente extra. Niente sorprese.", "Пълен комплект MiniSawX.<br>\n        Без доплащания. Без изненади."),
    ("Apri la scatola, monti e inizi a tagliare. Non manca niente.", "Отваряте кутията, сглобявате и започвате да режете. Нищо не липсва."),
    ("Kit completo MiniSawX — tutto quello che c’è nel pacco", "Пълен комплект MiniSawX — всичко в пратката"),
    ("Cosa c’è nella scatola", "Какво има в кутията"),
    ("A cosa serve davvero", "За какво наистина служи"),
    ("⚙️ Motosega elettrica MiniSawX", "⚙️ Електрически трион MiniSawX"),
    ("3.000 W in modalità compatta — il cuore del kit", "3 000 W в компактен режим — сърцето на комплекта"),
    ("🪜 Asta telescopica fino a 5 metri", "🪜 Телескопична щанга до 5 метра"),
    ("Arrivi in cima all’albero senza scala", "Стигате върха на дървото без стълба"),
    ("🔋 2 batterie da 48 V e 8.000 mAh", "🔋 2 батерии 48 V и 8 000 mAh"),
    ("Una al lavoro, l’altra in carica — non ti fermi", "Едната работи, другата се зарежда — не спирате"),
    ("⚡ Caricabatterie rapido", "⚡ Бързо зарядно"),
    ("45 minuti e torni a tagliare", "45 минути и пак режете"),
    ("⛓️ 2 catene di ricambio", "⛓️ 2 резервни вериги"),
    ("Non resti a metà ramo senza catena", "Не оставате по средата на клона без верига"),
    ("🛢️ Serbatoio olio + AutoChain X™", "🛢️ Резервоар за масло + AutoChain X™"),
    ("Lubrifica e tende da sola — manutenzione minima", "Смазва и обтяга сам — минимална поддръжка"),
    ("🧰 Set di attrezzi e valigetta", "🧰 Комплект инструменти и куфарче"),
    ("Tutto al suo posto, pronto da riporre", "Всичко на мястото си, готово за прибиране"),
    ("🛡️ Garanzia ufficiale 2 anni", "🛡️ Официална 2-годишна гаранция"),
    ("Assistenza inclusa — 30 giorni per il reso", "Помощ включена — 30 дни за връщане"),
    ("❓ Le domande più frequenti", "❓ Най-често задаваните въпроси"),
    ("Qualche dubbio? È normale.<br>\n        Lo chiarisco tutto qui.", "Съмнения? Нормално е.<br>\n        Тук изяснявам всичко."),
    ("Prima di ordinare, le risposte alle domande di sempre: consegna, pagamento, benzina, rami alti e reso.",
     "Преди да поръчате, отговорите на обичайните въпроси: доставка, плащане, бензин, високи клони и връщане."),
    ("Quando arriva l’ordine?", "Кога пристига поръчката?"),
    ("La consegna richiede circa 1–2 giorni lavorativi. Spedizione gratuita in tutta Italia.",
     "Доставката отнема около 1–2 работни дни. Безплатна доставка в цяла България."),
    ("Devo pagare in anticipo?", "Трябва ли да платя предварително?"),
    ("No. Paghi direttamente al corriere al momento della consegna. Niente carta. Niente anticipo.",
     "Не. Плащате директно на куриера при доставката. Без карта. Без аванс."),
    ("Serve la benzina?", "Трябва ли бензин?"),
    ("No. La MiniSawX funziona solo a batteria: due da 48 V e 8.000 mAh. Niente miscela, niente fumi, niente cavo di avviamento.",
     "Не. MiniSawX работи само с батерия: две по 48 V и 8 000 mAh. Без смес, без изпарения, без стартово въже."),
    ("Riesco a tagliare i rami alti senza scala?", "Мога ли да режа високите клони без стълба?"),
    ("Sì. L’asta telescopica arriva fino a 5 metri. Vicino al suolo usi il modo manuale compatto. In cima all’albero, monti l’asta.",
     "Да. Телескопичната щанга достига 5 метра. Близо до земята ползвате компактния ръчен режим. На върха на дървото слагате щангата."),
    ("E se poi non mi convince?", "А ако после не ме убеди?"),
    ("Hai 30 giorni per chiedere il reso, secondo le condizioni di rimborso. Non rischi niente.",
     "Имате 30 дни да поискате връщане според условията за възстановяване. Не рискувате нищо."),
    ("✅ Paghi quando arriva", "✅ Плащате, когато пристигне"),
    ("INSERISCI I DATI DI CONSEGNA", "ВЪВЕДЕТЕ ДАННИТЕ ЗА ДОСТАВКА"),
    ("L’ordine parte subito. Paghi solo alla consegna, direttamente al corriere.",
     "Поръчката тръгва веднага. Плащате само при доставка, директно на куриера."),
]

BG_TY = [
    ("Ordine ricevuto — Attendi la chiamata di conferma | MiniSawX", "Поръчката е получена — Изчакайте обаждането за потвърждение | MiniSawX"),
    ("Il tuo ordine MiniSawX è stato registrato. Manca solo un ultimo passaggio: rispondi alla chiamata di conferma del nostro operatore.",
     "Вашата поръчка MiniSawX е регистрирана. Остава само последната стъпка: отговорете на обаждането за потвърждение от нашия оператор."),
    ("Il tuo ordine MiniSawX è stato registrato!", "Вашата поръчка MiniSawX е регистрирана!"),
    ("Perfetto — il tuo ordine è in elaborazione. Manca solo <strong>un ultimo passaggio</strong> per completarlo e far partire la spedizione.",
     "Перфектно — поръчката се обработва. Остава само <strong>една последна стъпка</strong>, за да я завършите и да тръгне доставката."),
    ("MiniSawX — motosega elettrica telescopica", "MiniSawX — електрически телескопичен верижен трион"),
    ("Kit completo · Pagamento alla consegna", "Пълен комплект · Наложен платеж"),
    ("👇 Cosa devi fare adesso", "👇 Какво трябва да направите сега"),
    ("📞 Rispondi alla chiamata di conferma", "📞 Отговорете на обаждането за потвърждение"),
    ("Un nostro operatore ti contatterà <strong>nelle prossime ore</strong> per confermare il tuo ordine MiniSawX.",
     "Наш оператор ще се свърже <strong>в следващите часове</strong>, за да потвърди вашата поръчка MiniSawX."),
    ("Se non rispondi alla chiamata, l'ordine verrà automaticamente annullato.",
     "Ако не отговорите на обаждането, поръчката ще бъде автоматично анулирана."),
    ("🕒 Orari di contatto", "🕒 Часове за контакт"),
    ("Lunedì – Sabato · 9:00 – 18:00", "Понеделник – събота · 9:00 – 18:00"),
    ("📋 Cosa succede dopo", "📋 Какво следва"),
    ("Rispondi alla chiamata e <strong>conferma i tuoi dati</strong>", "Отговорете на обаждането и <strong>потвърдете данните си</strong>"),
    ("La tua MiniSawX verrà spedita entro <strong>24–48 ore</strong>", "Вашият MiniSawX ще бъде изпратен в рамките на <strong>24–48 часа</strong>"),
    ("Consegna a domicilio e <strong>pagamento alla consegna</strong>", "Доставка до дома и <strong>наложен платеж</strong>"),
    ("🔒 Pagamento alla consegna", "🔒 Наложен платеж"),
    ("🛡️ Garanzia 2 anni", "🛡️ Гаранция 2 години"),
    ("↩️ 30 giorni di prova", "↩️ 30 дни проба"),
]


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(f"wrote {path.relative_to(ROOT)} ({len(text)} bytes)")


def patch_gsh_landing(geo: str, cfg: dict) -> str:
    html = (GSH / cfg["src"] / "index.html").read_text(encoding="utf-8")
    html = swap_gtag(html, thank_you=False)
    html = branding(html)
    html = html.replace(f"https://gadgetroomhub.com/{cfg['src']}/", f"https://gadgetroomhub.com/{geo}/mini-saw/")
    html = html.replace(f"https://gadgetroomhub.com/{cfg['src']}/thank-you.html", f"https://gadgetroomhub.com/{geo}/mini-saw/thank-you.html")
    html = cache_bust(html)
    html = html.replace("GEO: 'it'", f"GEO: '{geo}'")  # just in case
    return html


def patch_gsh_ty(geo: str, cfg: dict) -> str:
    html = (GSH / cfg["src"] / "thank-you.html").read_text(encoding="utf-8")
    html = swap_gtag(html, thank_you=True)
    html = branding(html)
    html = cache_bust(html)
    return html


def patch_it_landing(geo: str, cfg: dict, pairs: list[tuple[str, str]]) -> str:
    html = IT_LANDING
    html = html.replace('<html lang="it">', f'<html lang="{cfg["lang"]}">')
    html = html.replace("  GEO: 'it',", f"  GEO: '{geo}',")
    html = html.replace("  PRICE: 59,", f"  PRICE: {cfg['price']},")
    html = html.replace("  CURRENCY: 'EUR',", f"  CURRENCY: '{cfg['currency']}',")
    html = html.replace("  OFFER_NAME: 'MiniSawX 1274',", f"  OFFER_NAME: 'MiniSawX {cfg['offer']}',")
    html = html.replace("  LP_ID: 'it-1293',", f"  LP_ID: '{geo}-{cfg['lp']}',")
    html = html.replace('href="https://gadgetroomhub.com/mini-saw/"', f'href="https://gadgetroomhub.com/{geo}/mini-saw/"')
    html = html.replace('value="1274"', f'value="{cfg["offer"]}"')
    html = html.replace('value="1293"', f'value="{cfg["lp"]}"')
    html = html.replace(
        "https://gadgetroomhub.com/mini-saw/thank-you.html",
        f"https://gadgetroomhub.com/{geo}/mini-saw/thank-you.html",
    )
    html = apply_pairs(html, pairs)
    html = html.replace("59,00€", cfg["display"])
    html = html.replace("196,00€", cfg["old"])
    html = re.sub(r"<footer class=\"site-footer\">.*?</footer>", landing_footer(geo), html, count=1, flags=re.S)
    return html


def patch_it_ty(geo: str, cfg: dict, pairs: list[tuple[str, str]]) -> str:
    html = IT_TY
    html = html.replace('<html lang="it">', f'<html lang="{cfg["lang"]}">')
    html = html.replace("  GEO: 'it',", f"  GEO: '{geo}',")
    html = html.replace("  PRICE: 59,", f"  PRICE: {cfg['price']},")
    html = html.replace("  CURRENCY: 'EUR',", f"  CURRENCY: '{cfg['currency']}',")
    cookie_text, cookie_accept, cookie_learn = cfg["cookie"]
    html = html.replace(
        "COOKIE_TEXT: 'Usiamo cookie tecnici e di terze parti per migliorare la tua esperienza e per analisi.'",
        f"COOKIE_TEXT: '{cookie_text}'",
    )
    html = html.replace("COOKIE_ACCEPT: 'Accetta'", f"COOKIE_ACCEPT: '{cookie_accept}'")
    html = html.replace("COOKIE_LEARN: 'Scopri di più'", f"COOKIE_LEARN: '{cookie_learn}'")
    html = apply_pairs(html, pairs)
    html = html.replace("59,00€", cfg["display"])
    html = re.sub(r"<footer class=\"site-footer\">.*?</footer>", ty_footer(geo), html, count=1, flags=re.S)
    return html


CARD = """    <article class="product-card">
      <a class="product-card__image" href="/{geo}/mini-saw/">
        <img src="/assets/img/products/saw3000x/hero.webp?v=20260905" alt="MiniSawX" loading="lazy" decoding="async" width="640" height="480" onerror="this.src='/assets/img/placeholder.svg'">
      </a>
      <div class="product-card__body">
        <h3 class="product-card__title"><a href="/{geo}/mini-saw/">MiniSawX</a></h3>
        <p class="product-card__desc">{desc}</p>
        <div class="product-card__price"><span class="product-card__price-new">{price}</span></div>
        <a class="product-card__cta" href="/{geo}/mini-saw/">{cta}</a>
      </div>
    </article>
"""


def insert_home_card(geo: str, price: str, cta: str, desc: str) -> None:
    path = ROOT / geo / "index.html"
    text = path.read_text(encoding="utf-8")
    if f"/{geo}/mini-saw/" in text:
        print(f"home card already in {geo}/index.html")
        return
    card = CARD.format(geo=geo, price=price, cta=cta, desc=desc)
    marker = '<div class="products-grid__list">\n'
    idx = text.find(marker)
    if idx < 0:
        raise SystemExit(f"no products grid in {geo}/index.html")
    insert_at = text.find("</article>", idx)
    if insert_at < 0:
        raise SystemExit(f"no article in {geo}/index.html")
    insert_at += len("</article>\n")
    text = text[:insert_at] + card + text[insert_at:]
    path.write_text(text, encoding="utf-8")
    print(f"home card → {geo}/index.html")


def update_sitemap(geos: list[str]) -> None:
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    block = []
    for geo in geos:
        url = f"https://gadgetroomhub.com/{geo}/mini-saw/"
        if url not in text:
            block.append(
                f'  <url><loc>{url}</loc><lastmod>2026-09-08</lastmod><changefreq>weekly</changefreq><priority>0.95</priority></url>'
            )
    if not block:
        print("sitemap already up to date")
        return
    needle = '  <url><loc>https://gadgetroomhub.com/it/mini-saw/</loc><lastmod>2026-09-05</lastmod><changefreq>weekly</changefreq><priority>0.95</priority></url>\n'
    if needle not in text:
        raise SystemExit("sitemap mini-saw anchor missing")
    text = text.replace(needle, needle + "\n".join(block) + "\n")
    path.write_text(text, encoding="utf-8")
    print(f"sitemap +{len(block)}")


def leftover_italian(html: str) -> list[str]:
    needles = [
        "Motosega", "Pagamento alla consegna", "Spedizione", "Prenota", "Consegna in tutta Italia",
        "Nome e Cognome", "Indirizzo di consegna", "CONFERMA ORDINE", "Quando arriva",
        "Chi siamo", "Informazioni", "Tutti i diritti", "Invio...", "Accetta",
    ]
    return [n for n in needles if n in html]


def main() -> None:
    geos = []
    for geo, cfg in GSH_GEOS.items():
        landing = patch_gsh_landing(geo, cfg)
        ty = patch_gsh_ty(geo, cfg)
        write(ROOT / geo / "mini-saw" / "index.html", landing)
        write(ROOT / geo / "mini-saw" / "thank-you.html", ty)
        insert_home_card(geo, cfg["display"], cfg["cta"], cfg["desc"])
        geos.append(geo)

    translated = {"lv": (LV, LV_TY), "gr": (GR, GR_TY), "bg": (BG, BG_TY)}
    for geo, (pairs, ty_pairs) in translated.items():
        cfg = NEW_GEOS[geo]
        landing = patch_it_landing(geo, cfg, pairs)
        ty = patch_it_ty(geo, cfg, ty_pairs)
        leftover = leftover_italian(landing)
        if leftover:
            print(f"WARN leftover IT in {geo} landing: {leftover}")
        leftover_ty = leftover_italian(ty)
        if leftover_ty:
            print(f"WARN leftover IT in {geo} thank-you: {leftover_ty}")
        write(ROOT / geo / "mini-saw" / "index.html", landing)
        write(ROOT / geo / "mini-saw" / "thank-you.html", ty)
        insert_home_card(geo, cfg["display"], cfg["cta"], cfg["desc"])
        geos.append(geo)

    update_sitemap(geos)


if __name__ == "__main__":
    main()

