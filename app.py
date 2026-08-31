import streamlit as st
import random

st.set_page_config(page_title="Logisztikai Flotta Tycoon", page_icon="🚚", layout="centered")

st.title("🚚 Logisztikai Flotta Tycoon")
st.markdown("Irányítsd a saját szállítmányozási céged! Válassz járművet, pakolj meg áruval, és szállíts a legtöbb profitért!")

if "indul" not in st.session_state:
    st.session_state.indul = False

if not st.session_state.indul:
    st.markdown("### 🏢 Új Vállalat Alapítása")
    ceg_nev = st.text_input("Céged neve:", "Gyorshoz Kft.")
    
    if st.button("Induljon az üzlet! 🚀"):
        st.session_state.indul = True
        st.session_state.ceg_nev = ceg_nev
        st.session_state.penz = 100000
        st.session_state.kor = 1
        st.session_state.sikeres_fuvarok = 0
        st.rerun()

else:
    st.sidebar.markdown(f"### 📊 {st.session_state.ceg_nev}")
    st.sidebar.metric(label="💰 Tőke", value=f"{st.session_state.penz:,} Ft")
    st.sidebar.metric(label="📅 Aktuális Nap", value=f"{st.session_state.kor} / 5")
    st.sidebar.metric(label="📦 Teljesített fuvarok", value=st.session_state.sikeres_fuvarok)

    if st.session_state.kor <= 5:
        st.markdown(f"## 🗺️ {st.session_state.kor}. Nap: Fuvar tervezése")
        
        jarmuvek = {
            "🚐 Helyi Furgon (Olcsó, kicsi)": {"kapacitas": 10, "koltseg_km": 50},
            "🚛 Nagy Teherautó (Közepes)": {"kapacitas": 40, "koltseg_km": 150},
            "🚢 Konténeres Hajó (Hatalmas, lassú)": {"kapacitas": 120, "koltseg_km": 400},
            "✈️ Cargo Repülő (Gyors, drága)": {"kapacitas": 60, "koltseg_km": 900}
        }

        valasztott_jarmu = st.selectbox("Válassz szállítóeszközt:", list(jarmuvek.keys()))
        j = jarmuvek[valasztott_jarmu]

        celok = {
            "🏠 Helyi piac (Budapest környéke)": 60,
            "🇪🇺 Nyugat-Európa (Bécs / München)": 600,
            "🌏 Távol-Kelet (Shanghai export)": 3500
        }
        valasztott_cel = st.selectbox("Válassz célállomást:", list(celok.keys()))
        tavolsag = celok[valasztott_cel]

        st.info(f"Jármű kapacitás: **{j['kapacitas']} db** áru | Távolság: **{tavolsag} km**")

        mennyiseg = st.slider("Mennyi árut pakolsz a járműbe?", 1, j["kapacitas"], 5)

        if st.button("📦 Indulás az útra!", type="primary"):
            ut_koltseg = tavolsag * j["koltseg_km"]
            eladasi_ar_egyseg = random.randint(1200, 1800)
            bevetel = mennyiseg * eladasi_ar_egyseg
            profit = bevetel - ut_koltseg

            st.session_state.penz += profit
            st.session_state.sikeres_fuvarok += 1

            if profit > 0:
                st.success(f"🎉 Sikeres fuvar! Bevétel: {bevetel:,} Ft | Útiköltség: {ut_koltseg:,} Ft | Tiszta profit: **+{profit:,} Ft**")
            else:
                st.warning(f"⚠️ Ráfizetéses fuvar! Bevétel: {bevetel:,} Ft | Útiköltség: {ut_koltseg:,} Ft | Veszteség: **{profit:,} Ft**")

            st.session_state.kor += 1
            st.rerun()
    else:
        st.balloons()
        st.markdown("# 🏆 Vége a játékra szánt napoknak!")
        st.markdown(f"Céged végső tőkéje: **{st.session_state.penz:,} Ft**")
        st.markdown(f"Összes sikeres fuvarod: **{st.session_state.sikeres_fuvarok} db**")

        if st.button("🔄 Új játék indítása"):
            st.session_state.indul = False
            st.rerun()
