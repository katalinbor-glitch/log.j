import streamlit as st
import random

st.set_page_config(page_title="Logisztikai Tycoon: Multi-Fleet Pro", page_icon="🚚", layout="centered")

st.title("🚚 Logisztikai Tycoon: Multi-Fleet Pro")
st.markdown("A legprofibb szint! Használd a pontos **Incoterms klauzulákat** (FCA, CPT, FOB, DDP), szervezz **kombinált multimodális fuvarokat**, és indíts egyszerre **akár 2 szállítóeszközt** is egyetlen megbízáshoz!")

if "indul" not in st.session_state:
    st.session_state.indul = False

if not st.session_state.indul:
    st.markdown("### 🏢 Új Vállalat Indítása")
    ceg_nev = st.text_input("Céged neve:", "GlobalTrans Kft.")
    
    if st.button("Induljon a multimodális birodalom! 🚀"):
        st.session_state.indul = True
        st.session_state.ceg_nev = ceg_nev
        st.session_state.penz = 220000
        st.session_state.rivalis_penz = 180000
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
        st.markdown(f"## 🗺️ {st.session_state.kor}. Nap: Logisztikai Megbízások")

        random.seed(st.session_state.kor * 777)
        
        ajanlatok_pool = [
            {"cim": "🍅 Friss mezőgazdasági export", "leírás": "Helyi/regionális gyors fuvar hűtést igénylő áruval.", "javasolt": ["🚐 Helyi Furgon (Olcsó, stabil)"], "tav": 50, "ido": 1, "alap_bev": 75000},
            {"cim": "📦 Gyári alkatrészek Nyugat-Európába", "leírás": "Közúti fuvar uniós partnerhez. Akár több teherautó is küldhető.", "javasolt": ["🚛 Nagy Teherautó (A győztes!)"], "tav": 500, "ido": 2, "alap_bev": 210000},
            {"cim": "🚢 Hatalmas tömegáru a Távol-Keletre", "leírás": "Óriási tengeri konténeres fuvar (vagy kombinált flotta).", "javasolt": ["🚢 Konténeres Hajó (Óriási raktér)"], "tav": 3000, "ido": 4, "alap_bev": 650000},
            {"cim": "⚡ Sürgős elektronikai expressz", "leírás": "Magas értékű, sürgős küldetés Ázsiába.", "javasolt": ["✈️ Cargo Repülő (Villámgyors)"], "tav": 3000, "ido": 2, "alap_bev": 900000}
        ]
        
        napi_ajanlatok = random.sample(ajanlatok_pool, 3)

        valasztott_index = st.radio(
            "Válaszd ki a napi fuvarfeladatot:",
            options=[0, 1, 2],
            format_func=lambda i: f"{napi_ajanlatok[i]['cim']} | Táv: {napi_ajanlatok[i]['tav']} km | Idő: {napi_ajanlatok[i]['ido']} nap | Bevétel: {napi_ajanlatok[i]['alap_bev']:,} Ft"
        )
        
        aktiv_feladat = napi_ajanlatok[valasztott_index]
        st.info(f"**Részletek:** {aktiv_feladat['leírás']} | **Menetidő:** {aktiv_feladat['ido']} nap")

        # Szakszerű Incoterms klauzulák kezelése
        st.markdown("### 📋 Incoterms Szakmai Klauzulák")
        incoterm = st.selectbox(
            "Válaszd ki a nemzetközi szerződéses feltételt:",
            [
                "EXW (Ex Works) - Gyári átvétel: minimális felelősség, kisebb bevétel",
                "FCA (Free Carrier) - Költségmentes fuvarozónak átadva (Ideális közútra/kamionra)",
                "CPT (Carriage Paid To) - Fuvarozás fizetve rendeltetési helyig",
                "FOB (Free on Board) - Hajó fedélzetére rajtva (Csak vízi/tengeri szállításhoz)",
                "DDP (Delivered Duty Paid) - Vámkezelve leszállítva: max. bevétel, de teljes kockázat!"
            ]
        )

        jarmuvek = {
            "🚐 Helyi Furgon (Olcsó, stabil)": {"kapacitas": 20, "koltseg_km": 35},
            "🚛 Nagy Teherautó (A győztes!)": {"kapacitas": 60, "koltseg_km": 110},
            "🚢 Konténeres Hajó (Óriási raktér)": {"kapacitas": 150, "koltseg_km": 280},
            "✈️ Cargo Repülő (Villámgyors)": {"kapacitas": 80, "koltseg_km": 650}
        }

        st.markdown("### 🚛 Járműpark Kiválasztása (Akár 2 eszközt is indíthatsz egyszerre!)")
        elso_jarmu = st.selectbox("1. Elsődleges szállítóeszköz:", list(jarmuvek.keys()))
        
        masodik_jarmu_aktivalva = st.checkbox("➕ Második szállítóeszköz indítása is a megbízáshoz (Multi-fleet konvoj)")
        masodik_jarmu = None
        if masodik_jarmu_aktivalva:
            masodik_jarmu = st.selectbox("2. Másodlagos szállítóeszköz:", list(jarmuvek.keys()))

        mennyiseg = st.slider("Összes szállítandó árumennyiség egységben:", 1, 200, 30)

        if st.button("🚀 Konvoj indítása!", type="primary"):
            tavolsag = aktiv_feladat['tav']
            fuvar_ido = aktiv_feladat['ido']
            
            # Klauzula validáció és korrekció szakmailag
            helyes_klauzula = True
            if "FOB" in incoterm and "🚢" not in elso_jarmu and (not masodik_jarmu or "🚢" not in masodik_jarmu):
                helyes_klauzula = False
                st.warning("⚠️ Szakmai hiba: A FOB klauzula kizárólag tengeri/vízi szállításhoz (hajóhoz) használható! Emiatt a megbízó kötbért számolt fel.")

            incoterm_szorzó = 1.0
            if "EXW" in incoterm:
                incoterm_szorzó = 0.80
            elif "FCA" in incoterm or "CPT" in incoterm:
                incoterm_szorzó = 1.05
            elif "FOB" in incoterm:
                incoterm_szorzó = 1.15
            elif "DDP" in incoterm:
                incoterm_szorzó = 1.30

            # 1. Jármű költségei
            j1 = jarmuvek[elso_jarmu]
            kedv_fakt = (100 - st.session_state.uzemanyag_kedvezmeny) / 100
            ut_koltseg_1 = int(tavolsag * j1['koltseg_km'] * kedv_fakt)
            kapacitas_osszes = j1['kapacitas']

            # 2. Jármű költségei (ha van)
            ut_koltseg_2 = 0
            if masodik_jarmu_aktivalva and masodik_jarmu:
                j2 = jarmuvek[masodik_jarmu]
                ut_koltseg_2 = int(tavolsag * j2['koltseg_km'] * kedv_fakt)
                kapacitas_osszes += j2['kapacitas']

            ossz_ut_koltseg = ut_koltseg_1 + ut_koltseg_2

            # Ellenőrzés, hogy elegendő kapacitású járművet választott-e
            if mennyiseg > kapacitas_osszes:
                st.error(f"❌ A kiválasztott járművek kapacitása ({kapacitas_osszes} egység) kevés a bepakolt áruhoz ({mennyiseg} egység)! A fuvar meghiúsult.")
                st.session_state.penz -= 40000 # Kötbér
            else:
                raktar_szorzó = 1 + (st.session_state.raktar_szint - 1) * 0.15
                bevetel = int(aktiv_feladat['alap_bev'] * (mennyiseg / 50) * raktar_szorzó * incoterm_szorzó)
                
                if not helyes_klauzula:
                    bevetel = int(bevetel * 0.7) # Büntetés a rossz klauzula miatt

                vám_birsag = 0
                if "DDP" in incoterm and tavolsag >= 500 and random.random() < 0.20:
                    vám_birsag = 50000
                    st.warning("⚠️ Vámhivatali akadás DDP fuvarnál! -50,000 Ft vámbírság.")

                profit = bevetel - ossz_ut_koltseg - vám_birsag
                st.session_state.penz += profit
                
                if profit > 0:
                    st.success(f"🎯 Sikeres multimodális konvoj fuvar ({fuvar_ido} nap)! Tiszta profit: **+{profit:,} Ft**")
                else:
                    st.warning(f"⚠️ Ráfizetéses fuvar! Veszteség: **{profit:,} Ft**")

            passziv_bevetel = (st.session_state.soforok_szama - 1) * 15000 * fuvar_ido
            st.session_state.penz += passziv_bevetel

            st.session_state.rivalis_penz += random.randint(50000, 95000) * fuvar_ido
            st.session_state.kor += fuvar_ido
            st.rerun()

    else:
        st.balloons()
        st.markdown("# 🏆 Vége a 12 napos multimodális kihívásnak!")
        st.markdown(f"### A te céged tőkéje: **{st.session_state.penz:,} Ft**")
        st.markdown(f"### A rivális MegaLog Kft. tőkéje: **{st.session_state.rivalis_penz:,} Ft**")

        if st.session_state.penz > st.session_state.rivalis_penz:
            st.success("🥇 Te vagy a logisztikai piacon a legfőbb mogul! Óriási győzelem!")
        else:
            st.error("🥈 A MegaLog Kft. jobban taktikázott a klauzulákkal és a járművekkel.")

        if st.button("🔄 Új játék indítása"):
            st.session_state.indul = False
            st.rerun()
