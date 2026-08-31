import streamlit as st
import random

st.set_page_config(page_title="Logisztikai Tycoon: Extended Pro", page_icon="📈", layout="centered")

st.title("📈 Logisztikai Tycoon: Extended Pro")
st.markdown("10 napos logisztikai háború a **MegaLog Kft.** ellen! Minden nap több megbízás közül választhatsz, tervezd meg okosan a stratégiádat.")

if "indul" not in st.session_state:
    st.session_state.indul = False

if not st.session_state.indul:
    st.markdown("### 🏢 Új Vállalat Indítása")
    ceg_nev = st.text_input("Céged neve:", "MegaTrans Kft.")
    
    if st.button("Induljon a 10 napos kihívás! 🚀"):
        st.session_state.indul = True
        st.session_state.ceg_nev = ceg_nev
        st.session_state.penz = 150000
        st.session_state.rivalis_penz = 130000
        st.session_state.kor = 1
        st.session_state.soforok_szama = 1
        st.session_state.raktar_szint = 1
        st.session_state.uzemanyag_kedvezmeny = 0
        st.rerun()

else:
    st.sidebar.markdown(f"### 📊 {st.session_state.ceg_nev}")
    st.sidebar.metric(label="💰 Tőkéd", value=f"{st.session_state.penz:,} Ft")
    st.sidebar.metric(label="🤖 MegaLog Kft. tőkéje", value=f"{st.session_state.rivalis_penz:,} Ft")
    st.sidebar.metric(label="📅 Aktuális Nap", value=f"{st.session_state.kor} / 10")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🏢 Cégfejlesztések")
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

    if st.session_state.kor <= 10:
        st.markdown(f"## 🗺️ {st.session_state.kor}. Nap: Válassz a napi ajánlatok közül!")

        # Generálunk 3 eltérő fuvajánlatot erre a napra a kor alapján
        random.seed(st.session_state.kor * 123)
        
        ajanlatok_pool = [
            {"cim": "🍅 Friss zöldség a helyi piacon", "leírás": "Rövid távú, stabil helyi fuvar.", "javasolt": "🚐 Helyi Furgon (Olcsó, stabil)", "tav": 50, "alap_bev": 65000},
            {"cim": "📦 Webshop csomagok Nyugat-Európába", "leírás": "Közepes távú, megbízható európai export.", "javasolt": "🚛 Nagy Teherautó (A győztes!)", "tav": 500, "alap_bev": 180000},
            {"cim": "🏗️ Ipari acélelemek építkezésre", "leírás": "Súlyos rakomány Nyugat-Európába.", "javasolt": "🚛 Nagy Teherautó (A győztes!)", "tav": 500, "alap_bev": 220000},
            {"cim": "🚢 Tömegáru konténer a Távol-Keletre", "leírás": "Hatalmas mennyiségű olcsó áru tengeren túlra.", "javasolt": "🚢 Konténeres Hajó (Óriási raktér)", "tav": 3000, "alap_bev": 520000},
            {"cim": "💎 Luxus elektronika villámgyorsan", "leírás": "Értékes raktér a Távol-Keletre, sürgős határidővel.", "javasolt": "✈️ Cargo Repülő (Villámgyors)", "tav": 3000, "alap_bev": 780000},
            {"cim": "⚡ Sürgős gyógyszerfutár helyben", "leírás": "Nagyon gyors helyi fuvar extra prémiummal.", "javasolt": "🚐 Helyi Furgon (Olcsó, stabil)", "tav": 50, "alap_bev": 95000}
        ]
        
        # Kiválasztunk 3-at a napi kínálathoz
        napi_ajanlatok = random.sample(ajanlatok_pool, 3)

        valasztott_index = st.radio(
            "Válaszd ki a számodra legszimpatikusabb megbízást:",
            options=[0, 1, 2],
            format_func=lambda i: f"{napi_ajanlatok[i]['cim']} | Távolság: {napi_ajanlatok[i]['tav']} km | Becsült bevétel: {napi_ajanlatok[i]['alap_bev']:,} Ft"
        )
        
        aktiv_feladat = napi_ajanlatok[valasztott_index]
        st.info(f"**Részletek:** {aktiv_feladat['leírás']} (Ideális eszköz hozzá: *{aktiv_feladat['javasolt']}*)")

        jarmuvek = {
            "🚐 Helyi Furgon (Olcsó, stabil)": {"kapacitas": 20, "koltseg_km": 35},
            "🚛 Nagy Teherautó (A győztes!)": {"kapacitas": 60, "koltseg_km": 110},
            "🚢 Konténeres Hajó (Óriási raktér)": {"kapacitas": 150, "koltseg_km": 290},
            "✈️ Cargo Repülő (Villámgyors)": {"kapacitas": 80, "koltseg_km": 680}
        }

        valasztott_jarmu = st.selectbox("Milyen járművel teljesíted?", list(jarmuvek.keys()))
        j = jarmuvek[valasztott_jarmu]

        mennyiseg = st.slider("Mennyi árut pakolsz be?", 1, j["kapacitas"], 15)
        gyorshajtas = st.checkbox("⚡ Sietsz? (Gyorshajtás kockázata: traffipax bírság)")

        if st.button("🚀 Megbízás teljesítése!", type="primary"):
            tavolsag = aktiv_feladat["tav"]
            alap_koltseg = tavolsag * j["koltseg_km"]
            kedvezmeny_faktor = (100 - st.session_state.uzemanyag_kedvezmeny) / 100
            ut_koltseg = int(alap_koltseg * kedvezmeny_faktor)

            helyes_jarmu = (valasztott_jarmu == aktiv_feladat['javasolt'])

            extra_birsag = 0
            if gyorshajtas and random.random() < 0.28:
                extra_birsag = 35000
                st.error("📸 Traffipax elkapott! -35,000 Ft gyorshajtási bírság.")

            raktar_szorzó = 1 + (st.session_state.raktar_szint - 1) * 0.15

            if helyes_jarmu:
                bevetel = int(aktiv_feladat['alap_bev'] * (mennyiseg / j['kapacitas']) * raktar_szorzó)
                if gyorshajtas and extra_birsag == 0:
                    bevetel = int(bevetel * 1.15)
                
                profit = bevetel - ut_koltseg - extra_birsag
                st.session_state.penz += profit
                st.success(f"🎯 Kiváló járműválasztás! Tiszta profit: **+{profit:,} Ft**")
            else:
                vesztesseg_birsag = 50000
                st.session_state.penz -= (ut_koltseg + vesztesseg_birsag)
                profit = -ut_koltseg - vesztesseg_birsag
                st.error(f"❌ Rossz eszköz ehhez a feladathoz! Veszteség: **{profit:,} Ft**")

            passziv_bevetel = (st.session_state.soforok_szama - 1) * 15000
            st.session_state.penz += passziv_bevetel

            st.session_state.rivalis_penz += random.randint(45000, 85000)
            st.session_state.kor += 1
            st.rerun()

    else:
        st.balloons()
        st.markdown("# 🏆 Vége a 10 napos logisztikai maratonnak!")
        st.markdown(f"### A te céged tőkéje: **{st.session_state.penz:,} Ft**")
        st.markdown(f"### A rivális MegaLog Kft. tőkéje: **{st.session_state.rivalis_penz:,} Ft**")

        if st.session_state.penz > st.session_state.rivalis_penz:
            st.success("🥇 Fantasztikus teljesítmény! Teljesen letaroltad a piacot 10 nap alatt!")
        else:
            st.error("🥈 A MegaLog Kft. jobban bírta a hosszú távú versenyt.")

        if st.button("🔄 Új játék indítása"):
            st.session_state.indul = False
            st.rerun()
