import streamlit as st
import random

st.set_page_config(page_title="Logisztikai Tycoon: Real Time & Intermodal", page_icon="⏳", layout="centered")

st.title("⏳ Logisztikai Tycoon: Real Time & Intermodal")
st.markdown("Most már a **menetidő** is számít! A távoli hajóutak és repülők több napig kötik le a kapacitásodat. Tervezz előre!")

if "indul" not in st.session_state:
    st.session_state.indul = False

if not st.session_state.indul:
    st.markdown("### 🏢 Új Vállalat Indítása")
    ceg_nev = st.text_input("Céged neve:", "GlobalTrans Kft.")
    
    if st.button("Induljon a valós idejű birodalom! 🚀"):
        st.session_state.indul = True
        st.session_state.ceg_nev = ceg_nev
        st.session_state.penz = 180000
        st.session_state.rivalis_penz = 150000
        st.session_state.kor = 1
        st.session_state.soforok_szama = 1
        st.session_state.raktar_szint = 1
        st.session_state.uzemanyag_kedvezmeny = 0
        st.rerun()

else:
    st.sidebar.markdown(f"### 📊 {st.session_state.ceg_nev}")
    st.sidebar.metric(label="💰 Tőkéd", value=f"{st.session_state.penz:,} Ft")
    st.sidebar.metric(label="🤖 MegaLog Kft. tőkéje", value=f"{st.session_state.rivalis_penz:,} Ft")
    st.sidebar.metric(label="📅 Aktuális Nap", value=f"{st.session_state.kor} / 12")
    
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

    if st.session_state.kor <= 12:
        st.markdown(f"## 🗺️ {st.session_state.kor}. Nap: Aktuális Megbízások")

        random.seed(st.session_state.kor * 555)
        
        ajanlatok_pool = [
            {"cim": "🍅 Friss mezőgazdasági export", "leírás": "Gyors helyi fuvar hűtést igénylő áruval.", "javasolt": "🚐 Helyi Furgon (Olcsó, stabil)", "tav": 50, "ido": 1, "alap_bev": 70000},
            {"cim": "📦 Gyári alkatrészek Nyugat-Európába", "leírás": "Megbízható közúti fuvar uniós partnerhez.", "javasolt": "🚛 Nagy Teherautó (A győztes!)", "tav": 500, "ido": 2, "alap_bev": 190000},
            {"cim": "🚢 Konténeres nyersanyag a Távol-Keletre", "leírás": "Hatalmas tömegáru óceáni útvonalon. (Hosszú menetidő!)", "javasolt": "🚢 Konténeres Hajó (Óriási raktér)", "tav": 3000, "ido": 4, "alap_bev": 600000},
            {"cim": "⚡ Sürgős mikrochip szállítmány Ázsiába", "leírás": "Magas értékű, expressz repülős küldetés.", "javasolt": "✈️ Cargo Repülő (Villámgyors)", "tav": 3000, "ido": 2, "alap_bev": 850000}
        ]
        
        napi_ajanlatok = random.sample(ajanlatok_pool, 3)

        valasztott_index = st.radio(
            "Válaszd ki a napi fuvarfeladatot:",
            options=[0, 1, 2],
            format_func=lambda i: f"{napi_ajanlatok[i]['cim']} | Táv: {napi_ajanlatok[i]['tav']} km | Időtartam: {napi_ajanlatok[i]['ido']} nap | Bevétel: {napi_ajanlatok[i]['alap_bev']:,} Ft"
        )
        
        aktiv_feladat = napi_ajanlatok[valasztott_index]
        st.info(f"**Részletek:** {aktiv_feladat['leírás']} | **Menetidő:** {aktiv_feladat['ido']} nap | Ajánlott eszköz: *{aktiv_feladat['javasolt']}*")

        st.markdown("### 📋 Incoterms Felelősségi Klauzula")
        incoterm = st.selectbox(
            "Válaszd ki a szerződéses feltételt:",
            [
                "EXW (Ex Works) - Kisebb bevétel, minimális felelősség",
                "FOB (Free on Board) - Standard piaci ár és felelősség",
                "DDP (Delivered Duty Paid) - Maximális bevétel, de teljes kockázat!"
            ]
        )

        kombinalt = False
        if aktiv_feladat['tav'] >= 500:
            kombinalt = st.checkbox("⚓+🚛 Intermodális Kombinált Szállítás (Hajó + Teherautó: olcsóbb km, de +20k átrakodási díj)")

        jarmuvek = {
            "🚐 Helyi Furgon (Olcsó, stabil)": {"kapacitas": 20, "koltseg_km": 35},
            "🚛 Nagy Teherautó (A győztes!)": {"kapacitas": 60, "koltseg_km": 110},
            "🚢 Konténeres Hajó (Óriási raktér)": {"kapacitas": 150, "koltseg_km": 280},
            "✈️ Cargo Repülő (Villámgyors)": {"kapacitas": 80, "koltseg_km": 650}
        }

        valasztott_jarmu = st.selectbox("Milyen fő szállítóeszközt indítasz?", list(jarmuvek.keys()))
        j = jarmuvek[valasztott_jarmu]

        mennyiseg = st.slider("Mennyi árut pakolsz be?", 1, j["kapacitas"], 15)

        if st.button("🚀 Megbízás indítása!", type="primary"):
            tavolsag = aktiv_feladat['tav']
            fuvar_ido = aktiv_feladat['ido']
            
            km_koltseg = j['koltseg_km']
            atrakodasi_dij = 0
            if kombinalt:
                km_koltseg = int(km_koltseg * 0.75)
                atrakodasi_dij = 20000

            alap_koltseg = tavolsag * km_koltseg
            kedvezmeny_faktor = (100 - st.session_state.uzemanyag_kedvezmeny) / 100
            ut_koltseg = int(alap_koltseg * kedvezmeny_faktor) + atrakodasi_dij

            helyes_jarmu = (valasztott_jarmu == aktiv_feladat['javasolt'])

            incoterm_szorzó = 1.0
            if "EXW" in incoterm:
                incoterm_szorzó = 0.85
            elif "DDP" in incoterm:
                incoterm_szorzó = 1.25

            raktar_szorzó = 1 + (st.session_state.raktar_szint - 1) * 0.15

            if helyes_jarmu:
                bevetel = int(aktiv_feladat['alap_bev'] * (mennyiseg / j['kapacitas']) * raktar_szorzó * incoterm_szorzó)
                
                vám_birsag = 0
                if "DDP" in incoterm and tavolsag >= 500 and random.random() < 0.18:
                    vám_birsag = 40000
                    st.warning("⚠️ Vámhivatali akadás DDP fuvarnál! -40,000 Ft büntetés.")

                profit = bevetel - ut_koltseg - vám_birsag
                st.session_state.penz += profit
                st.success(f"🎯 Sikeres fuvar ({fuvar_ido} napig tartott)! Tiszta profit: **+{profit:,} Ft**")
            else:
                vesztesseg_birsag = 50000
                st.session_state.penz -= (ut_koltseg + vesztesseg_birsag)
                profit = -ut_koltseg - vesztesseg_birsag
                st.error(f"❌ Nem megfelelő jármű! Veszteség: **{profit:,} Ft**")

            # A passziv bevétel a fuvar ideje alatt minden nap jár a sofőrök után!
            osszes_passziv = (st.session_state.soforok_szama - 1) * 15000 * fuvar_ido
            st.session_state.penz += osszes_passziv

            # A rivális is halad a napok alatt
            st.session_state.rivalis_penz += random.randint(45000, 85000) * fuvar_ido

            # A napok számlálója annyival nő, amennyi ideig a fuvar tartott!
            st.session_state.kor += fuvar_ido
            st.rerun()

    else:
        st.balloons()
        st.markdown("# 🏆 Vége a 12 napos logisztikai futamnak!")
        st.markdown(f"### A te céged tőkéje: **{st.session_state.penz:,} Ft**")
        st.markdown(f"### A rivális MegaLog Kft. tőkéje: **{st.session_state.rivalis_penz:,} Ft**")

        if st.session_state.penz > st.session_state.rivalis_penz:
            st.success("🥇 Zseniális logisztikai ütemterv! Te nyerted meg a versenyt!")
        else:
            st.error("🥈 A MegaLog Kft. jobban gazdálkodott az idővel és a flottával.")

        if st.button("🔄 Új játék indítása"):
            st.session_state.indul = False
            st.rerun()
