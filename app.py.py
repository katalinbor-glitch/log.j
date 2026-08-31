import streamlit as st
import random

st.set_page_config(page_title="Global Profitability - Ultimátum", page_icon="🌐", layout="centered")

st.title("🌐 Global Profitability - Nemzetközi Logisztikai Birodalom")
st.markdown("Importálj külföldről, kezeld az árfolyamkockázatot, vegyél fel hiteleket és előzd meg a versenytársat!")

if "jatek_indul" not in st.session_state:
    st.session_state.jatek_indul = False

if not st.session_state.jatek_indul:
    st.header("⚙️ Játék beállításai és vállalegalapítás")
    nev = st.text_input("Vállalatod neve:", "Global Trans Kft.")
    szint = st.selectbox("Nehézségi szint:", ["Kezdő (Belföld + EU)", "Haladó (Globális piac + Árfolyamok)", "Profi Guru (Minden akadály + Magas kockázat)"])
    
    if st.button("Vállalat indítása! 🚀"):
        st.session_state.jatek_indul = True
        st.session_state.nev = nev
        st.session_state.szint = szint
        st.session_state.nap = 1
        st.session_state.jatek_vege = False
        st.session_state.hitel = 0
        
        if "Kezdő" in szint:
            st.session_state.penz = 45000
            st.session_state.ai_penz = 25000
            st.session_state.kockazat_szorzo = 0.5
        elif "Haladó" in szint:
            st.session_state.penz = 35000
            st.session_state.ai_penz = 35000
            st.session_state.kockazat_szorzo = 1.0
        else:
            st.session_state.penz = 25000
            st.session_state.ai_penz = 45000
            st.session_state.kockazat_szorzo = 1.6
            
        st.session_state.keszlet = 0
        st.session_state.jarmu_szint = 1
        st.session_state.jarmu_kapacitas = 4
        st.rerun()

