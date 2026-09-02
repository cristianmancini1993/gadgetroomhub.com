#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate Kemppi portable welder landings for CEE geos (offers #166–#171)."""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

GEOS = {
    "166": {
        "geo": "si",
        "lang": "sl",
        "tr": "si",
        "price": 99.99,
        "currency": "EUR",
        "slug": "kemppi-166",
        "country": "Sloveniji",
        "cpa": 17.0,
    },
    "167": {
        "geo": "ro",
        "lang": "ro",
        "tr": "ro",
        "price": 549.00,
        "currency": "RON",
        "slug": "kemppi-167",
        "country": "România",
        "cpa": 17.0,
    },
    "168": {
        "geo": "pl",
        "lang": "pl",
        "tr": "pl",
        "price": 439.00,
        "currency": "PLN",
        "slug": "kemppi-168",
        "country": "Polsce",
        "cpa": 17.0,
    },
    "169": {
        "geo": "hu",
        "lang": "hu",
        "tr": "hu",
        "price": 36999.00,
        "currency": "HUF",
        "slug": "kemppi-169",
        "country": "Magyarországon",
        "cpa": 17.0,
    },
    "170": {
        "geo": "cz",
        "lang": "cs",
        "tr": "cz",
        "price": 2449.00,
        "currency": "CZK",
        "slug": "kemppi-170",
        "country": "Česku",
        "cpa": 17.0,
    },
    "171": {
        "geo": "sk",
        "lang": "sk",
        "tr": "sk",
        "price": 99.99,
        "currency": "EUR",
        "slug": "kemppi-171",
        "country": "Slovensku",
        "cpa": 17.0,
    },
}


def was_price(now: float) -> float:
    return round(now / 0.4 + 1e-9, 2)


def fmt_price(amount: float, currency: str) -> str:
    if currency == "RON":
        whole = int(amount)
        frac = int(round((amount - whole) * 100))
        whole_s = f"{whole:,}".replace(",", ".")
        return f"{whole_s},{frac:02d} lei"
    if currency == "CZK":
        whole = int(round(amount))
        whole_s = f"{whole:,}".replace(",", ".")
        return f"{whole_s},00 Kč"
    if currency == "HUF":
        whole = int(round(amount))
        whole_s = f"{whole:,}".replace(",", ".")
        return f"{whole_s} Ft"
    if currency == "PLN":
        whole = int(amount)
        frac = int(round((amount - whole) * 100))
        whole_s = f"{whole:,}".replace(",", ".")
        return f"{whole_s},{frac:02d} zł"
    s = f"{amount:.2f}".replace(".", ",")
    return f"{s} €"


def load_ga_shared() -> dict:
    """Reuse footer/cookie/thank-you chrome from GlacierAir i18n."""
    tr: dict = {}
    for name in ("_ga_i18n_part1", "_ga_i18n_part2", "_ga_i18n_part3"):
        path = Path(__file__).with_name(f"{name}.py")
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(mod)
        tr.update(mod.TRANSLATIONS)
    return tr


