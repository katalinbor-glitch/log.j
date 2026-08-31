import streamlit as st
import random

st.set_page_config(page_title="Logisztikai Tycoon: Pro Edition", page_icon="🚚", layout="centered")

st.title("🚚 Logisztikai Tycoon: Pro Edition")
st.markdown("Vezesd a céged a **MegaLog Kft.** ellen! Vigyázz a gyorshajtásra, a vezetési időre, és használd ki az időablakos bónuszokat!")

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
        st.session_state.uzemanyag_kedvezmeny = 0
        st.rerun()

else:
    st.sidebar.markdown(f"### 📊 {st.session_state.ceg_nev}")
    st.sidebar.metric(label="💰 Tőkéd", value=f"{st.session_state.penz:,} Ft")
    st.sidebar.metric(label="🤖 MegaLog Kft. tőkéje", value=f"{st.session_state.rivalis_penz:,} Ft")
    st.sidebar.metric(label="📅 Aktuális Nap", value=f"{st.session_state.kor} / 5")
    
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
        st.success(f"A raktár a(z) {st.session_state.raktar_szint}. szintre lépett!")
        st.rerun()

    if st.session_state.penz >= 40000 and st.sidebar.button("⚡ Üzemanyag-takarékosság (40k Ft)"):
        st.session_state.penz -= 40000
        st.session_state.uzemanyag_kedvezmeny += 15
        st.success("Sikeres fejlesztés!")
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

        csempeszet = st.checkbox("🔥 Titkos csempészáru (Dupla bevétel, de 20% esély a bukásra és 40k bírságra)")
        gyorshajtas = st.checkbox("⚡ Nyomod neki a gázt? (Gyorsabb fuvar, de 25% esély traffipaxra és 30k bírságra)")

        mennyiseg = st.slider("Mennyi árut pakolsz be?", 1, j["kapacitas"], 10)

        if st.button("🚀 Indulás a fuvarra!", type="primary"):
            # Vezetői idő túllépés esélye nagy távolságon
            sofor_kimerult = (tavolsag >= 3000) and (random.random() < 0.30)
            
            if sofor_kimerult:
                st.warning("😴 A sofór túllépte a engedélyezett vezetési időt! Pihennie kell, ez a nap elment.")
                st.session_state.kor += 1
                st.session_state.rivalis_penz += random.randint(40000, 85000)
                st.rerun()

            alap_koltseg = tavolsag * j["koltseg_km"]
            kedvezmeny_faktor = (100 - st.session_state.uzemanyag_kedvezmeny) / 100
            ut_koltseg = int(alap_koltseg * kedvezmeny_faktor)
            
            alap_ar = random.randint(1400, 2000)
            raktar_szorzó = 1 + (st.session_state.raktar_szint - 1) * 0.15
            
            extra_birsag = 0
            if gyorshajtas:
                if random.random() < 0.25:
                    extra_birsag = 30000
                    st.error("📸 Villant a traffipax! Gyorshajtási bírság: 30,000 Ft.")

            if csempeszet:
                bukas = random.random() < 0.20
                if bukas:
                    biro_birsag = 40000
                    st.session_state.penz -= (ut_koltseg + biro_birsag + extra_birsag)
                    st.error(f"🚨 Elkaptak a vámosok! Bírság: {biro_birsag:,} Ft.")
                    profit = -ut_koltseg - biro_birsag - extra_birsag
                else:
                    bevetel = int(mennyiseg * alap_ar * raktar_szorzó * 2)
                    profit = bevetel - ut_koltseg - extra_birsag
                    st.session_state.penz += profit
                    st.success(f"🥷 Sikerült a csempészet! Tiszta profit: **+{profit:,} Ft**")
            else:
                bevetel = int(mennyiseg * alap_ar * raktar_szorzó)
                if gyorshajtas and extra_birsag == 0:
                    bevetel = int(bevetel * 1.15) # Gyorshajtás bónusz, ha nem kapták el
                
                profit = bevetel - ut_koltseg - extra_birsag
                st.session_state.penz += profit
                
                if profit > 0:
                    st.success(f"🎉 Sikeres fuvar! Tiszta profit: **+{profit:,} Ft**")
                else:
                    st.warning(f"⚠️ Ráfizetéses fuvar! Veszteség: **{profit:,} Ft**")

            passziv_bevetel = (st.session_state.soforok_szama - 1) * 15000
            st.session_state.penz += passziv_bevetel

            # Időablak bónusz: Ha helyi fuvar volt, belefér egy extra fuvar (nem növekszik a nap)
            if tavolsag == 50 and random.random() < 0.40:
                st.info("⏱️ Kiváló időbeosztás! Az időablak miatt belefért egy extra helyi kör ezen a napon (a nap nem lépett tovább)!")
            else:
                st.session_state.kor += 1

            st.session_state.rivalis_penz += random.randint(40000, 85000)
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