else:
    # Raktárak (egyes helyeken az árak EUR-ban vagy USD-ben vannak megadva a nemzetközi jelleg miatt)
    raktarak = {
        "Budapest (Belföld)": {"tavolsag": 20, "ar": 300, "valuta": "HUF", "vam": 0.0},
        "Bécs (Ausztria)": {"tavolsag": 250, "ar": 0.8, "valuta": "EUR", "vam": 0.05},
        "Frankfurt (Németország)": {"tavolsag": 900, "ar": 0.65, "valuta": "EUR", "vam": 0.12},
        "Sanghaj (Kína - Globális)": {"tavolsag": 3000, "ar": 0.85, "valuta": "USD", "vam": 0.25}
    }
    
    uzemanyag_km = 10
    raktar_koltseg = 45

    # Oldalsáv statisztikák
    st.sidebar.header(f"🏢 {st.session_state.nev}")
    st.sidebar.text(f"Szint: {st.session_state.szint}")
    st.sidebar.metric(label="Aktuális Nap", value=f"{st.session_state.nap} / 7")
    st.sidebar.metric(label="Pénztárca", value=f"{st.session_state.penz:,} Ft")
    st.sidebar.metric(label="Aktuális Hitel", value=f"{st.session_state.hitel:,} Ft")
    st.sidebar.metric(label="Raktárkészlet", value=f"{st.session_state.keszlet} db")
    st.sidebar.metric(label="Flotta kapacitás", value=f"{st.session_state.jarmu_kapacitas} db")
    st.sidebar.metric(label="AI Konkurens tőkéje", value=f"{st.session_state.ai_penz:,} Ft")

    if not st.session_state.jatek_vege:
        st.subheader(f"--- {st.session_state.nap}. NAPI NEMZETKÖZI OPERÁCIÓ ---")
        
        # 1. Napi árfolyamok és piaci trend generálása
        eur_arfolyam = random.randint(380, 420)  # 1 EUR = X HUF
        usd_arfolyam = random.randint(350, 390)  # 1 USD = X HUF
        eladasi_ar = random.choice([600, 650, 700, 750]) # Piaci eladási ár HUF-ban
        
        st.info(f"💱 **Deviza- és Piaci Indexek:** 1 EUR = **{eur_arfolyam} Ft** | 1 USD = **{usd_arfolyam} Ft** | Mai eladási ár: **{eladasi_ar} Ft/db**")

        # 2. Hitelkezelés (kamatfizetés és felvétel)
        if st.session_state.hitel > 0:
            kamat = int(st.session_state.hitel * 0.1)
            st.session_state.penz -= kamat
            st.warning(f"🏦 Banki hitel utáni napi kamat levonva: {kamat} Ft")

        col1, col2 = st.columns(2)
        with col1:
            if st.session_state.hitel == 0 and st.button("Hitelt veszek fel (15 000 Ft)"):
                st.session_state.hitel += 15000
                st.session_state.penz += 15000
                st.rerun()
        with col2:
            if st.session_state.hitel >= 5000 and st.button("Törlesztek 5 000 Ft-ot"):
                if st.session_state.penz >= 5000:
                    st.session_state.hitel -= 5000
                    st.session_state.penz -= 5000
                    st.rerun()
                else:
                    st.error("Nincs elég pénzed a törlesztéshez!")

        # 3. Flottafejlesztés
        if st.session_state.jarmu_szint < 3 and st.session_state.penz >= 15000:
            if st.button("🚛 Flotta fejlesztése (Ár: 15 000 Ft, +6 kapacitás)"):
                st.session_state.penz -= 15000
                st.session_state.jarmu_szint += 1
                st.session_state.jarmu_kapacitas += 6
                st.success("Sikeres flottafejlesztés!")
                st.rerun()

        # 4. Raktárválasztás és rendelés
        valasztott_raktar = st.selectbox("Válassz beszállítói raktárat:", ["Kihagyom"] + list(raktarak.keys()))
        
        rendeles = 0
        if valasztott_raktar != "Kihagyom":
            rendeles = st.slider("Mennyi árut rendelsz?", 1, st.session_state.jarmu_kapacitas, 1)

        if st.button("Nap lezárása és fuvar indítása 👉"):
            # AI konkurens lépése
            ai_eladott = random.randint(20, 35)
            st.session_state.ai_penz += (ai_eladott * eladasi_ar) - random.randint(4000, 7000)

            # Beszerzés feldolgozása valutákkal
            if valasztott_raktar != "Kihagyom":
                r_info = raktarak[valasztott_raktar]
                
                # Ár kiszámítása HUF-ra konvertálva
                if r_info["valuta"] == "EUR":
                    egyseg_ar_huf = r_info["ar"] * eur_arfolyam
                elif r_info["valuta"] == "USD":
                    egyseg_ar_huf = r_info["ar"] * usd_arfolyam
                else:
                    egyseg_ar_huf = r_info["ar"]
                
                ar_koltseg = rendeles * egyseg_ar_huf
                ut_koltseg = r_info["tavolsag"] * 2 * uzemanyag_km
                osszes_kiadas = ar_koltseg + ut_koltseg

                if osszes_kiadas > st.session_state.penz:
                    st.error("Nincs elegendő tőke a nemzetközi fuvarhoz! Rendelés törölve.")
                else:
                    st.session_state.penz -= osszes_kiadas
                    
                    # Vámkezelési és logisztikai akadályok (sérülés/késés)
                    kockazat = r_info["vam"] * st.session_state.kockazat_szorzo
                    problemas = sum(1 for _ in range(rendeles) if random.random() < kockazat)
                    sikeres_aru = rendeles - problemas
                    
                    if problemas > 0:
                        st.warning(f"⚠️ Vámkezelési vagy szállítási hiba miatt {problemas} db áru kárba veszett / csúszott!")
                    
                    st.session_state.keszlet += sikeres_aru

            # Piaci kiszolgálás
            kereslet = random.randint(20, 40)
            eladott = min(st.session_state.keszlet, kereslet)
            bevetel = eladott * eladasi_ar
            st.session_state.penz += bevetel
            st.session_state.keszlet -= eladott

            # Raktározási költség
            r_koltseg = st.session_state.keszlet * raktar_koltseg
            st.session_state.penz -= r_koltseg

            st.write(f"✅ **Eladott mennyiség:** {eladott} db | **Bevétel:** {bevetel:,} Ft")
            st.write(f"📦 **Raktározási költség:** {r_koltseg} Ft")

            if st.session_state.nap >= 7:
                st.session_state.jatek_vege = True
            else:
                st.session_state.nap += 1
            
            st.rerun()

    else:
        st.balloons()
        st.header("🏆 Nemzetközi Játék Vége!")
        st.write(f"A te vállalatod tőkéje ({st.session_state.nev}): **{st.session_state.penz:,} Ft**")
        st.write(f"A versenytárs tőkéje: **{st.session_state.ai_penz:,} Ft**")
        
        if st.session_state.penz > st.session_state.ai_penz:
            st.success("🎉 Óriási győzelem! Te vagy a globális logisztikai piac királya!")
        else:
            st.warning("🥈 A versenytárs jobban gazdálkodott a devizákkal és a raktárakkal. Próbáld újra!")

        if st.button("Új játék indítása"):
            st.session_state.jatek_indul = False
            st.rerun()