# Kemppi product copy per language key (si/ro/pl/hu/cz/sk)
COPY = {
    "si": {
        "title": "Kemppi™ — Prenosni varilni aparat 8 v 1 MIG TIG elektroda | -60%",
        "description": "Kemppi™: prenosni varilni aparat 8 v 1 (MIG, TIG, elektroda, rezanje) do 200A in 5 mm. Kompletni komplet vključen, plačilo po povzetju v Sloveniji.",
        "topbar": "🔥 POPUST 60 % + BREZPLAČNA DOSTAVA — PLAČILO PO POVZETJU 🔥",
        "rating": "<strong>4,8/5</strong> — Ocene od <strong>3.842</strong> preverjenih strank",
        "gift": "🎁 BREZPLAČNO: KOMPLET PRIBORA + ROKAVICE",
        "h1": "Ne kupujte 8 različnih aparatov.<br>Dovolj je eden: <span class=\"hl\">Kemppi™</span>",
        "lead": "Z enim aparatom varite skoraj vsak material: <strong>MIG, TIG, elektroda in rezanje</strong> — jeklo, nerjavno jeklo in lito železo do <strong>5 mm</strong>. Kompakten, zmogljiv in vedno pripravljen, s kompletnim kompletom pribora.",
        "alt_hero": "Kemppi prenosni varilni aparat 8 v 1",
        "cta": "DA, ŽELIM Kemppi™ →",
        "form_note": "🔒 Brez predplačila · Brez kartice · Plačate šele ob prejemu",
        "f1_h": "8 funkcij v 1",
        "f1_p": "MIG · TIG · elektroda · rezanje",
        "f2_h": "Prava moč 200A",
        "f2_p": "Taljenje do 5 mm debeline",
        "f3_h": "Kompletni komplet",
        "f3_p": "Maska, rokavice, elektrode in kabli",
        "f4_h": "Plačilo po povzetju",
        "f4_p": "Priročno, varno, brez predplačila",
        "countdown": "⏰ 60 % popust poteče čez",
        "stock_l": "Razpoložljivost na zalogi",
        "stock_r": "Ostali so samo še 4 kosi",
        "live": "<strong>{n} oseb</strong> trenutno gleda Kemppi",
        "live0": "<strong>41 oseb</strong> trenutno gleda Kemppi",
        "form_h2": "Dokončajte naročilo",
        "form_p": "Izpolnite obrazec: naša ekipa vas bo kontaktirala za potrditev podrobnosti.",
        "label_name": "Ime in priimek*",
        "label_phone": "Telefonska številka*",
        "label_addr": "Naslov za dostavo*",
        "ph_name": "Luka Novak",
        "ph_phone": "+386 41 123 456",
        "ph_addr": "Ulica 10, 1000 Ljubljana",
        "btn": "DA, ŽELIM Kemppi™",
        "ey1": "01 — Sistem vse v enem",
        "h3_1": "8 funkcij v enem aparatu — brez kompromisov",
        "tag1a": "MIG",
        "tag1b": "TIG Lift DC",
        "tag1c": "MMA",
        "tag1d": "Rezanje",
        "p1": "Varjenje MIG brez plina, TIG Lift DC, MMA z elektrodo, točkovno varjenje in rezanje — vse, kar ponuja profesionalna delavnica, v enem kompaktnem aparatu. <strong>Ničesar drugega vam ni treba kupiti.</strong>",
        "i1": "Od majhnega popravila doma do zahtevnejšega dela — vse z enim orodjem.",
        "alt_d1": "Kemppi 8 funkcij v enem aparatu",
        "ey2": "02 — Profesionalni rezultati takoj",
        "h3_2": "Čisti zvari in samodejna regulacija toka",
        "tag2a": "Hot Start",
        "tag2b": "Anti-Stick",
        "tag2c": "Arc Force",
        "p2": "Zaradi vgrajenih sistemov Hot Start, Anti-Stick in Arc Force ostane lok stabilen tudi, če še niste držali elektrode. Izberete material in debelino: <strong>Kemppi™ sam nastavi napetost in amperažo.</strong>",
        "i2": "Konec zažganih zvarov in lukenj v pločevini — čisti rezultati že od prvega uporabe.",
        "alt_d2": "Kemppi čisti zvari in samodejna regulacija",
        "ey3": "03 — Zmogljiv, a prenosljiv",
        "h3_3": "Prava moč 200A — deluje iz domače vtičnice",
        "tag3a": "200A",
        "tag3b": "IGBT",
        "tag3c": "220V",
        "p3": "Vari jeklo, nerjavno jeklo in lito železo do <strong>5 mm</strong> brez sunkov toka. Inverterska tehnologija IGBT pametno upravlja porabo: <strong>deluje iz običajne vtičnice 220V</strong>, v garaži ali na gradbišču.",
        "i3": "Tehta le nekaj kilogramov — nosite ga kot torbo od vratnih vrat do cevi na gradbišču.",
        "alt_d3": "Kemppi prenosni varilec za garažo in gradbišče",
        "cmp_label": "Zakaj se res splača",
        "cmp_h2": "Ločeni varilci vs Kemppi™",
        "th_sep": "3 ločeni aparati",
        "r1a": "Strošek",
        "r1b": "≈ {sep}",
        "r1c": "{now} enkrat",
        "r2a": "MIG + TIG + elektroda",
        "r2b": "Da, a 3 aparati",
        "r2c": "Vse v enem",
        "r3a": "Prostor",
        "r3b": "Zapolni garažo",
        "r3c": "En kovček",
        "r4a": "Za začetnike",
        "r4b": "Potrebne izkušnje",
        "r4c": "Samodejna regulacija",
        "r5a": "Komplet pribora",
        "r5b": "Pogosto posebej",
        "r5c": "Maska, rokavice, elektrode vključene",
        "r6a": "Garancija",
        "r6b": "Različna",
        "r6c": "4 leta + vračilo 30 dni",
        "rev_h2": "Na tisoče strank ga priporoča",
        "rev_sub": "★ 4,8/5 · Preverjen nakup · Pregledane ocene",
        "rev1_h": "Prišel danes, odlično vari",
        "rev1_p": "«Prišel danes, lepo zapakirano. V kovčku je res vse: maska, rokavice, elektrode. Takoj preizkušen na nosilcu — odlično vari. Zelo zadovoljen.»",
        "rev1_a": "Luka N. ✅ — Preverjen nakup",
        "rev2_h": "Idealno tudi za začetnike",
        "rev2_p": "«Uporabljam ga v garaži za drobna dela. Lahek in priročen. S samodejno regulacijo sem tudi kot začetnik naredil čist zvar.»",
        "rev2_a": "Matej K. ✅ — Preverjen nakup",
        "rev3_h": "Uspeh že ob prvem poskusu",
        "rev3_p": "«Uporabil sem ga za ojačitev nosilca na vrtu: zvar uspel že prvič. Robustno, vse vključeno in plačano ob dostavi. Zame je odlično.»",
        "rev3_a": "Petra M. ✅ — Preverjen nakup",
        "kit_eye": "Kaj prejmete v paketu",
        "kit_h2": "📦 Kompletni komplet Kemppi™ 8 v 1",
        "alt_kit": "Kompletni komplet Kemppi prenosni varilec",
        "li1": "<strong>1× Varilec Kemppi™</strong> 8 v 1 (MIG · TIG · elektroda · rezanje)",
        "li2": "1× Profesionalna zaščitna maska",
        "li3": "1× Par rokavic za visoke temperature",
        "li4": "1× Izbrani set elektrod",
        "li5": "1× Visokokakovostne sponke in kabli",
        "li6": "1× Navodila v slovenščini + hitri vodič",
        "li7": "Garancija 4 leta + podpora v slovenščini",
        "li8": "Brezplačna dostava 24/48 h po Sloveniji",
        "faq_h2": "Pogosta vprašanja",
        "fq1": "Ali lahko plačam, ko paket prispe?",
        "fa1": "Da. Plačate v gotovini kurirju ob dostavi, brez podatkov o kartici. Sledenje prek SMS in e-pošte v 24–48 urah.",
        "fq2": "Ali potrebujem tehnika za montažo?",
        "fa2": "Ne: odprete škatlo, priklopite kable in ste pripravljeni v približno 60 sekundah. Kompletni komplet je vključen.",
        "fq3": "Ali bo izklopil varovalke doma?",
        "fa3": "Ne. Inverterska tehnologija IGBT upravlja porabo brez sunkov in deluje iz običajne vtičnice 220V.",
        "fq4": "Ali je primeren tudi za začetnike?",
        "fa4": "Da. Hot Start, Anti-Stick, Arc Force in samodejna regulacija toka pomagajo do čistih zvarov že od prvega uporabe.",
        "fq5": "Ali ga lahko vrnem, če me ne prepriča?",
        "fa5": "Imate 30 dni za vračilo s polnim povračilom, plus 4 leta garancije in podporo strankam.",
        "fq6": "Koliko stane dostava in kako dolgo traja?",
        "fa6": "Dostava je <strong>brezplačna</strong> po {country}. Naročilo obdelamo v 24 urah; kurir pride v 24/48 delovnih urah.",
        "lang_label": "slovenščini",
    },
    "ro": {
        "title": "Kemppi™ — Aparat de sudură portabil 8 în 1 MIG TIG electrod | -60%",
        "description": "Kemppi™: aparat de sudură portabil 8 în 1 (MIG, TIG, electrod, tăiere) până la 200A și 5 mm. Kit complet inclus, plata ramburs în România.",
        "topbar": "🔥 REDUCERE 60% + LIVRARE GRATUITĂ — PLATĂ RAMBURS 🔥",
        "rating": "<strong>4,8/5</strong> — Evaluat de <strong>3.842</strong> clienți verificați",
        "gift": "🎁 CADOU: KIT ACCESORII + MĂNUȘI",
        "h1": "Nu cumpăra 8 aparate diferite.<br>Îți trebuie doar unul: <span class=\"hl\">Kemppi™</span>",
        "lead": "Cu un singur aparat sudezi aproape orice material: <strong>MIG, TIG, electrod și tăiere</strong> — oțel, inox și fontă până la <strong>5 mm</strong>. Compact, puternic și gata de folosit, cu kit complet de accesorii inclus.",
        "alt_hero": "Kemppi aparat de sudură portabil 8 în 1",
        "cta": "DA, VREAU Kemppi™ →",
        "form_note": "🔒 Zero avans · Zero card · Plătești doar când îl primești",
        "f1_h": "8 funcții în 1",
        "f1_p": "MIG · TIG · electrod · tăiere",
        "f2_h": "Putere reală 200A",
        "f2_p": "Sudură până la 5 mm grosime",
        "f3_h": "Kit complet inclus",
        "f3_p": "Mască, mănuși, electrozi și cabluri",
        "f4_h": "Plată ramburs",
        "f4_p": "Convenabil, sigur, fără avans",
        "countdown": "⏰ Reducerea de 60% expiră în",
        "stock_l": "Disponibilitate în stoc",
        "stock_r": "Au mai rămas doar 4 buc.",
        "live": "<strong>{n} persoane</strong> privesc Kemppi acum",
        "live0": "<strong>41 persoane</strong> privesc Kemppi acum",
        "form_h2": "Finalizează comanda",
        "form_p": "Completează formularul: echipa noastră te va contacta pentru a confirma detaliile.",
        "label_name": "Nume și prenume*",
        "label_phone": "Număr de telefon*",
        "label_addr": "Adresa de livrare*",
        "ph_name": "Andrei Popescu",
        "ph_phone": "+40 721 123 456",
        "ph_addr": "Str. Exemplu 10, București",
        "btn": "DA, VREAU Kemppi™",
        "ey1": "01 — Sistem all-in-one",
        "h3_1": "8 funcții într-un singur aparat — fără compromisuri",
        "tag1a": "MIG",
        "tag1b": "TIG Lift DC",
        "tag1c": "MMA",
        "tag1d": "Tăiere",
        "p1": "Sudură MIG fără gaz, TIG Lift DC, MMA cu electrod, sudură în puncte și tăiere — tot ce oferă un atelier profesional, într-un aparat compact. <strong>Nu mai trebuie să cumperi nimic altceva.</strong>",
        "i1": "De la o mică reparație acasă la o lucrare mai grea — totul cu o singură unealtă.",
        "alt_d1": "Kemppi 8 funcții într-un singur aparat",
        "ey2": "02 — Rezultate profesionale din prima",
        "h3_2": "Suduri curate și reglare automată a curentului",
        "tag2a": "Hot Start",
        "tag2b": "Anti-Stick",
        "tag2c": "Arc Force",
        "p2": "Datorită sistemelor Hot Start, Anti-Stick și Arc Force, arcul rămâne stabil chiar dacă nu ai mai ținut un electrod. Alegi materialul și grosimea: <strong>Kemppi™ setează singur tensiunea și amperajul.</strong>",
        "i2": "Gata cu sudurile arse și găurile în tablă — rezultate curate de la prima utilizare.",
        "alt_d2": "Kemppi suduri curate și reglare automată",
        "ey3": "03 — Puternic, dar portabil",
        "h3_3": "Putere reală 200A — compatibil cu priza de acasă",
        "tag3a": "200A",
        "tag3b": "IGBT",
        "tag3c": "220V",
        "p3": "Sudează oțel carbon, inox și fontă până la <strong>5 mm</strong> fără salturi de curent. Tehnologia inverter IGBT gestionează inteligent consumul: <strong>funcționează dintr-o priză normală 220V</strong>, în garaj sau pe șantier.",
        "i3": "Cântărește doar câteva kilograme — îl porți oriunde ca pe o geantă.",
        "alt_d3": "Kemppi portabil pentru garaj și șantier",
        "cmp_label": "De ce merită cu adevărat",
        "cmp_h2": "Aparate separate vs Kemppi™",
        "th_sep": "3 aparate separate",
        "r1a": "Cost",
        "r1b": "≈ {sep}",
        "r1c": "{now} o singură dată",
        "r2a": "MIG + TIG + electrod",
        "r2b": "Da, dar 3 aparate",
        "r2c": "Totul într-unul",
        "r3a": "Spațiu",
        "r3b": "Umple garajul",
        "r3c": "O valiză",
        "r4a": "Ușor pentru începători",
        "r4b": "Necesită experiență",
        "r4c": "Reglare automată",
        "r5a": "Kit accesorii",
        "r5b": "Adesea separat",
        "r5c": "Mască, mănuși, electrozi incluși",
        "r6a": "Garanție",
        "r6b": "Variabilă",
        "r6c": "4 ani + retur 30 zile",
        "rev_h2": "Mii de clienți îl recomandă",
        "rev_sub": "★ 4,8/5 · Achiziție verificată · Recenzii verificate",
        "rev1_h": "A ajuns azi, sudează excelent",
        "rev1_p": "«A ajuns azi, foarte bine ambalat. În valiză e chiar tot: mască, mănuși, electrozi. L-am încercat imediat pe un suport — sudează excelent. Foarte mulțumit.»",
        "rev1_a": "Andrei M. ✅ — Achiziție verificată",
        "rev2_h": "Ideal și pentru începători",
        "rev2_p": "«Îl folosesc în garaj pentru lucrări mici. Ușor și comod de mutat. Cu reglarea automată, chiar și ca începător am făcut o sudură curată.»",
        "rev2_a": "Ionuț R. ✅ — Achiziție verificată",
        "rev3_h": "Reușit din prima încercare",
        "rev3_p": "«L-am folosit să consolidez un suport în grădină: sudură reușită din prima. Robust, totul inclus și plătit la livrare. Pentru mine e promovat.»",
        "rev3_a": "Maria D. ✅ — Achiziție verificată",
        "kit_eye": "Ce primești în pachet",
        "kit_h2": "📦 Kitul complet Kemppi™ 8 în 1",
        "alt_kit": "Kit complet Kemppi aparat de sudură portabil",
        "li1": "<strong>1× Aparat Kemppi™</strong> 8 în 1 (MIG · TIG · electrod · tăiere)",
        "li2": "1× Masca de protecție profesională",
        "li3": "1× Pereche de mănuși rezistente la temperaturi înalte",
        "li4": "1× Set de electrozi selectați",
        "li5": "1× Cleme și cabluri de calitate",
        "li6": "1× Instrucțiuni în română + ghid rapid",
        "li7": "Garanție 4 ani + suport în română",
        "li8": "Livrare gratuită 24/48 h în toată România",
        "faq_h2": "Întrebări frecvente",
        "fq1": "Pot plăti când ajunge coletul?",
        "fa1": "Da. Plătești cash curierului la livrare, fără date de card. Tracking prin SMS și e-mail în 24–48 de ore.",
        "fq2": "Am nevoie de tehnician pentru montaj?",
        "fa2": "Nu: deschizi cutia, conectezi cablurile și ești gata în aproximativ 60 de secunde. Kitul complet este inclus.",
        "fq3": "Sare siguranțele de acasă?",
        "fa3": "Nu. Tehnologia inverter IGBT gestionează consumul fără vârfuri bruște și funcționează dintr-o priză normală 220V.",
        "fq4": "Este potrivit și pentru începători?",
        "fa4": "Da. Hot Start, Anti-Stick, Arc Force și reglarea automată te ajută să obții suduri curate încă de la prima utilizare.",
        "fq5": "Pot returna produsul dacă nu sunt mulțumit?",
        "fa5": "Ai 30 de zile pentru retur cu rambursare completă, plus 4 ani garanție și asistență clienți.",
        "fq6": "Cât costă livrarea și cât durează?",
        "fa6": "Livrarea este <strong>gratuită</strong> în {country}. Procesăm comanda în 24 de ore; curierul ajunge în 24/48 de ore lucrătoare.",
        "lang_label": "română",
    },
    "pl": {
        "title": "Kemppi™ — Przenośna spawarka 8 w 1 MIG TIG elektroda | -60%",
        "description": "Kemppi™: przenośna spawarka 8 w 1 (MIG, TIG, elektroda, cięcie) do 200A i 5 mm. Pełny zestaw w zestawie, płatność przy odbiorze w Polsce.",
        "topbar": "🔥 RABAT 60% + DARMOWA DOSTAWA — PŁATNOŚĆ PRZY ODBIORZE 🔥",
        "rating": "<strong>4,8/5</strong> — Na podstawie <strong>3.842</strong> zweryfikowanych opinii",
        "gift": "🎁 GRATIS: ZESTAW AKCESORIÓW + RĘKAWICE",
        "h1": "Nie kupuj 8 różnych urządzeń.<br>Wystarczy jedno: <span class=\"hl\">Kemppi™</span>",
        "lead": "Jednym urządzeniem spawasz prawie każdy materiał: <strong>MIG, TIG, elektroda i cięcie</strong> — stal, nierdzewka i żeliwo do <strong>5 mm</strong>. Kompaktowa, mocna i gotowa do pracy, z kompletnym zestawem akcesoriów.",
        "alt_hero": "Kemppi przenośna spawarka 8 w 1",
        "cta": "TAK, CHCĘ Kemppi™ →",
        "form_note": "🔒 Zero zaliczki · Bez karty · Płacisz dopiero przy odbiorze",
        "f1_h": "8 funkcji w 1",
        "f1_p": "MIG · TIG · elektroda · cięcie",
        "f2_h": "Prawdziwa moc 200A",
        "f2_p": "Spawanie do 5 mm grubości",
        "f3_h": "Pełny zestaw w cenie",
        "f3_p": "Maska, rękawice, elektrody i kable",
        "f4_h": "Płatność przy odbiorze",
        "f4_p": "Wygodnie, bezpiecznie, bez zaliczki",
        "countdown": "⏰ Rabat 60% wygasa za",
        "stock_l": "Dostępność w magazynie",
        "stock_r": "Zostały tylko 4 szt.",
        "live": "<strong>{n} osób</strong> ogląda teraz Kemppi",
        "live0": "<strong>41 osób</strong> ogląda teraz Kemppi",
        "form_h2": "Dokończ zamówienie",
        "form_p": "Wypełnij formularz: nasz zespół skontaktuje się, aby potwierdzić szczegóły.",
        "label_name": "Imię i nazwisko*",
        "label_phone": "Numer telefonu*",
        "label_addr": "Adres dostawy*",
        "ph_name": "Jan Kowalski",
        "ph_phone": "+48 500 123 456",
        "ph_addr": "ul. Przykładowa 10, 00-001 Warszawa",
        "btn": "TAK, CHCĘ Kemppi™",
        "ey1": "01 — System wszystko w jednym",
        "h3_1": "8 funkcji w jednym urządzeniu — bez kompromisów",
        "tag1a": "MIG",
        "tag1b": "TIG Lift DC",
        "tag1c": "MMA",
        "tag1d": "Cięcie",
        "p1": "Spawanie MIG bez gazu, TIG Lift DC, MMA elektrodą, spawanie punktowe i cięcie — wszystko, co daje profesjonalny warsztat, w jednym kompaktowym urządzeniu. <strong>Nie musisz kupować niczego więcej.</strong>",
        "i1": "Od drobnej naprawy w domu po trudniejszą pracę — wszystko jednym narzędziem.",
        "alt_d1": "Kemppi 8 funkcji w jednym urządzeniu",
        "ey2": "02 — Profesjonalne efekty od razu",
        "h3_2": "Czyste spoiny i automatyczna regulacja prądu",
        "tag2a": "Hot Start",
        "tag2b": "Anti-Stick",
        "tag2c": "Arc Force",
        "p2": "Dzięki systemom Hot Start, Anti-Stick i Arc Force łuk pozostaje stabilny nawet jeśli nigdy nie trzymałeś elektrody. Wybierasz materiał i grubość: <strong>Kemppi™ sam ustawia napięcie i amperaż.</strong>",
        "i2": "Koniec ze spalonymi spoinami i dziurami w blasze — czyste efekty od pierwszego użycia.",
        "alt_d2": "Kemppi czyste spoiny i automatyczna regulacja",
        "ey3": "03 — Mocna, ale przenośna",
        "h3_3": "Prawdziwa moc 200A — działa z domowego gniazdka",
        "tag3a": "200A",
        "tag3b": "IGBT",
        "tag3c": "220V",
        "p3": "Spawa stal węglową, nierdzewną i żeliwo do <strong>5 mm</strong> bez skoków prądu. Technologia falownika IGBT inteligentnie zarządza poborem: <strong>działa ze zwykłego gniazdka 220V</strong>, w garażu lub na budowie.",
        "i3": "Waży tylko kilka kilogramów — nosisz ją jak torbę od furtki domu po rury na budowie.",
        "alt_d3": "Kemppi przenośna spawarka do garażu i budowy",
        "cmp_label": "Dlaczego naprawdę warto",
        "cmp_h2": "Osobne spawarki vs Kemppi™",
        "th_sep": "3 osobne maszyny",
        "r1a": "Koszt",
        "r1b": "≈ {sep}",
        "r1c": "{now} jednorazowo",
        "r2a": "MIG + TIG + elektroda",
        "r2b": "Tak, ale 3 urządzenia",
        "r2c": "Wszystko w jednym",
        "r3a": "Miejsce",
        "r3b": "Zapełnia garaż",
        "r3c": "Jedna walizka",
        "r4a": "Dla początkujących",
        "r4b": "Potrzebne doświadczenie",
        "r4c": "Automatyczna regulacja",
        "r5a": "Zestaw akcesoriów",
        "r5b": "Często osobno",
        "r5c": "Maska, rękawice, elektrody w zestawie",
        "r6a": "Gwarancja",
        "r6b": "Różna",
        "r6c": "4 lata + zwrot 30 dni",
        "rev_h2": "Tysiące klientów ją poleca",
        "rev_sub": "★ 4,8/5 · Zweryfikowany zakup · Sprawdzone opinie",
        "rev1_h": "Przyszła dziś, spawa świetnie",
        "rev1_p": "«Przyszła dziś, dobrze zapakowana. W walizce jest naprawdę wszystko: maska, rękawice, elektrody. Od razu przetestowałem na uchwycie — spawa świetnie. Bardzo zadowolony.»",
        "rev1_a": "Piotr K. ✅ — Zweryfikowany zakup",
        "rev2_h": "Idealna też dla początkujących",
        "rev2_p": "«Używam w garażu do drobnych prac. Lekka i wygodna do przenoszenia. Dzięki automatycznej regulacji nawet jako początkujący zrobiłem czystą spoinę.»",
        "rev2_a": "Marek W. ✅ — Zweryfikowany zakup",
        "rev3_h": "Udało się za pierwszym razem",
        "rev3_p": "«Użyłem do wzmocnienia uchwytu w ogrodzie: spoina wyszła za pierwszym razem. Solidna, wszystko w zestawie, płatność przy odbiorze. U mnie zdana.»",
        "rev3_a": "Anna N. ✅ — Zweryfikowany zakup",
        "kit_eye": "Co jest w paczce",
        "kit_h2": "📦 Kompletny zestaw Kemppi™ 8 w 1",
        "alt_kit": "Kompletny zestaw Kemppi przenośna spawarka",
        "li1": "<strong>1× Spawarka Kemppi™</strong> 8 w 1 (MIG · TIG · elektroda · cięcie)",
        "li2": "1× Profesjonalna maska ochronna",
        "li3": "1× Para rękawic odpornych na wysoką temperaturę",
        "li4": "1× Wybrany zestaw elektrod",
        "li5": "1× Wysokiej jakości zaciski i kable",
        "li6": "1× Instrukcja po polsku + szybki przewodnik",
        "li7": "Gwarancja 4 lata + wsparcie po polsku",
        "li8": "Darmowa dostawa 24/48 h w całej Polsce",
        "faq_h2": "Najczęstsze pytania",
        "fq1": "Czy mogę zapłacić przy odbiorze paczki?",
        "fa1": "Tak. Płacisz gotówką kurierowi przy dostawie, bez danych karty. Tracking SMS i e-mail w ciągu 24–48 godzin.",
        "fq2": "Czy potrzebuję technika do montażu?",
        "fa2": "Nie: otwierasz pudełko, podłączasz kable i jesteś gotowy w około 60 sekund. Pełny zestaw w cenie.",
        "fq3": "Czy wywali bezpieczniki w domu?",
        "fa3": "Nie. Technologia falownika IGBT zarządza poborem bez nagłych skoków i działa ze zwykłego gniazdka 220V.",
        "fq4": "Czy nadaje się dla początkujących?",
        "fa4": "Tak. Hot Start, Anti-Stick, Arc Force i automatyczna regulacja pomagają uzyskać czyste spoiny od pierwszego użycia.",
        "fq5": "Czy mogę zwrócić, jeśli nie spełni oczekiwań?",
        "fa5": "Masz 30 dni na zwrot z pełnym zwrotem pieniędzy, plus 4 lata gwarancji i wsparcie klienta.",
        "fq6": "Ile kosztuje dostawa i ile trwa?",
        "fa6": "Dostawa jest <strong>darmowa</strong> w {country}. Zamówienie realizujemy w 24 godziny; kurier przyjeżdża w 24/48 godzin roboczych.",
        "lang_label": "polskim",
    },
    "hu": {
        "title": "Kemppi™ — Hordozható hegesztőgép 8 az 1-ben MIG TIG elektróda | -60%",
        "description": "Kemppi™: hordozható hegesztőgép 8 az 1-ben (MIG, TIG, elektróda, vágás) 200A-ig és 5 mm-ig. Teljes készlet benne, utánvét Magyarországon.",
        "topbar": "🔥 60% KEDVEZMÉNY + INGYENES SZÁLLÍTÁS — UTÁNVÉT 🔥",
        "rating": "<strong>4,8/5</strong> — <strong>3.842</strong> ellenőrzött vásárló értékelése alapján",
        "gift": "🎁 AJÁNDÉK: KIEGÉSZÍTŐ KÉSZLET + KESZTYŰ",
        "h1": "Ne vegyen 8 különböző gépet.<br>Elég egy: <span class=\"hl\">Kemppi™</span>",
        "lead": "Egyetlen géppel szinte minden anyagot hegeszthet: <strong>MIG, TIG, elektróda és vágás</strong> — acél, rozsdamentes és öntöttvas <strong>5 mm</strong>-ig. Kompakt, erős és azonnal használható, teljes kiegészítő készlettel.",
        "alt_hero": "Kemppi hordozható hegesztőgép 8 az 1-ben",
        "cta": "IGEN, KÉREM a Kemppi™-t →",
        "form_note": "🔒 Nincs előleg · Nincs kártya · Csak átvételkor fizet",
        "f1_h": "8 funkció 1-ben",
        "f1_p": "MIG · TIG · elektróda · vágás",
        "f2_h": "Valódi 200A teljesítmény",
        "f2_p": "Hegesztés 5 mm vastagságig",
        "f3_h": "Teljes készlet benne",
        "f3_p": "Maszk, kesztyű, elektródák és kábelek",
        "f4_h": "Utánvét",
        "f4_p": "Kényelmes, biztonságos, előleg nélkül",
        "countdown": "⏰ A 60% kedvezmény lejár",
        "stock_l": "Raktárkészlet",
        "stock_r": "Már csak 4 db maradt",
        "live": "<strong>{n} ember</strong> nézi most a Kemppit",
        "live0": "<strong>41 ember</strong> nézi most a Kemppit",
        "form_h2": "Fejezze be a rendelést",
        "form_p": "Töltse ki az űrlapot: csapatunk felveszi Önnel a kapcsolatot a részletek megerősítéséhez.",
        "label_name": "Teljes név*",
        "label_phone": "Telefonszám*",
        "label_addr": "Szállítási cím*",
        "ph_name": "Kovács János",
        "ph_phone": "+36 30 123 4567",
        "ph_addr": "Példa utca 10, 1011 Budapest",
        "btn": "IGEN, KÉREM a Kemppi™-t",
        "ey1": "01 — Minden egyben rendszer",
        "h3_1": "8 funkció egyetlen gépben — kompromisszumok nélkül",
        "tag1a": "MIG",
        "tag1b": "TIG Lift DC",
        "tag1c": "MMA",
        "tag1d": "Vágás",
        "p1": "Gáz nélküli MIG, TIG Lift DC, MMA elektródával, ponthegesztés és vágás — mindaz, amit egy professzionális műhely kínál, egy kompakt gépben. <strong>Nem kell semmi mást vásárolnia.</strong>",
        "i1": "A kisebb házi javítástól a nehezebb munkáig — minden egyetlen eszközzel.",
        "alt_d1": "Kemppi 8 funkció egyetlen gépben",
        "ey2": "02 — Professzionális eredmény azonnal",
        "h3_2": "Tiszta varratok és automatikus áramszabályozás",
        "tag2a": "Hot Start",
        "tag2b": "Anti-Stick",
        "tag2c": "Arc Force",
        "p2": "A beépített Hot Start, Anti-Stick és Arc Force rendszereknek köszönhetően az ív stabil marad akkor is, ha még soha nem tartott elektródát. Válassza ki az anyagot és a vastagságot: <strong>a Kemppi™ magától beállítja a feszültséget és az ampert.</strong>",
        "i2": "Nincs többé megégett varrat és lyuk a lemezen — tiszta eredmény már az első használattól.",
        "alt_d2": "Kemppi tiszta varratok és automatikus szabályozás",
        "ey3": "03 — Erős, mégis hordozható",
        "h3_3": "Valódi 200A teljesítmény — otthoni konnektorról",
        "tag3a": "200A",
        "tag3b": "IGBT",
        "tag3c": "220V",
        "p3": "Szénacélt, rozsdamentest és öntöttvasat hegeszt <strong>5 mm</strong>-ig áramingadozás nélkül. Az IGBT inverter technológia okosan kezeli a felvételt: <strong>normál 220V-os konnektorról működik</strong>, garázsban vagy építkezésen.",
        "i3": "Csak néhány kilót nyom — úgy viszi, mint egy táskát, a kaputól az építési csövekig.",
        "alt_d3": "Kemppi hordozható hegesztő garázsba és telephelyre",
        "cmp_label": "Miért éri meg igazán",
        "cmp_h2": "Külön gépek vs Kemppi™",
        "th_sep": "3 külön gép",
        "r1a": "Költség",
        "r1b": "≈ {sep}",
        "r1c": "{now} egyszer",
        "r2a": "MIG + TIG + elektróda",
        "r2b": "Igen, de 3 gép",
        "r2c": "Minden egyben",
        "r3a": "Helyigény",
        "r3b": "Betölti a garázst",
        "r3c": "Egy táska",
        "r4a": "Kezdőknek is",
        "r4b": "Tapasztalat kell",
        "r4c": "Automatikus szabályozás",
        "r5a": "Kiegészítő készlet",
        "r5b": "Gyakran külön",
        "r5c": "Maszk, kesztyű, elektródák benne",
        "r6a": "Garancia",
        "r6b": "Változó",
        "r6c": "4 év + 30 napos visszaküldés",
        "rev_h2": "Több ezer vásárló ajánlja",
        "rev_sub": "★ 4,8/5 · Ellenőrzött vásárlás · Ellenőrzött értékelések",
        "rev1_h": "Ma megérkezett, remekül hegeszt",
        "rev1_p": "«Ma megérkezett, jól csomagolva. A táskában tényleg minden benne van: maszk, kesztyű, elektródák. Azonnal kipróbáltam egy konzolon — remekül hegeszt. Nagyon elégedett vagyok.»",
        "rev1_a": "László K. ✅ — Ellenőrzött vásárlás",
        "rev2_h": "Kezdőknek is ideális",
        "rev2_p": "«A garázsban használom apró munkákhoz. Könnyű és könnyen mozgatható. Az automatikus szabályozással kezdőként is tiszta varratot csináltam.»",
        "rev2_a": "Gábor T. ✅ — Ellenőrzött vásárlás",
        "rev3_h": "Elsőre sikerült",
        "rev3_p": "«Kerti konzolt erősítettem vele: a varrat elsőre sikerült. Strapabíró, minden benne, utánvéttel fizettem. Nálam átment.»",
        "rev3_a": "Eszter N. ✅ — Ellenőrzött vásárlás",
        "kit_eye": "Mit kap a csomagban",
        "kit_h2": "📦 A teljes Kemppi™ 8 az 1-ben készlet",
        "alt_kit": "Teljes Kemppi hordozható hegesztő készlet",
        "li1": "<strong>1× Kemppi™ hegesztő</strong> 8 az 1-ben (MIG · TIG · elektróda · vágás)",
        "li2": "1× Professzionális védőmaszk",
        "li3": "1× Magas hőmérsékletű kesztyű",
        "li4": "1× Válogatott elektróda készlet",
        "li5": "1× Minőségi bilincsek és kábelek",
        "li6": "1× Magyar útmutató + gyors segédlet",
        "li7": "4 év garancia + magyar támogatás",
        "li8": "Ingyenes szállítás 24/48 óra alatt Magyarországon",
        "faq_h2": "Gyakori kérdések",
        "fq1": "Fizethetek, amikor megérkezik a csomag?",
        "fa1": "Igen. Készpénzzel fizet a futárnak átvételkor, kártyaadatok nélkül. Követés SMS-ben és e-mailben 24–48 órán belül.",
        "fq2": "Szerelő kell a beüzemeléshez?",
        "fa2": "Nem: kinyitja a dobozt, csatlakoztatja a kábeleket, és kb. 60 másodperc alatt kész. A teljes készlet benne van.",
        "fq3": "Kioldja otthon a biztosítékokat?",
        "fa3": "Nem. Az IGBT inverter technológia hirtelen csúcsok nélkül kezeli a felvételt, és normál 220V-os konnektorról működik.",
        "fq4": "Kezdőknek is alkalmas?",
        "fa4": "Igen. A Hot Start, Anti-Stick, Arc Force és az automatikus áramszabályozás segít tiszta varratot kapni már az első használattól.",
        "fq5": "Visszaküldhetem, ha nem tetszik?",
        "fa5": "30 napos visszaküldési joga van teljes visszatérítéssel, plusz 4 év garancia és ügyfélszolgálat.",
        "fq6": "Mennyibe kerül a szállítás, és mennyi ideig tart?",
        "fa6": "A szállítás <strong>ingyenes</strong> {country}. A rendelést 24 órán belül feldolgozzuk; a futár 24/48 munkanapon belül megérkezik.",
        "lang_label": "magyarul",
    },
    "cz": {
        "title": "Kemppi™ — Přenosná svářečka 8 v 1 MIG TIG elektroda | -60%",
        "description": "Kemppi™: přenosná svářečka 8 v 1 (MIG, TIG, elektroda, řezání) až 200A a 5 mm. Kompletní sada v balení, platba na dobírku v Česku.",
        "topbar": "🔥 SLEVA 60 % + DOPRAVA ZDARMA — PLATBA NA DOBÍRKU 🔥",
        "rating": "<strong>4,8/5</strong> — Na základě <strong>3.842</strong> ověřených recenzí",
        "gift": "🎁 ZDARMA: SADA PŘÍSLUŠENSTVÍ + RUKAVICE",
        "h1": "Nekupujte 8 různých přístrojů.<br>Stačí jeden: <span class=\"hl\">Kemppi™</span>",
        "lead": "Jedním přístrojem svaříte téměř každý materiál: <strong>MIG, TIG, elektroda a řezání</strong> — ocel, nerez a litina až do <strong>5 mm</strong>. Kompaktní, výkonná a připravená k použití, s kompletní sadou příslušenství.",
        "alt_hero": "Kemppi přenosná svářečka 8 v 1",
        "cta": "ANO, CHCI Kemppi™ →",
        "form_note": "🔒 Bez zálohy · Bez karty · Platíte až při převzetí",
        "f1_h": "8 funkcí v 1",
        "f1_p": "MIG · TIG · elektroda · řezání",
        "f2_h": "Skutečný výkon 200A",
        "f2_p": "Svařování až do 5 mm tloušťky",
        "f3_h": "Kompletní sada v ceně",
        "f3_p": "Maska, rukavice, elektrody a kabely",
        "f4_h": "Platba na dobírku",
        "f4_p": "Pohodlně, bezpečně, bez zálohy",
        "countdown": "⏰ Sleva 60 % vyprší za",
        "stock_l": "Dostupnost skladem",
        "stock_r": "Zbývají pouze 4 ks",
        "live": "<strong>{n} lidí</strong> právě prohlíží Kemppi",
        "live0": "<strong>41 lidí</strong> právě prohlíží Kemppi",
        "form_h2": "Dokončete objednávku",
        "form_p": "Vyplňte formulář: náš tým vás kontaktuje pro potvrzení podrobností.",
        "label_name": "Jméno a příjmení*",
        "label_phone": "Telefonní číslo*",
        "label_addr": "Doručovací adresa*",
        "ph_name": "Jan Novák",
        "ph_phone": "+420 601 123 456",
        "ph_addr": "Ulice 10, 110 00 Praha",
        "btn": "ANO, CHCI Kemppi™",
        "ey1": "01 — Systém vše v jednom",
        "h3_1": "8 funkcí v jednom přístroji — bez kompromisů",
        "tag1a": "MIG",
        "tag1b": "TIG Lift DC",
        "tag1c": "MMA",
        "tag1d": "Řezání",
        "p1": "Svařování MIG bez plynu, TIG Lift DC, MMA elektrodou, bodové svařování a řezání — vše, co nabízí profesionální dílna, v jednom kompaktním přístroji. <strong>Nemusíte kupovat nic dalšího.</strong>",
        "i1": "Od drobné domácí opravy po náročnější práci — vše jedním nástrojem.",
        "alt_d1": "Kemppi 8 funkcí v jednom přístroji",
        "ey2": "02 — Profesionální výsledky hned",
        "h3_2": "Čisté svary a automatická regulace proudu",
        "tag2a": "Hot Start",
        "tag2b": "Anti-Stick",
        "tag2c": "Arc Force",
        "p2": "Díky systémům Hot Start, Anti-Stick a Arc Force zůstává oblouk stabilní, i když jste nikdy nedrželi elektrodu. Zvolíte materiál a tloušťku: <strong>Kemppi™ sám nastaví napětí a ampéry.</strong>",
        "i2": "Konec spálených svarů a děr v plechu — čisté výsledky od prvního použití.",
        "alt_d2": "Kemppi čisté svary a automatická regulace",
        "ey3": "03 — Výkonná, ale přenosná",
        "h3_3": "Skutečný výkon 200A — funguje z domácí zásuvky",
        "tag3a": "200A",
        "tag3b": "IGBT",
        "tag3c": "220V",
        "p3": "Svařuje uhlíkovou ocel, nerez a litinu až do <strong>5 mm</strong> bez výkyvů proudu. Invertorová technologie IGBT inteligentně řídí odběr: <strong>funguje z běžné zásuvky 220V</strong>, v garáži nebo na stavbě.",
        "i3": "Váží jen několik kilo — nosíte ji jako tašku od brány domu po trubky na stavbě.",
        "alt_d3": "Kemppi přenosná svářečka do garáže a na stavbu",
        "cmp_label": "Proč se to opravdu vyplatí",
        "cmp_h2": "Samostatné svářečky vs Kemppi™",
        "th_sep": "3 samostatné stroje",
        "r1a": "Cena",
        "r1b": "≈ {sep}",
        "r1c": "{now} jednou",
        "r2a": "MIG + TIG + elektroda",
        "r2b": "Ano, ale 3 přístroje",
        "r2c": "Vše v jednom",
        "r3a": "Prostor",
        "r3b": "Zaplněná garáž",
        "r3c": "Jeden kufřík",
        "r4a": "Pro začátečníky",
        "r4b": "Nutné zkušenosti",
        "r4c": "Automatická regulace",
        "r5a": "Sada příslušenství",
        "r5b": "Často zvlášť",
        "r5c": "Maska, rukavice, elektrody v balení",
        "r6a": "Záruka",
        "r6b": "Různá",
        "r6c": "4 roky + vrácení 30 dní",
        "rev_h2": "Tisíce zákazníků ji doporučují",
        "rev_sub": "★ 4,8/5 · Ověřený nákup · Kontrolované recenze",
        "rev1_h": "Dorazila dnes, svařuje skvěle",
        "rev1_p": "«Dorazila dnes, výborně zabalená. V kufříku je opravdu vše: maska, rukavice, elektrody. Hned vyzkoušeno na konzole — svařuje skvěle. Velmi spokojen.»",
        "rev1_a": "Jan N. ✅ — Ověřený nákup",
        "rev2_h": "Ideální i pro začátečníky",
        "rev2_p": "«Používám ji v garáži na drobné práce. Lehká a snadno přenosná. S automatickou regulací jsem i jako začátečník udělal čistý svar.»",
        "rev2_a": "Petr K. ✅ — Ověřený nákup",
        "rev3_h": "Povedlo se napoprvé",
        "rev3_p": "«Použil jsem ji na vyztužení konzoly na zahradě: svar napoprvé. Robustní, vše v balení a placeno na dobírku. U mě prošla.»",
        "rev3_a": "Eva M. ✅ — Ověřený nákup",
        "kit_eye": "Co dostanete v balení",
        "kit_h2": "📦 Kompletní sada Kemppi™ 8 v 1",
        "alt_kit": "Kompletní sada Kemppi přenosná svářečka",
        "li1": "<strong>1× Svářečka Kemppi™</strong> 8 v 1 (MIG · TIG · elektroda · řezání)",
        "li2": "1× Profesionální ochranná maska",
        "li3": "1× Pár rukavic odolných vůči vysoké teplotě",
        "li4": "1× Vybraná sada elektrod",
        "li5": "1× Kvalitní svorky a kabely",
        "li6": "1× Návod v češtině + rychlý průvodce",
        "li7": "Záruka 4 roky + podpora v češtině",
        "li8": "Doprava zdarma 24/48 h po celé ČR",
        "faq_h2": "Časté otázky",
        "fq1": "Mohu zaplatit, až balík dorazí?",
        "fa1": "Ano. Platíte hotově kurýrovi při doručení, bez údajů o kartě. Sledování přes SMS a e-mail do 24–48 hodin.",
        "fq2": "Potřebuji technika k montáži?",
        "fa2": "Ne: otevřete krabici, připojíte kabely a za cca 60 sekund jste připraveni. Kompletní sada je v balení.",
        "fq3": "Vypne jističe doma?",
        "fa3": "Ne. Invertorová technologie IGBT řídí odběr bez náhlých špiček a funguje z běžné zásuvky 220V.",
        "fq4": "Hodí se i pro začátečníky?",
        "fa4": "Ano. Hot Start, Anti-Stick, Arc Force a automatická regulace proudu pomáhají k čistým svarům od prvního použití.",
        "fq5": "Mohu ji vrátit, pokud mě nepřesvědčí?",
        "fa5": "Máte 30 dní na vrácení s plnou refundací, plus 4 roky záruky a zákaznickou podporu.",
        "fq6": "Kolik stojí doprava a jak dlouho trvá?",
        "fa6": "Doručení je <strong>zdarma</strong> v {country}. Objednávku zpracujeme do 24 hodin; kurýr dorazí do 24/48 pracovních hodin.",
        "lang_label": "češtině",
    },
    "sk": {
        "title": "Kemppi™ — Prenosná zváračka 8 v 1 MIG TIG elektróda | -60%",
        "description": "Kemppi™: prenosná zváračka 8 v 1 (MIG, TIG, elektróda, rezanie) až 200A a 5 mm. Kompletná sada v balení, platba na dobierku na Slovensku.",
        "topbar": "🔥 ZĽAVA 60 % + DOPRAVA ZADARMO — PLATBA NA DOBIERKU 🔥",
        "rating": "<strong>4,8/5</strong> — Na základe <strong>3.842</strong> overených recenzií",
        "gift": "🎁 ZADARMO: SADA PRÍSLUŠENSTVA + RUKAVICE",
        "h1": "Nekupujte 8 rôznych prístrojov.<br>Stačí jeden: <span class=\"hl\">Kemppi™</span>",
        "lead": "Jedným prístrojom zvárate takmer každý materiál: <strong>MIG, TIG, elektróda a rezanie</strong> — oceľ, nerez a liatina až do <strong>5 mm</strong>. Kompaktná, výkonná a pripravená na použitie, s kompletnou sadou príslušenstva.",
        "alt_hero": "Kemppi prenosná zváračka 8 v 1",
        "cta": "ÁNO, CHCEM Kemppi™ →",
        "form_note": "🔒 Bez zálohy · Bez karty · Platíte až pri prevzatí",
        "f1_h": "8 funkcií v 1",
        "f1_p": "MIG · TIG · elektróda · rezanie",
        "f2_h": "Skutočný výkon 200A",
        "f2_p": "Zváranie až do 5 mm hrúbky",
        "f3_h": "Kompletná sada v cene",
        "f3_p": "Maska, rukavice, elektródy a káble",
        "f4_h": "Platba na dobierku",
        "f4_p": "Pohodlne, bezpečne, bez zálohy",
        "countdown": "⏰ Zľava 60 % vyprší o",
        "stock_l": "Dostupnosť na sklade",
        "stock_r": "Zostávajú len 4 ks",
        "live": "<strong>{n} ľudí</strong> práve pozerá Kemppi",
        "live0": "<strong>41 ľudí</strong> práve pozerá Kemppi",
        "form_h2": "Dokončite objednávku",
        "form_p": "Vyplňte formulár: náš tím vás kontaktuje na potvrdenie podrobností.",
        "label_name": "Meno a priezvisko*",
        "label_phone": "Telefónne číslo*",
        "label_addr": "Doručovacia adresa*",
        "ph_name": "Martin Horváth",
        "ph_phone": "+421 901 123 456",
        "ph_addr": "Ulica 10, 811 01 Bratislava",
        "btn": "ÁNO, CHCEM Kemppi™",
        "ey1": "01 — Systém všetko v jednom",
        "h3_1": "8 funkcií v jednom prístroji — bez kompromisov",
        "tag1a": "MIG",
        "tag1b": "TIG Lift DC",
        "tag1c": "MMA",
        "tag1d": "Rezanie",
        "p1": "Zváranie MIG bez plynu, TIG Lift DC, MMA elektródou, bodové zváranie a rezanie — všetko, čo ponúka profesionálna dielňa, v jednom kompaktnom prístroji. <strong>Nemusíte kupovať nič ďalšie.</strong>",
        "i1": "Od drobnej domácej opravy po náročnejšiu prácu — všetko jedným nástrojom.",
        "alt_d1": "Kemppi 8 funkcií v jednom prístroji",
        "ey2": "02 — Profesionálne výsledky hneď",
        "h3_2": "Čisté zvary a automatická regulácia prúdu",
        "tag2a": "Hot Start",
        "tag2b": "Anti-Stick",
        "tag2c": "Arc Force",
        "p2": "Vďaka systémom Hot Start, Anti-Stick a Arc Force zostáva oblúk stabilný, aj keď ste nikdy nedržali elektródu. Zvolíte materiál a hrúbku: <strong>Kemppi™ sám nastaví napätie a ampére.</strong>",
        "i2": "Koniec spálených zvarov a dier v plechu — čisté výsledky od prvého použitia.",
        "alt_d2": "Kemppi čisté zvary a automatická regulácia",
        "ey3": "03 — Výkonná, ale prenosná",
        "h3_3": "Skutočný výkon 200A — funguje z domácej zásuvky",
        "tag3a": "200A",
        "tag3b": "IGBT",
        "tag3c": "220V",
        "p3": "Zvára uhlíkovú oceľ, nerez a liatinu až do <strong>5 mm</strong> bez výkyvov prúdu. Invertorová technológia IGBT inteligentne riadi odber: <strong>funguje z bežnej zásuvky 220V</strong>, v garáži alebo na stavbe.",
        "i3": "Váži len niekoľko kíl — nosíte ju ako tašku od brány domu po rúry na stavbe.",
        "alt_d3": "Kemppi prenosná zváračka do garáže a na stavbu",
        "cmp_label": "Prečo sa to naozaj oplatí",
        "cmp_h2": "Samostatné zváračky vs Kemppi™",
        "th_sep": "3 samostatné stroje",
        "r1a": "Cena",
        "r1b": "≈ {sep}",
        "r1c": "{now} raz",
        "r2a": "MIG + TIG + elektróda",
        "r2b": "Áno, ale 3 prístroje",
        "r2c": "Všetko v jednom",
        "r3a": "Priestor",
        "r3b": "Zapĺňa garáž",
        "r3c": "Jeden kufrík",
        "r4a": "Pre začiatočníkov",
        "r4b": "Potrebné skúsenosti",
        "r4c": "Automatická regulácia",
        "r5a": "Sada príslušenstva",
        "r5b": "Často zvlášť",
        "r5c": "Maska, rukavice, elektródy v balení",
        "r6a": "Záruka",
        "r6b": "Rôzna",
        "r6c": "4 roky + vrátenie 30 dní",
        "rev_h2": "Tisíce zákazníkov ju odporúčajú",
        "rev_sub": "★ 4,8/5 · Overený nákup · Skontrolované recenzie",
        "rev1_h": "Prišla dnes, zvárá skvele",
        "rev1_p": "«Prišla dnes, výborne zabalená. V kufríku je naozaj všetko: maska, rukavice, elektródy. Hneď vyskúšané na konzole — zvárá skvele. Veľmi spokojný.»",
        "rev1_a": "Martin K. ✅ — Overený nákup",
        "rev2_h": "Ideálna aj pre začiatočníkov",
        "rev2_p": "«Používam ju v garáži na drobné práce. Ľahká a pohodlná na prenášanie. S automatickou reguláciou som aj ako začiatočník urobil čistý zvar.»",
        "rev2_a": "Juraj H. ✅ — Overený nákup",
        "rev3_h": "Podarilo sa na prvý pokus",
        "rev3_p": "«Použil som ju na spevnenie konzoly v záhrade: zvar na prvý pokus. Robustná, všetko v balení a platené na dobierku. U mňa prešla.»",
        "rev3_a": "Zuzana M. ✅ — Overený nákup",
        "kit_eye": "Čo dostanete v balení",
        "kit_h2": "📦 Kompletná sada Kemppi™ 8 v 1",
        "alt_kit": "Kompletná sada Kemppi prenosná zváračka",
        "li1": "<strong>1× Zváračka Kemppi™</strong> 8 v 1 (MIG · TIG · elektróda · rezanie)",
        "li2": "1× Profesionálna ochranná maska",
        "li3": "1× Pár rukavíc odolných voči vysokej teplote",
        "li4": "1× Vybraná sada elektród",
        "li5": "1× Kvalitné svorky a káble",
        "li6": "1× Návod v slovenčine + rýchly sprievodca",
        "li7": "Záruka 4 roky + podpora v slovenčine",
        "li8": "Doprava zadarmo 24/48 h po celom Slovensku",
        "faq_h2": "Časté otázky",
        "fq1": "Môžem zaplatiť, keď balík dorazí?",
        "fa1": "Áno. Platíte hotovosť kuriérovi pri doručení, bez údajov o karte. Sledovanie cez SMS a e-mail do 24–48 hodín.",
        "fq2": "Potrebujem technika na montáž?",
        "fa2": "Nie: otvoríte krabicu, pripojíte káble a za cca 60 sekúnd ste pripravení. Kompletná sada je v balení.",
        "fq3": "Vypne poistky doma?",
        "fa3": "Nie. Invertorová technológia IGBT riadi odber bez náhlych špičiek a funguje z bežnej zásuvky 220V.",
        "fq4": "Hodí sa aj pre začiatočníkov?",
        "fa4": "Áno. Hot Start, Anti-Stick, Arc Force a automatická regulácia prúdu pomáhajú k čistým zvarom od prvého použitia.",
        "fq5": "Môžem ju vrátiť, ak ma nepresvedčí?",
        "fa5": "Máte 30 dní na vrátenie s plnou refundáciou, plus 4 roky záruky a zákaznícku podporu.",
        "fq6": "Koľko stojí doprava a ako dlho trvá?",
        "fa6": "Doručenie je <strong>zadarmo</strong> v {country}. Objednávku spracujeme do 24 hodín; kuriér dorazí do 24/48 pracovných hodín.",
        "lang_label": "slovenčine",
    },
}


