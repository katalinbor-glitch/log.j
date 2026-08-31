import streamlit as st
import random

st.set_page_config(page_title="Logisztikai Tycoon: Boss Edition + Analízis", page_icon="🏢", layout="centered")

st.title("🏢 Logisztikai Tycoon: Boss Edition + Analízis")
st.markdown("Versenyezz a könyörtelen **MegaLog Corp.** ellen, elemezd a döntéseid hatásait, és tanulj a logisztikai kihívásokból!")

if "indul" not in st.session_state:
    st.session_state.indul = False
if "utolso_naplo" not in st.session_state:
    st.session_state.utolso_naplo = None

if not st.session_state.indul:
    st.markdown("### 🏢 Új Vállalat Indítása")
    ceg_nev = st.text_input("Céged neve:", "GlobalTrans Kft.")
    
    if st.button("Induljon a harc a MegaLog Corp. ellen! 🚀"):
        st.session_state.indul = True
        st.session_state.ceg_nev = ceg_nev
        st.session_state.penz = 220000
        st.session_state.rivalis_penz = 180000
        st.session_state.kor = 1
        st.session_state.soforok_szama = 1
        st.session_state.raktar_szint = 1
        st.session_state.uzemanyag_kedvezmeny = 0
        st.session_state.utolso_naplo = None
        st.rerun()

