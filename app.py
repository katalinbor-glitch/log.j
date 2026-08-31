import streamlit as st
import random

st.set_page_config(page_title="Global Logistics Tycoon", page_icon="🚀", layout="centered")

st.title("🚀 Global Logistics Tycoon")
st.markdown("Üdvözöljük a vezérigazgató úr szobájában! Építs fel egy nemzetközi szállítmányozási birodalmat, hozz meg kockázatos döntéseket, és hagyd le a riválisodat!")

if "jatek_indul" not in st.session_state:
    st.session_state.jatek_indul = False

if not st.session_state.jatek_indul:
    st.markdown("### 📋 Új cég indítása")
    nev = st.text_input("A te céged neve:", "Express Cargo Kft.")
    szint = st.selectbox("Válassz nehézségi szintet:", ["Kezdő (Belföldi piac)", "Haladó (Európai Import)", "Profi (Globális Kockázat)"])
    
    if st.button("Cég alapítása és indítás! 🎯"):
        st.session_state.jatek_indul = True
        st.session_state.nev = nev
        st.session_state.szint = szint
        st.session_state.nap = 1
        st.session_state.jatek_vege = False
        st.session_state.hitel = 0
        
        if "Kezdő" in szint:
            st.session_state.penz = 50000
            st.session_state.ai_penz = 25000
        elif "Haladó" in szint:
            st.session_state.penz = 35000
            st.session_state.ai_penz = 35000
        else:
            st.session_state.penz = 25000
            st.session_state.ai_penz = 45000
            
        st.session_state.keszlet = 0
        st.session_state.jarmu_szint = 1
        st.session_state.jarmu_kapacitas = 5
        st.rerun()