INDEX_TMPL = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<title>Redirect…</title>
<script>
(function () {{
  var path = '/{geo}/{slug}/landing.html';
  window.location.replace(path + window.location.search + window.location.hash);
}})();
</script>
<meta http-equiv="refresh" content="0;url=/{geo}/{slug}/landing.html">
<link rel="canonical" href="https://gadgetroomhub.com/{geo}/{slug}/landing.html">
</head>
<body>
<p><a href="/{geo}/{slug}/landing.html">Kemppi™</a></p>
</body>
</html>
"""


LANDING_TMPL = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=AW-18421446541"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', 'AW-18421446541');
  gtag('config', 'AW-18360728507');
</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="contact" content="info@gadgetroomhub.com">
<meta name="theme-color" content="#14181f">
<link rel="canonical" href="https://gadgetroomhub.com/{geo}/{slug}/landing.html">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/glacierair-landing.css">
<script>
window.SITE_CONFIG = {{
  GEO: '{geo}',
  PRODUCT_SLUG: '{slug}',
  CURRENCY: '{currency}',
  PRICE: {price_num},
  OFFER_NAME: 'Kemppi {offer}',
  LP_ID: '{geo}-{offer}',
  FORM_ENDPOINT: 'https://TODO-network-endpoint.com/api/lead',
  SUBMITTING_LABEL: '{submitting}',
  COOKIE_TEXT: '{cookie_text}',
  COOKIE_ACCEPT: '{cookie_accept}',
  COOKIE_LEARN: '{cookie_learn}'
}};
</script>
<script src="/assets/js/tracking.js" defer></script>
<script src="/assets/js/form-handler.js" defer></script>
</head>
<body>

<div class="topbar">{topbar}</div>

<div class="rating-strip wrap">
  <div class="stars">★★★★★</div>
  <div class="rating-text">{rating}</div>
</div>

<section class="hero wrap">
  <div class="hero-copy">
    <span class="gift-strip">{gift}</span>
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
    <div class="hero-image hero-image-mobile-only">
      <img decoding="async" src="/assets/img/products/kemppi/hero.png?v=1" alt="{alt_hero}" width="560" height="560" loading="eager" fetchpriority="high">
    </div>
    <div class="price-block">
      <span class="was">{was}</span>
      <span class="now">{now}</span>
      <span class="pct">-60%</span>
    </div>
    <a href="#order-form" class="cta-btn">{cta}</a>
    <p class="form-note">{form_note}</p>
  </div>
  <div class="hero-image hero-image-desktop-only">
    <img decoding="async" src="/assets/img/products/kemppi/hero.png?v=1" alt="{alt_hero}" width="560" height="560" loading="eager" fetchpriority="high">
  </div>
</section>

<div class="wrap">
  <div class="feature-row">
    <div class="feature-item"><div class="ico">⚡</div><h4>{f1_h}</h4><p>{f1_p}</p></div>
    <div class="feature-item"><div class="ico">🔥</div><h4>{f2_h}</h4><p>{f2_p}</p></div>
    <div class="feature-item"><div class="ico">🧰</div><h4>{f3_h}</h4><p>{f3_p}</p></div>
    <div class="feature-item"><div class="ico">💳</div><h4>{f4_h}</h4><p>{f4_p}</p></div>
  </div>
</div>

<section class="order-section" id="order-form">
  <div class="wrap">
    <div class="urgency-strip">
      <div class="countdown-row">
        <div class="countdown-label">{countdown}</div>
        <div class="countdown-timer" id="countdownTimer">
          <div class="box"><div class="num" id="cd-h">00</div><div class="lbl">{hours}</div></div>
          <div class="sep">:</div>
          <div class="box"><div class="num" id="cd-m">14</div><div class="lbl">{mins}</div></div>
          <div class="sep">:</div>
          <div class="box"><div class="num" id="cd-s">59</div><div class="lbl">{secs}</div></div>
        </div>
      </div>
      <div class="stock-row">
        <div class="stock-label"><span class="left">{stock_l}</span><span class="right">{stock_r}</span></div>
        <div class="stock-bar"><div class="stock-bar-fill"></div></div>
      </div>
      <div class="live-row">
        <span class="dot"></span>
        <span id="liveCount" data-live="{live}">{live0}</span>
      </div>
    </div>

    <div class="order-card">
      <h2>{form_h2}</h2>
      <p>{form_p}</p>
      <form class="tm-order-form order-form cod-form" novalidate>
        <div class="cod-form__field">
          <label for="name">{label_name}</label>
          <input class="cod-form__input" id="name" type="text" name="name" autocomplete="name" placeholder="{ph_name}" required minlength="3">
        </div>
        <div class="cod-form__field">
          <label for="phone">{label_phone}</label>
          <input class="cod-form__input" id="phone" type="tel" name="phone" autocomplete="tel" placeholder="{ph_phone}" required>
        </div>
        <div class="cod-form__field">
          <label for="address">{label_addr}</label>
          <input class="cod-form__input" id="address" type="text" name="address" autocomplete="street-address" placeholder="{ph_addr}" required minlength="10">
        </div>
        <div style="margin-top: 10px; text-align: center">
          <button name="submit" type="submit">{btn}</button>
        </div>
        <p class="form-note">{form_note}</p>
      </form>
    </div>
  </div>
</section>

<section class="why-block wrap">
  <div class="why-grid">
    <div class="why-img"><img decoding="async" src="/assets/img/products/kemppi/desc-1.png?v=1" alt="{alt_d1}" loading="lazy"></div>
    <div>
      <div class="num-eyebrow">{ey1}</div>
      <h3>{h3_1}</h3>
      <div class="tag-row"><span class="tag">{tag1a}</span><span class="tag">{tag1b}</span><span class="tag">{tag1c}</span><span class="tag">{tag1d}</span></div>
      <p>{p1}</p>
      <p class="italic">{i1}</p>
    </div>
  </div>
</section>

<section class="why-block wrap">
  <div class="why-grid">
    <div class="why-img"><img decoding="async" src="/assets/img/products/kemppi/desc-2.png?v=1" alt="{alt_d2}" loading="lazy"></div>
    <div>
      <div class="num-eyebrow">{ey2}</div>
      <h3>{h3_2}</h3>
      <div class="tag-row"><span class="tag">{tag2a}</span><span class="tag">{tag2b}</span><span class="tag">{tag2c}</span></div>
      <p>{p2}</p>
      <p class="italic">{i2}</p>
    </div>
  </div>
</section>

<section class="why-block wrap" style="border-bottom:none;">
  <div class="why-grid">
    <div class="why-img"><img decoding="async" src="/assets/img/products/kemppi/desc-3.png?v=2" alt="{alt_d3}" loading="lazy"></div>
    <div>
      <div class="num-eyebrow">{ey3}</div>
      <h3>{h3_3}</h3>
      <div class="tag-row"><span class="tag">{tag3a}</span><span class="tag">{tag3b}</span><span class="tag">{tag3c}</span></div>
      <p>{p3}</p>
      <p class="italic">{i3}</p>
    </div>
  </div>
</section>

<section class="compare wrap">
  <div class="section-label">{cmp_label}</div>
  <h2>{cmp_h2}</h2>
  <table>
    <tr><th></th><th>{th_sep}</th><th class="highlight">Kemppi™</th></tr>
    <tr><td>{r1a}</td><td>{r1b}</td><td class="win">{r1c}</td></tr>
    <tr><td>{r2a}</td><td>{r2b}</td><td class="win">{r2c}</td></tr>
    <tr><td>{r3a}</td><td>{r3b}</td><td class="win">{r3c}</td></tr>
    <tr><td>{r4a}</td><td>{r4b}</td><td class="win">{r4c}</td></tr>
    <tr><td>{r5a}</td><td>{r5b}</td><td class="win">{r5c}</td></tr>
    <tr><td>{r6a}</td><td>{r6b}</td><td class="win">{r6c}</td></tr>
  </table>
</section>

<section class="testimonials">
  <div class="wrap">
    <div class="section-heading">
      <h2>{rev_h2}</h2>
      <span class="eyebrow" style="display:block;margin-top:8px;color:#5b6472;font-weight:600;text-transform:none;letter-spacing:0;font-size:14px;">{rev_sub}</span>
    </div>
    <div class="t-grid">
      <div class="testimonial">
        <img decoding="async" class="t-photo" src="/assets/img/reviews/kemppi/review-1.png?v=1" alt="{rev1_a}" loading="lazy">
        <div class="t-body">
          <div class="stars">★★★★★</div>
          <h4>{rev1_h}</h4>
          <p>{rev1_p}</p>
          <div class="author-row"><div class="author">{rev1_a}</div></div>
        </div>
      </div>
      <div class="testimonial">
        <img decoding="async" class="t-photo" src="/assets/img/reviews/kemppi/review-2.png?v=1" alt="{rev2_a}" loading="lazy">
        <div class="t-body">
          <div class="stars">★★★★★</div>
          <h4>{rev2_h}</h4>
          <p>{rev2_p}</p>
          <div class="author-row"><div class="author">{rev2_a}</div></div>
        </div>
      </div>
      <div class="testimonial">
        <img decoding="async" class="t-photo" src="/assets/img/reviews/kemppi/review-3.png?v=1" alt="{rev3_a}" loading="lazy">
        <div class="t-body">
          <div class="stars">★★★★★</div>
          <h4>{rev3_h}</h4>
          <p>{rev3_p}</p>
          <div class="author-row"><div class="author">{rev3_a}</div></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="kit-section wrap">
  <div class="section-heading">
    <span class="eyebrow">{kit_eye}</span>
    <h2>{kit_h2}</h2>
  </div>
  <div class="kit-box">
    <img decoding="async" src="/assets/img/products/kemppi/kit.png?v=1" alt="{alt_kit}" loading="lazy">
    <div class="kit-content">
      <div class="price-block" style="margin-bottom:16px;">
        <span class="was">{was}</span>
        <span class="now">{now}</span>
        <span class="pct">-60%</span>
      </div>
      <ul>
        <li>{li1}</li>
        <li>{li2}</li>
        <li>{li3}</li>
        <li>{li4}</li>
        <li>{li5}</li>
        <li>{li6}</li>
        <li>{li7}</li>
        <li>{li8}</li>
      </ul>
      <a href="#order-form" class="cta-btn">{cta}</a>
    </div>
  </div>
</section>

<section class="faq wrap">
  <div class="section-heading">
    <h2>{faq_h2}</h2>
  </div>
  <div class="faq-item"><button class="faq-q" type="button"><span>{fq1}</span><span class="arrow">▾</span></button>
    <div class="faq-a"><p>{fa1}</p></div></div>
  <div class="faq-item"><button class="faq-q" type="button"><span>{fq2}</span><span class="arrow">▾</span></button>
    <div class="faq-a"><p>{fa2}</p></div></div>
  <div class="faq-item"><button class="faq-q" type="button"><span>{fq3}</span><span class="arrow">▾</span></button>
    <div class="faq-a"><p>{fa3}</p></div></div>
  <div class="faq-item"><button class="faq-q" type="button"><span>{fq4}</span><span class="arrow">▾</span></button>
    <div class="faq-a"><p>{fa4}</p></div></div>
  <div class="faq-item"><button class="faq-q" type="button"><span>{fq5}</span><span class="arrow">▾</span></button>
    <div class="faq-a"><p>{fa5}</p></div></div>
  <div class="faq-item"><button class="faq-q" type="button"><span>{fq6}</span><span class="arrow">▾</span></button>
    <div class="faq-a"><p>{fa6}</p></div></div>
</section>

<footer class="site-footer">
  <div class="container">
    <div class="site-footer__grid">
      <div>
        <a href="/" class="site-logo" aria-label="gadgetroomhub.com home">
          <span class="site-logo__text"><span class="site-logo__text-primary">gadgetroomhub</span><span class="site-logo__text-accent">.com</span></span>
        </a>
        <p class="site-footer__blurb">{footer_blurb}</p>
      </div>
      <div>
        <h4 class="site-footer__heading">{info}</h4>
        <ul class="site-footer__list">
          <li><a href="/{geo}/about-us.html">{about}</a></li>
          <li><a href="/{geo}/contact-us.html">{contact}</a></li>
          <li><a href="/{geo}/privacy-policy.html">{privacy}</a></li>
          <li><a href="/{geo}/terms-conditions.html">{terms}</a></li>
          <li><a href="/{geo}/cookie-policy.html">{cookie}</a></li>
          <li><a href="/{geo}/shipping-policy.html">{ship}</a></li>
          <li><a href="/{geo}/refund-policy.html">{refund}</a></li>
        </ul>
      </div>
      <div>
        <h4 class="site-footer__heading">{contacts}</h4>
        <ul class="site-footer__list">
          <li><strong>WHATECH MOBILE CO., LIMITED</strong></li>
          <li>Room 505, 5th floor, Beverley Commercial Centre</li>
          <li>87-105 Chatham Road South, Hong Kong</li>
          <li><a href="mailto:info@gadgetroomhub.com">info@gadgetroomhub.com</a></li>
        </ul>
      </div>
    </div>
    <div class="site-footer__bottom">
      © <span data-year>2026</span> <strong>WHATECH MOBILE CO., LIMITED</strong> — {rights}.
      <a href="/">gadgetroomhub.com</a>
    </div>
  </div>
</footer>

<script src="/assets/js/glacierair-landing.js" defer></script>
<script>
  document.querySelectorAll('[data-year]').forEach(function (el) {{
    el.textContent = String(new Date().getFullYear());
  }});
</script>
</body>
</html>
"""


