import streamlit as st
import random

st.set_page_config(page_title="Logisztikai Tycoon: Ultimate", page_icon="🚀", layout="centered")

st.title("🚀 Logisztikai Tycoon: Ultimate Edition")
st.markdown("Vezesd piacvezetővé a szállítmányozó céged a **MegaLog Kft.** elleni harcban! Kerüld el a váratlan eseményeket, vagy próbáld ki a feketepiacot!")

if "indul" not in st.session_state:
    st.session_state.indul = False

if not st.session_state.indul:
    st.markdown("### 🏢 Cégalapítás")
    ceg_nev = st.text_input("Céged neve:", "Gyorshoz Kft.")
    
    if st.button("Induljon a birodalom! 🎯"):
        st.session_state.indul = True
        st.session_state.ceg_nev = ceg_nev
        st.session_state.penz = 120000
        st.session_state.rivalis_penz = 100000
        st.session_state.kor = 1
        st.session_state.fejlesztes_sebesseg = 0  # % bónusz
        st.session_state.fejlesztes_olcsobb = 0   # % költségcsökkentés
        st.rerun()

else:
    # Oldalsáv statisztikák
    st.sidebar.markdown(f"### 📊 {st.session_state.ceg_nev}")
    st.sidebar.metric(label="💰 Tőkéd", value=f"{st.session_state.penz:,} Ft")
    st.sidebar.metric(label="🤖 Rivális (MegaLog) tőkéje", value=f"{st.session_state.rivalis_penz:,} Ft")
    st.sidebar.metric(label="📅 Aktuális Nap", value=f"{st.session_state.kor} / 5")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🛠️ Flotta Fejlesztések")
    st.sidebar.text(f"Sebesség bónusz: +{st.session_state.fejlesztes_sebesseg}%")
    st.sidebar.text(f"Költségcsökkentés: -{st.session_state.fejlesztes_olcsobb}%")
    
    if st.session_state.penz >= 40000 and st.sidebar.button("⚡ +10% Üzemanyag-hatékonyság (40k Ft)"):
        st.session_state.penz -= 40000
        st.session_state.fejlesztes_olcsobb += 10
        st.success("Sikeres fejlesztés!")
        st.rerun()

    if st.session_state.kor <= 5:
        st.markdown(f"## 🗺️ {st.session_state.kor}. Nap: Stratégia és Fuvar")
        
        jarmuvek = {
            "🚐 Helyi Furgon": {"kapacitas": 15, "koltseg_km": 40},
            "🚛 Nagy Teherautó": {"kapacitas": 45, "koltseg_km": 130},
            "🚢 Konténeres Hajó": {"kapacitas": 130, "koltseg_km": 350},
            "✈️ Cargo Repülő": {"kapacitas": 70, "koltseg_km": 800}
        }

        valasztott_jarmu = st.selectbox("Válassz szállítóeszközt:", list(jarmuvek.keys()))
        j = jarmuvek[valasztott_jarmu]

        celok = {
            "🏠 Helyi piac (60 km)": 60,
            "🇪🇺 Nyugat-Európa (600 km)": 600,
            "🌏 Távol-Kelet (3500 km)": 3500
        }
        valasztott_cel = st.selectbox("Válassz útvonalat:", list(celok.keys()))
        tavolsag = celok[valasztott_cel]

        # Feketepiac opció
        feketepiac = st.checkbox("🔥 Feketepiaci / Csempész áru szállítása (Dupla bevétel, de 35% esély a bukásra!)")

        mennyiseg = st.slider("Mennyi árut pakolsz be?", 1, j["kapacitas"], 5)

        if st.button("🚀 Indítás az útra!", type="primary"):
            # Költségek számítása fejlesztéssel
            alap_koltseg = tavolsag * j["koltseg_km"]
            kedvezmeny_faktor = (100 - st.session_state.fejlesztes_olcsobb) / 100
            ut_koltseg = int(alap_koltseg * kedvezmeny_faktor)

            # Váratlan esemény sorsolás
            esemenyek = [
                ("Semmi különös, sima út volt.", 1.0, "✨"),
                ("Dugóba keverkedtek a kamionok! +20% útiköltség", 1.2, "🚧"),
                ("Üzemanyagár-robbanás! +30% útiköltség", 1.3, "⛽"),
                ("Zöld hullám és kedvező szél! -15% útiköltség", 0.85, "💨"),
                ("Defektet kapott a jármű, szerelni kellett.", 1.1, "🔧")
            ]
            esemeny_szoveg, esemeny_szorzo, esemeny_ikon = random.choice(esemenyek)
            ut_koltseg = int(ut_koltseg * esemeny_szorzo)

            # Feketepiac logika
            if feketepiac:
                bukas = random.random() < 0.35
                if bukas:
                    biro_birsag = 150000
                    st.session_state.penz -= biro_birsag
                    st.error(f"🚨 A VÁMOSOK LEKAPCSOLTÁK A SZÁLLÍTMÁNYT! Lefoglalták az árut és kiírtak {biro_birsag:,} Ft bírságot!")
                    profit = -ut_koltseg - biro_birsag
                else:
                    bevetel = mennyiseg * random.randint(3000, 4500)
                    profit = bevetel - ut_koltseg
                    st.session_state.penz += profit
                    st.success(f"🥷 Sikerült kicsempészni az árut! Tiszta profit: **+{profit:,} Ft**")
            else:
                eladasi_ar = random.randint(1300, 1900)
                bevetel = mennyiseg * eladasi_ar
                profit = bevetel - ut_koltseg
                st.session_state.penz += profit

                if profit > 0:
                    st.success(f"🎉 Sikeres fuvar! ({esemeny_ikon} {esemeny_szoveg}) | Profit: **+{profit:,} Ft**")
                else:
                    st.warning(f"⚠️ Ráfizetéses fuvar! ({esemeny_ikon} {esemeny_szoveg}) | Veszteség: **{profit:,} Ft**")

            # Rivális AI fejlődése
            st.session_state.rivalis_penz += random.randint(30000, 90000)

            # Következő nap
            st.session_state.kor += 1
            st.rerun()

    else:
        st.balloons()
        st.markdown("# 🏆 Vége a 5 napos üzleti ciklusnak!")
        
        st.markdown(f"### A te céged tőkéje: **{st.session_state.penz:,} Ft**")
        st.markdown(f"### A rivális MegaLog Kft. tőkéje: **{st.session_state.rivalis_penz:,} Ft**")

        if st.session_state.penz > st.session_state.rivalis_penz:
            st.success("🥇 GRATULÁLUNK! Nyertél, te lettél a logisztikai piac királya!")
        else:
            st.error("🥈 A rivális MegaLog Kft. idén megelőzött. Próbáld újra egy okosabb stratégiával!")

        if st.button("🔄 Új játék indítása"):
            st.session_state.indul = False
            st.rerun()
