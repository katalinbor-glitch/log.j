import streamlit as st
import random

st.set_page_config(page_title="Logisztikai Tycoon: Turbo Edition", page_icon="🚚", layout="centered")

st.title("🚚 Logisztikai Tycoon: Turbo Edition")
st.markdown("Most már nemcsak fuvarozol, hanem cégbirodalmat építesz! Versenyezz a **MegaLog Kft.**-vel, vegyél fel sofőröket és fejleszd a telephelyed!")

if "indul" not in st.session_state:
    st.session_state.indul = False

if not st.session_state.indul:
    st.markdown("### 🏢 Új Vállalat Indítása")
    ceg_nev = st.text_input("Céged neve:", "TurboTrans Kft.")
    
    if st.button("Induljon a birodalom! 🚀"):
        st.session_state.indul = True
        st.session_state.ceg_nev = ceg_nev
        st.session_state.penz = 150000
        st.session_state.rivalis_penz = 130000
        st.session_state.kor = 1
        st.session_state.soforok_szama = 1
        st.session_state.raktar_szint = 1
        st.session_state.bónusz_bevetel = 0 
        st.rerun()

else:
    st.sidebar.markdown(f"### 📊 {st.session_state.ceg_nev}")
    st.sidebar.metric(label="💰 Tőkéd", value=f"{st.session_state.penz:,} Ft")
    st.sidebar.metric(label="🤖 MegaLog Kft. tőkéje", value=f"{st.session_state.rivalis_penz:,} Ft")
    st.sidebar.metric(label="📅 Aktuális Nap", value=f"{st.session_state.kor} / 5")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🏢 Cégfejlesztések")
    st.sidebar.text(("👥 Sofőrök száma: ") + str(st.session_state.soforok_szama))
    st.sidebar.text(f"📦 Raktár szint: {st.session_state.raktar_szint}")

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

    if st.session_state.kor <= 5:
        st.markdown(f"## 🗺️ {st.session_state.kor}. Nap: Válassz küldetést!")
        
        jarmuvek = {
            "🚐 Helyi Furgon (Olcsó, stabil)": {"kapacitas": 20, "koltseg_km": 30},
            "🚛 Nagy Teherautó (A győztes!)": {"kapacitas": 60, "koltseg_km": 100},
            "🚢 Konténeres Hajó (Óriási raktér)": {"kapacitas": 150, "koltseg_km": 300},
            "✈️ Cargo Repülő (Villámgyors)": {"kapacitas": 80, "koltseg_km": 700}
        }

        valasztott_jarmu = st.selectbox("Válassz járművet:", list(jarmuvek.keys()))
        j = jarmuvek[valasztott_jarmu]

        celok = {
            "🏠 Helyi piac (50 km)": 50,
            "🇪🇺 Nyugat-Európa (500 km)": 500,
            "🌏 Távol-Kelet (3000 km)": 3000
        }
        valasztott_cel = st.selectbox("Válassz útvonalat:", list(celok.keys()))
        tavolsag = celok[valasztott_cel]

        VIP_megbizas = random.random() < 0.35
        if VIP_megbizas:
            st.info("⭐ **VIP megbízás érkezett!** (+50% bevétel)")

        mennyiseg = st.slider("Mennyi árut pakolsz be?", 1, j["kapacitas"], 10)

        if st.button("🚀 Indulás a fuvarra!", type="primary"):
            ut_koltseg = tavolsag * j["koltseg_km"]
            alap_ar = random.randint(1400, 2000)
            raktar_szorzó = 1 + (st.session_state.raktar_szint - 1) * 0.15
            
            bevetel = int(mennyiseg * alap_ar * raktar_szorzó)
            
            if VIP_megbizas:
                bevetel = int(bevetel * 1.5)

            profit = bevetel - ut_koltseg
            passziv_bevetel = (st.session_state.soforok_szama - 1) * 15000
            ossz_profit = profit + passziv_bevetel

            st.session_state.penz += ossz_profit

            if ossz_profit > 0:
                st.success(f"🎉 Sikeres fuvar! Tiszta profit: **+{ossz_profit:,} Ft**")
            else:
                st.warning(f"⚠️ Ráfizetéses fuvar! Veszteség: **{ossz_profit:,} Ft**")

            st.session_state.rivalis_penz += random.randint(40000, 85000)
            st.session_state.kor += 1
            st.rerun()

    else:
        st.balloons()
        st.markdown("# 🏆 Vége az 5 napos ciklusnak!")
        st.markdown(f"### A te céged tőkéje: **{st.session_state.penz:,} Ft**")
        st.markdown(f"### A rivális MegaLog Kft. tőkéje: **{st.session_state.rivalis_penz:,} Ft**")

        if st.session_state.penz > st.session_state.rivalis_penz:
            st.success("🥇 Óriási győzelem! Te lettél a logisztikai piac egyeduralkodója!")
        else:
            st.error("🥈 A MegaLog Kft. ezúttal jobban bírta a tempót.")

        if st.button("🔄 Új játék indítása"):
            st.session_state.indul = False
            st.rerun()