def esc_js(s: str) -> str:
    return s.replace("\\", "\\\\").replace("'", "\\'")


def render_landing(offer: str, cfg: dict, copy: dict, shared: dict) -> str:
    was = fmt_price(was_price(cfg["price"]), cfg["currency"])
    now = fmt_price(cfg["price"], cfg["currency"])
    sep = fmt_price(round(cfg["price"] * 4.4, 2), cfg["currency"])
    ctx = dict(copy)
    ctx.update(
        {
            k: shared[k]
            for k in (
                "about",
                "contact",
                "privacy",
                "terms",
                "cookie",
                "ship",
                "refund",
                "info",
                "contacts",
                "rights",
                "footer_blurb",
                "hours",
                "mins",
                "secs",
                "submitting",
                "cookie_text",
                "cookie_accept",
                "cookie_learn",
            )
        }
    )
    for k in ("submitting", "cookie_text", "cookie_accept", "cookie_learn"):
        ctx[k] = esc_js(ctx[k])
    ctx["r1b"] = copy["r1b"].format(sep=sep)
    ctx["r1c"] = copy["r1c"].format(now=now)
    ctx["fa6"] = copy["fa6"].format(country=cfg["country"])
    ctx.update(
        {
            "lang": cfg["lang"],
            "geo": cfg["geo"],
            "slug": cfg["slug"],
            "offer": offer,
            "currency": cfg["currency"],
            "price_num": cfg["price"],
            "was": was,
            "now": now,
        }
    )
    return LANDING_TMPL.format(**ctx)