else:
    # Raktárak
    raktarak = {
        "🏭 Budapest (Helyi raktár)": {"tavolsag": 20, "ar": 280, "valuta": "HUF", "vam": 0.0, "ikon": "🏠"},
        "🚛 Bécs (EU raktár)": {"tavolsag": 250, "ar": 0.75, "valuta": "EUR", "vam": 0.05, "ikon": "🇦🇹"},
        "🚢 Frankfurt (Közép-Európa)": {"tavolsag": 900, "ar": 0.60, "valuta": "EUR", "vam": 0.12, "ikon": "🇩🇪"},
        "✈️ Sanghaj (Globális tengeri/légi)": {"tavolsag": 3000, "ar": 0.80, "valuta": "USD", "vam": 0.22, "ikon": "🇨🇳"}
    }
    
    uzemanyag_km = 8
    raktar_koltseg = 30

    # Oldalsáv statisztika
    st.sidebar.markdown(f"### 🏢 {st.session_state.nev}")
    st.sidebar.markdown(f"**Szint:** {st.session_state.szint}")
    st.sidebar.divider()
    st.sidebar.metric(label="📅 Aktuális Nap", value=f"{st.session_state.nap} / 7")
    st.sidebar.metric(label="💰 Céged Tőkéje", value=f"{st.session_state.penz:,} Ft")
    st.sidebar.metric(label="🏦 Aktuális Hitel", value=f"{st.session_state.hitel:,} Ft")
    st.sidebar.metric(label="📦 Raktárkészlet", value=f"{st.session_state.keszlet} db")
    st.sidebar.metric(label="🚚 Flotta Kapacitás", value=f"{st.session_state.jarmu_szint}. szint ({st.session_state.jarmu_kapacitas} db)")
    st.sidebar.metric(label="🤖 AI Rivális Tőkéje", value=f"{st.session_state.ai_penz:,} Ft")

    if not st.session_state.jatek_vege:
        st.markdown(f"## 📊 {st.session_state.nap}. Napi Operációs Döntések")
        
        # Piaci adatok
        eur_arfolyam = random.randint(385, 415)
        usd_arfolyam = random.randint(355, 385)
        eladasi_ar = random.choice([600, 650, 700])
        
        st.success(f"💱 **Piaci Index:** 1 EUR = **{eur_arfolyam} Ft** | 1 USD = **{usd_arfolyam} Ft** | 🏷️ Mai eladási ár: **{eladasi_ar} Ft/db**")

        # Hitel és fejlesztés gombok oszlopokban
        col1, col2 = st.columns(2)
        with col1:
            if st.session_state.hitel == 0 and st.button("💵 Banki hitel felvétele (+20 000 Ft)"):
                st.session_state.hitel += 20000
                st.session_state.penz += 20000
                st.rerun()
            elif st.session_state.hitel > 0 and st.button("💳 Hitel törlesztése (-10 000 Ft)"):
                if st.session_state.penz >= 10000:
                    st.session_state.hitel -= 10000
                    st.session_state.penz -= 10000
                    st.rerun()
                else:
                    st.error("Nincs elég pénzed a törlesztéshez!")
        with col2:
            if st.session_state.jarmu_szint < 3 and st.session_state.penz >= 12000:
                if st.button("🚀 Flotta fejlesztése (12 000 Ft)"):
                    st.session_state.penz -= 12000
                    st.session_state.jarmu_szint += 1
                    st.session_state.jarmu_kapacitas += 5
                    st.rerun()

        st.divider()
        
        # Raktárválasztás
        valasztott_raktar = st.selectbox("📦 Válassz beszállítói partnert:", ["Kihagyom (Csak készletkiárusítás)"] + list(raktarak.keys()))
        
        rendeles = 0
        if "Kihagyom" not in valasztott_raktar:
            rendeles = st.slider("Mennyi árut rendelsz a fuvarkorláton belül?", 1, st.session_state.jarmu_kapacitas, 1)

        if st.button("⚡ Nap lezárása és fuvar indítása!", type="primary"):
            # AI lépése
            ai_eladott = random.randint(15, 30)
            st.session_state.ai_penz += (ai_eladott * eladasi_ar) - random.randint(3000, 6000)

            # Beszerzés és logisztika
            if "Kihagyom" not in valasztott_raktar:
                r_info = raktarak[valasztott_raktar]
                
                if r_info["valuta"] == "EUR":
                    egyseg_ar = r_info["ar"] * eur_arfolyam
                elif r_info["valuta"] == "USD":
                    egyseg_ar = r_info["ar"] * usd_arfolyam
                else:
                    egyseg_ar = r_info["ar"]
                
                ar_koltseg = rendeles * egyseg_ar
                ut_koltseg = r_info["tavolsag"] * 2 * uzemanyag_km
                osszes_kiadas = ar_koltseg + ut_koltseg

                if osszes_kiadas > st.session_state.penz:
                    st.error("❌ Nincs elég tőke a fuvar kifizetéséhez! A rendelés meghiúsult.")
                else:
                    st.session_state.penz -= osszes_kiadas
                    
                    # Vám / sérülés kockázat
                    hibas = sum(1 for _ in range(rendeles) if random.random() < r_info["vam"])
                    sikeres = rendeles - hibas
                    
                    if hibas > 0:
                        st.warning(f"⚠️ Vámbürokrácia / logisztikai hiba miatt {hibas} db áru kárba veszett!")
                    st.session_state.keszlet += sikeres

            # Piaci eladás
            kereslet = random.randint(15, 35)
            eladott = min(st.session_state.keszlet, kereslet)
            bevetel = eladott * eladasi_ar
            st.session_state.penz += bevetel
            st.session_state.keszlet -= eladott

            # Raktárköltség
            r_koltseg = st.session_state.keszlet * raktar_koltseg
            st.session_state.penz -= r_koltseg

            # Napi összegzés dobozban
            st.info(f"📋 **E nap mérlege:** Eladva: **{eladott} db** áru | Bevétel: **{bevetel:,} Ft** | Raktáradó: **{r_koltseg:,} Ft**")

            if st.session_state.nap >= 7:
                st.session_state.jatek_vege = True
            else:
                st.session_state.nap += 1
            
            st.rerun()

    else:
        st.balloons()
        st.markdown("# 🏆 Vége a 7 napos üzleti évnek!")
        st.markdown(f"A te céged végső tőkéje: **{st.session_state.penz:,} Ft**")
        st.markdown(f"A rivális AI cég tőkéje: **{st.session_state.ai_penz:,} Ft**")
        
        if st.session_state.penz > st.session_state.ai_penz:
            st.success("🎉 Gratulálunk! Te lettél a piac leggazdagabb logisztikai mágnása!")
        else:
            st.warning("🥈 A rivális cég idén jobban sakkozott a számokkal. Próbáld újra!")

        if st.button("🔄 Új játék indítása"):
            st.session_state.jatek_indul = False
            st.rerun()