else:
    # 💰 KÖZÉPSŐ PÉNZ ÉS ÁLLAPOT KIJELZÉS
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label=f"📊 {st.session_state.ceg_nev} tőkéje", value=f"{st.session_state.penz:,} Ft")
    with col2:
        st.metric(label="🦾 MegaLog Corp. (Főellenség)", value=f"{st.session_state.rivalis_penz:,} Ft")
    with col3:
        st.metric(label="📅 Aktuális Nap", value=f"{st.session_state.kor} / 12")
    st.markdown("---")

    # 📊 LEGFELÜL: Elemzés az előző körről, ha létezik
    if st.session_state.utolso_naplo:
        with st.expander("📈 Előző fuvar részletes elemzése (Kattints a kibontáshoz)", expanded=True):
            nap = st.session_state.utolso_naplo
            st.markdown(f"**Választott feladat:** {nap['feladat']} ({nap['tav']} km)")
            st.markdown(f"**Alapbevétel:** {nap['alap_bev']:,} Ft | **Incoterm szorzó:** {nap['incoterm_nev']}")
            
            st.markdown("#### Költségek és Tényezők bontása:")
            st.write(f"- Jármű(vek) útiköltsége: **-{nap['ossz_ut_koltseg']:,} Ft**")
            if nap['esemeny_koltseg'] > 0:
                st.write(f"- Váratlan esemény hatása: **-{nap['esemeny_koltseg']:,} Ft** ({nap['esemeny_uzenet']})")
            if nap['extra_birsag'] > 0:
                st.write(f"- Gyorshajtási bírság: **-{nap['extra_birsag']:,} Ft**")
            if nap['vam_birsag'] > 0:
                st.write(f"- Vámhivatali bírság: **-{nap['vam_birsag']:,} Ft**")
            
            st.markdown(f"### Eredmény: **{nap['profit']:,} Ft**")
            st.info(nap['tanulsag'])
        st.markdown("---")

    st.sidebar.markdown(f"### ⚙️ Cégfejlesztések")
    st.sidebar.text(f"👥 Sofőrök száma: {st.session_state.soforok_szama}")
    st.sidebar.text(f"📦 Raktár szint: {st.session_state.raktar_szint}. szint")
    st.sidebar.text(f"⛽ Üzemanyag-spórolás: -{st.session_state.uzemanyag_kedvezmeny}%")

    if st.session_state.penz >= 50000 and st.sidebar.button("👥 Új sofőr felvétele (50k Ft)"):
        st.session_state.penz -= 50000
        st.session_state.soforok_szama += 1
        st.success("Új sofőr állt munkába!")
        st.rerun()

    if st.session_state.penz >= 70000 and st.sidebar.button("🏗️ Raktár bővítés (70k Ft)"):
        st.session_state.penz -= 70000
        st.session_state.raktar_szint += 1
        st.success("A raktár bővült!")
        st.rerun()

    if st.session_state.penz >= 40000 and st.sidebar.button("⚡ Üzemanyag-takarékosság (40k Ft)"):
        st.session_state.penz -= 40000
        st.session_state.uzemanyag_kedvezmeny += 15
        st.success("Üzemanyag-fejlesztés kész!")
        st.rerun()

    if st.session_state.kor <= 12:
        st.markdown(f"## 🗺️ {st.session_state.kor}. Nap: Megbízások & MegaLog Ellenséges Lépések")

        random.seed(st.session_state.kor * 999)
        
        ajanlatok_pool = [
            {"cim": "🍅 Friss mezőgazdasági export", "leírás": "Helyi gyors fuvar hűtést igénylő áruval.", "tav": 50, "ido": 1, "alap_bev": 75000},
            {"cim": "📦 Gyári alkatrészek Nyugat-Európába", "leírás": "Közúti fuvar uniós partnerhez.", "tav": 500, "ido": 2, "alap_bev": 210000},
            {"cim": "🚢 Hatalmas tömegáru a Távol-Keletre", "leírás": "Hatalmas tengeri konténeres fuvar.", "tav": 3000, "ido": 4, "alap_bev": 650000},
            {"cim": "⚡ Sürgős elektronikai expressz", "leírás": "Magas értékű, sürgős küldetés Ázsiába.", "tav": 3000, "ido": 2, "alap_bev": 900000}
        ]
        
        napi_ajanlatok = random.sample(ajanlatok_pool, 3)

        valasztott_index = st.radio(
            "Válaszd ki a napi fuvarfeladatot:",
            options=[0, 1, 2],
            format_func=lambda i: f"{napi_ajanlatok[i]['cim']} | Táv: {napi_ajanlatok[i]['tav']} km | Idő: {napi_ajanlatok[i]['ido']} nap | Bevétel: {napi_ajanlatok[i]['alap_bev']:,} Ft"
        )
        
        aktiv_feladat = napi_ajanlatok[valasztott_index]
        st.info(f"**Részletek:** {aktiv_feladat['leírás']} | **Menetidő:** {aktiv_feladat['ido']} nap")

        jarmuvek = {
            "🚐 Helyi Furgon (Olcsó, stabil)": {"kapacitas": 20, "koltseg_km": 35},
            "🚛 Nagy Teherautó (A győztes!)": {"kapacitas": 60, "koltseg_km": 110},
            "🚢 Konténeres Hajó (Óriási raktér)": {"kapacitas": 150, "koltseg_km": 280},
            "✈️ Cargo Repülő (Villámgyors)": {"kapacitas": 80, "koltseg_km": 650}
        }

        st.markdown("### 🚛 Járműpark Kiválasztása")
        elso_jarmu = st.selectbox("1. Elsődleges szállítóeszköz:", list(jarmuvek.keys()))
        
        masodik_jarmu_aktivalva = st.checkbox("➕ Második szállítóeszköz indítása is (Multi-fleet konvoj)")
        masodik_jarmu = None
        if masodik_jarmu_aktivalva:
            masodik_jarmu = st.selectbox("2. Másodlagos szállítóeszköz:", list(jarmuvek.keys()))

        benne_van_hajó = ("🚢" in elso_jarmu) or (masodik_jarmu and "🚢" in masodik_jarmu)

        st.markdown("### 📋 Incoterms Szakmai Klauzulák (Szűkítve az eszközhöz)")
        if benne_van_hajó:
            elerheto_klauzulak = [
                "EXW (Ex Works) - Gyári átvétel: minimális felelősség",
                "FOB (Free on Board) - Hajó fedélzetére rajtva (Kizárólag hajóhoz!)",
                "CIF (Cost, Insurance and Freight) - Költség, biztosítás és fuvardíj (Hajóhoz)",
                "DDP (Delivered Duty Paid) - Vámkezelve leszállítva"
            ]
        else:
            elerheto_klauzulak = [
                "EXW (Ex Works) - Gyári átvétel: minimális felelősség",
                "FCA (Free Carrier) - Költségmentes fuvarozónak átadva (Közúti/Légi)",
                "CPT (Carriage Paid To) - Fuvarozás fizetve rendeltetési helyig",
                "DDP (Delivered Duty Paid) - Vámkezelve leszállítva"
            ]

        incoterm = st.selectbox("Válaszd ki a szerződéses feltételt:", elerheto_klauzulak)

        mennyiseg = st.slider("Összes szállítandó árumennyiség egységben:", 1, 200, 30)
        
        st.markdown("### ⚡ Úti kockázatok & Extra opciók")
        gyorshajtas = st.checkbox("⚡ Nyomod neki a gázt? (Gyorsabb fuvar, de 25% esély traffipax bírságra)")
        idoablak = st.checkbox("⏱️ Szigorú időablakos szállítás vállalása (Pontosság esetén bónusz, hiba esetén kötbér)")

        if st.button("🚀 Konvoj indítása!", type="primary"):
            tavolsag = aktiv_feladat['tav']
            fuvar_ido = aktiv_feladat['ido']
            
            esemeny_koltseg = 0
            esemeny_uzenet = "Semmilyen váratlan akadály nem nehezítette az utat."
            esemeny_esely = random.random()
            
            if esemeny_esely < 0.35:
                esemeny_koltseg = 45000
                esemeny_uzenet = "Vad sztrájk bénította meg a határátkelőt (-45,000 Ft extra kiadás)."
                st.error(f"🚨 **Váratlan esemény:** {esemeny_uzenet}")
            elif esemeny_esely < 0.65:
                esemeny_koltseg = 60000
                esemeny_uzenet = "MegaLog Corp. szabotázs! A főellenség bérencei feltörték a rendszert (-60,000 Ft kár)."
                st.error(f"🦾 **Váratlan esemény:** {esemeny_uzenet}")
            elif esemeny_esely < 0.85:
                esemeny_koltseg = 35000
                esemeny_uzenet = "Műszaki hiba: Az egyik jármű váltója megadta magát (-35,000 Ft szerviz)."
                st.warning(f"🛠️ **Váratlan esemény:** {esemeny_uzenet}")
            else:
                st.success("✨ **Szerencsés út:** Sima út, zökkenőmentes haladás.")

            sofor_kimerult = (tavolsag >= 3000) and (random.random() < 0.25)
            if sofor_kimerult:
                st.warning("😴 A sofőrök túllépték a maximális vezetési időt! Kötelező 1 napos pihenő miatt csúszik a fuvar.")
                fuvar_ido += 1

            incoterm_szorzó = 1.0
            if "EXW" in incoterm:
                incoterm_szorzó = 0.80
            elif "FCA" in incoterm or "CPT" in incoterm or "FOB" in incoterm or "CIF" in incoterm:
                incoterm_szorzó = 1.10
            elif "DDP" in incoterm:
                incoterm_szorzó = 1.30

            j1 = jarmuvek[elso_jarmu]
            kedv_fakt = (100 - st.session_state.uzemanyag_kedvezmeny) / 100
            ut_koltseg_1 = int(tavolsag * j1['koltseg_km'] * kedv_fakt)
            kapacitas_osszes = j1['kapacitas']

            ut_koltseg_2 = 0
            if masodik_jarmu_aktivalva and masodik_jarmu:
                j2 = jarmuvek[masodik_jarmu]
                ut_koltseg_2 = int(tavolsag * j2['koltseg_km'] * kedv_fakt)
                kapacitas_osszes += j2['kapacitas']

            ossz_ut_koltseg = ut_koltseg_1 + ut_koltseg_2

            extra_birsag = 0
            if gyorshajtas and random.random() < 0.25:
                extra_birsag = 35000
                st.error("📸 Villant a traffipax! Gyorshajtási bírság: 35,000 Ft.")

            if mennyiseg > kapacitas_osszes:
                st.error(f"❌ A járművek kapacitása ({kapacitas_osszes}) kevés a rakományhoz ({mennyiseg})! A fuvar meghiúsult.")
                st.session_state.penz -= 40000
                profit = -40000
                tanulsag = "Kapacitáshiba történt: túl kevés vagy túl kicsi járművet indítottál a rengeteg áruhoz, ami súlyos kötbért eredményezett."
            else:
                raktar_szorzó = 1 + (st.session_state.raktar_szint - 1) * 0.15
                bevetel = int(aktiv_feladat['alap_bev'] * (mennyiseg / 50) * raktar_szorzó * incoterm_szorzó)
                
                if gyorshajtas and extra_birsag == 0:
                    bevetel = int(bevetel * 1.12)

                idoblak_uzenet = ""
                if idoablak:
                    if random.random() < 0.60:
                        bevetel = int(bevetel * 1.25)
                        idoblak_uzenet = " Időablak teljesítve (+25% bónusz)."
                        st.success(f"⏱️ Sikerült tartani az időablakot!{idoblak_uzenet}")
                    else:
                        bevetel = int(bevetel * 0.8)
                        idoblak_uzenet = " Időablak csúszás (kötbér levonva)."
                        st.warning(f"⚠️ Késés az időablakban!{idoblak_uzenet}")

                vám_birsag = 0
                if "DDP" in incoterm and tavolsag >= 500 and random.random() < 0.20:
                    vám_birsag = 50000
                    st.warning("⚠️ Vámhivatali akadás DDP fuvarnál! -50,000 Ft vámbírság.")

                profit = bevetel - ossz_ut_koltseg - extra_birsag - vám_birsag - esemeny_koltseg
                st.session_state.penz += profit
                
                # Tanulság szöveg generálása az elemzéshez
                tanulsag = f"A {incoterm.split(' - ')[0]} klauzula és a kiválasztott flotta kombinációja bruttó {bevetel:,} Ft bevételt hozott. "
                if profit > 0:
                    tanulsag += "Nyereséges volt a döntés, a járművek km-költségei nem ették meg a profitot."
                else:
                    tanulsag += "Ráfizetéses lett a fuvar: vagy a túl magas km-költségű jármű (pl. repülő rövid távon), vagy a váratlan események/bírságok emésztették fel a pénzt."

            # Napló mentése a következő kör eleji elemzéshez
            st.session_state.utolso_naplo = {
                "feladat": aktiv_feladat['cim'],
                "tav": tavolsag,
                "alap_bev": aktiv_feladat['alap_bev'],
                "incoterm_nev": incoterm,
                "ossz_ut_koltseg": ossz_ut_koltseg,
                "esemeny_koltseg": esemeny_koltseg,
                "esemeny_uzenet": esemeny_uzenet,
                "extra_birsag": extra_birsag,
                "vam_birsag": vám_birsag,
                "profit": profit,
                "tanulsag": tanulsag
            }

            passziv_bevetel = (st.session_state.soforok_szama - 1) * 15000 * fuvar_ido
            st.session_state.penz += passziv_bevetel

            st.session_state.rivalis_penz += random.randint(60000, 110000) * fuvar_ido
            st.session_state.kor += fuvar_ido
            st.rerun()

    else:
        st.balloons()
        st.markdown("# 🏆 Vége a 12 napos MegaLog elleni harcnak!")
        st.markdown(f"### A te céged tőkéje: **{st.session_state.penz:,} Ft**")
        st.markdown(f"### A főellenség MegaLog Corp. tőkéje: **{st.session_state.rivalis_penz:,} Ft**")

        if st.session_state.penz > st.session_state.rivalis_penz:
            st.success("🥇 Sikerült legyőznöd a MegaLog Corp.-ot! Kiváló logisztikai stratéga vagy!")
        else:
            st.error("🥈 A MegaLog Corp. könyörtelenül bedarálta a cégedet.")

        if st.button("🔄 Új játék indítása"):
            st.session_state.indul = False
            st.session_state.utolso_naplo = None
            st.rerun()