def render_thank_you(offer: str, cfg: dict, copy: dict, shared: dict, it_ty: str) -> str:
    geo = cfg["geo"]
    slug = cfg["slug"]
    html = it_ty
    html = html.replace('lang="it"', f'lang="{cfg["lang"]}"', 1)
    html = re.sub(r"GEO:\s*'[^']*'", f"GEO: '{geo}'", html)
    html = re.sub(r"PRODUCT_SLUG:\s*'[^']*'", f"PRODUCT_SLUG: '{slug}'", html)
    html = re.sub(r"CURRENCY:\s*'[^']*'", f"CURRENCY: '{cfg['currency']}'", html)
    html = re.sub(r"PRICE:\s*[0-9.]+", f"PRICE: {cfg['price']}", html)
    html = re.sub(
        r"trackPurchase\([0-9.]+,\s*'[^']*'\)",
        f"trackPurchase({cfg['price']}, '{cfg['currency']}')",
        html,
    )
    html = re.sub(
        r"COOKIE_TEXT:\s*'[^']*',\s*\n\s*COOKIE_ACCEPT:\s*'[^']*',\s*\n\s*COOKIE_LEARN:\s*'[^']*'",
        f"COOKIE_TEXT: '{esc_js(shared['cookie_text'])}',\n  COOKIE_ACCEPT: '{esc_js(shared['cookie_accept'])}',\n  COOKIE_LEARN: '{esc_js(shared['cookie_learn'])}'",
        html,
    )
    ty_title = shared["ty_title"].replace("GlacierAir™", "Kemppi™")
    html = re.sub(r"<title>.*?</title>", f"<title>{ty_title}</title>", html, count=1)
    ty_desc = shared.get("ty_desc", "").replace("GlacierAir™", "Kemppi™")
    if ty_desc:
        html = re.sub(
            r'<meta name="description" content=".*?"\s*/?>',
            f'<meta name="description" content="{ty_desc}">',
            html,
            count=1,
        )
    html = html.replace("Il tuo ordine è stato registrato con successo!", shared["ty_h1"])
    html = html.replace(
        "Perfetto — il tuo ordine è in elaborazione. Manca solo <strong>un ultimo passaggio</strong> per completarlo e far partire la spedizione.",
        shared["ty_sub"],
    )
    html = html.replace(
        "Il team gadgetroomhub al lavoro: call center e logistica COD", shared["ty_alt"]
    )
    html = html.replace("👇 Cosa devi fare adesso", shared["ty_eyebrow"])
    html = html.replace("📞 Rispondi alla chiamata di conferma", shared["ty_action_title"])
    html = html.replace(
        "Un nostro operatore ti contatterà <strong>nelle prossime ore</strong> per confermare il tuo ordine.",
        shared["ty_action_body"],
    )
    html = html.replace(
        "Se non rispondi alla chiamata, l'ordine verrà automaticamente annullato.",
        shared["ty_action_warn"],
    )
    html = html.replace("🕒 Orari di contatto", shared["ty_hours_h"])
    html = html.replace("<strong>Lunedì – Sabato</strong> · 9:00 – 18:00", shared["ty_hours"])
    html = html.replace("📋 Cosa succede dopo", shared["ty_next_h"])
    it_steps = [
        "Rispondi alla chiamata e <strong>conferma i tuoi dati</strong>",
        "Il tuo ordine verrà spedito entro <strong>24–48 ore</strong>",
        "Consegna a domicilio e <strong>pagamento alla consegna</strong>",
    ]
    for ii, li in zip(it_steps, shared["ty_steps"]):
        html = html.replace(f"<li>{ii}</li>", f"<li>{li}</li>")
    badge2 = shared["ty_badges"][1]
    for old, new in (
        ("24 mesi", "4 anni"),
        ("24 Monate", "4 Jahre"),
        ("24 meses", "4 años"),
        ("24 months", "4 years"),
        ("24 hónap", "4 év"),
        ("24 miesiące", "4 lata"),
        ("24 mesece", "4 leta"),
        ("24 meseci", "4 leta"),
        ("24 luni", "4 ani"),
        ("24 měsíců", "4 roky"),
        ("24 mesiacov", "4 roky"),
    ):
        if old in badge2:
            badge2 = badge2.replace(old, new)
            break
    html = html.replace("🔒 Pagamento alla consegna", shared["ty_badges"][0])
    html = html.replace("🛡️ Garanzia 4 anni", badge2)
    html = html.replace("🔐 Protezione SSL", shared["ty_badges"][2])

    footer_it = (
        "    <div>\n"
        '      <h4 class="site-footer__heading">Informazioni</h4>\n'
        '      <ul class="site-footer__list">\n'
        '        <li><a href="/it/about-us.html">Chi siamo</a></li>\n'
        '        <li><a href="/it/contact-us.html">Contattaci</a></li>\n'
        '        <li><a href="/it/privacy-policy.html">Privacy Policy</a></li>\n'
        '        <li><a href="/it/terms-conditions.html">Termini e Condizioni</a></li>\n'
        '        <li><a href="/it/cookie-policy.html">Cookie Policy</a></li>\n'
        '        <li><a href="/it/shipping-policy.html">Politica di Spedizione</a></li>\n'
        '        <li><a href="/it/refund-policy.html">Politica di Rimborso</a></li>\n'
        "      </ul>\n"
        "    </div>\n"
        "    <div>\n"
        '      <h4 class="site-footer__heading">Contatti</h4>'
    )
    # IT kemppi thank-you uses slightly different shipping/refund labels
    footer_it_alt = footer_it.replace("Politica di Spedizione", "Politica di spedizione").replace(
        "Politica di Rimborso", "Politica di reso"
    )
    footer_geo = (
        "    <div>\n"
        f'      <h4 class="site-footer__heading">{shared["info"]}</h4>\n'
        '      <ul class="site-footer__list">\n'
        f'        <li><a href="/{geo}/about-us.html">{shared["about"]}</a></li>\n'
        f'        <li><a href="/{geo}/contact-us.html">{shared["contact"]}</a></li>\n'
        f'        <li><a href="/{geo}/privacy-policy.html">{shared["privacy"]}</a></li>\n'
        f'        <li><a href="/{geo}/terms-conditions.html">{shared["terms"]}</a></li>\n'
        f'        <li><a href="/{geo}/cookie-policy.html">{shared["cookie"]}</a></li>\n'
        f'        <li><a href="/{geo}/shipping-policy.html">{shared["ship"]}</a></li>\n'
        f'        <li><a href="/{geo}/refund-policy.html">{shared["refund"]}</a></li>\n'
        "      </ul>\n"
        "    </div>\n"
        "    <div>\n"
        f'      <h4 class="site-footer__heading">{shared["contacts"]}</h4>'
    )
    if footer_it in html:
        html = html.replace(footer_it, footer_geo)
    elif footer_it_alt in html:
        html = html.replace(footer_it_alt, footer_geo)
    else:
        html = html.replace("/it/", f"/{geo}/")
    html = html.replace("Tutti i diritti riservati.", shared["rights"] + ".")
    html = html.replace("/it/", f"/{geo}/")
    html = re.sub(r"'value':\s*[0-9.]+", f"'value': {cfg['cpa']}", html)
    html = re.sub(
        r"<!-- Google Ads Purchase conversion[^>]*>",
        f"<!-- Google Ads Purchase conversion — value = CPA/CPL EUR for offer #{offer} -->",
        html,
    )
    return html


def update_sitemap() -> None:
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    entries = []
    for offer, cfg in GEOS.items():
        geo = cfg["geo"]
        slug = cfg["slug"]
        for loc in (f"https://gadgetroomhub.com/{geo}/{slug}/", f"https://gadgetroomhub.com/{geo}/{slug}/landing.html"):
            line = f'  <url><loc>{loc}</loc><lastmod>2026-08-11</lastmod><changefreq>weekly</changefreq><priority>0.95</priority></url>\n'
            if loc not in text:
                entries.append(line)
    if not entries:
        return
    marker = '  <url><loc>https://gadgetroomhub.com/en/kemppi/landing.html</loc><lastmod>2026-08-11</lastmod><changefreq>weekly</changefreq><priority>0.95</priority></url>\n'
    if marker in text:
        text = text.replace(marker, marker + "".join(entries))
    else:
        text = text.replace(
            "</urlset>",
            "".join(entries) + "</urlset>",
        )
    path.write_text(text, encoding="utf-8")
    print(f"Sitemap: added {len(entries)} Kemppi geo URLs")


def main(only: set[str] | None = None) -> None:
    shared_all = load_ga_shared()
    it_ty = (ROOT / "it/kemppi/thank-you.html").read_text(encoding="utf-8")
    for offer, cfg in GEOS.items():
        if only is not None and offer not in only:
            continue
        tr_key = cfg["tr"]
        copy = COPY[tr_key]
        shared = shared_all[tr_key]
        out_dir = ROOT / cfg["geo"] / cfg["slug"]
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "landing.html").write_text(
            render_landing(offer, cfg, copy, shared), encoding="utf-8"
        )
        (out_dir / "index.html").write_text(
            INDEX_TMPL.format(lang=cfg["lang"], geo=cfg["geo"], slug=cfg["slug"]),
            encoding="utf-8",
        )
        (out_dir / "thank-you.html").write_text(
            render_thank_you(offer, cfg, copy, shared, it_ty), encoding="utf-8"
        )
        print(
            f"Wrote {cfg['geo']}/{cfg['slug']}/ (#{offer}) — {fmt_price(cfg['price'], cfg['currency'])}"
        )
    update_sitemap()


if __name__ == "__main__":
    import sys

    only = set(sys.argv[1:]) if len(sys.argv) > 1 else None
    main(only)
