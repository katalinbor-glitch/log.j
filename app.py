import streamlit as st
import random

st.set_page_config(page_title="Logisztikai Tycoon: Logikai Kihívás", page_icon="🧩", layout="centered")

st.title("🧩 Logisztikai Tycoon: Logikai Kihívás")
st.markdown("Itt már észre is szükség van! Minden nap egy **specifikus megbízást** kapsz. Válaszd ki a tökéletes szállítóeszközt és stratégiát, különben büntetést fizetsz!")

if "indul" not in st.session_state:
    st.session_state.indul = False

if not st.session_state.indul:
    st.markdown("### 🏢 Új Vállalat Indítása")
    ceg_nev = st.text_input("Céged neve:", "LogiPro Kft.")
    
    if st.button("Induljon a kihívás! 🎯"):
        st.session_state.indul = True
        st.session_state.ceg_nev = ceg_nev
        st.session_state.penz = 120000
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
        st.success("A raktár bővült!")
        st.rerun()

    if st.session_state.penz >= 40000 and st.sidebar.button("⚡ Üzemanyag-takarékosság (40k Ft)"):
        st.session_state.penz -= 40000
        st.session_state.uzemanyag_kedvezmeny += 15
        st.success("Fejlesztés kész!")
        st.rerun()

    if st.session_state.kor <= 5:
        st.markdown(f"## 🗺️ {st.session_state.kor}. Nap: Napi Megbízás")

        # Véletlenszerűen generálunk egy feladatot a napra
        feladatok_lista = [
            {
                "cim": "🍅 Sürgős Friss Zöldség Szállítás",
                "leiras": "Helyi piacra kell vinni gyorsan romló árut. A távolság rövid (50 km), de nem szabad sokat tökölni, mert megromlik!",
                "ideális": "🚐 Helyi Furgon (Olcsó, stabil)",
                "tavolsag": 50,
                "alap_bevetel": 75000
            },
            {
                "cim": "🏭 Nehéz Ipari Alkatrészek Exportja",
                "leiras": "Nyugat-Európába (500 km) kell eljuttatni egy nagyobb adag közepes súlyú gyári gépet.",
                "ideális": "🚛 Nagy Teherautó (A győztes!)",
                "tavolsag": 500,
                "alap_bevetel": 190000
            },
            {
                "cim": "📦 Hatalmas Tengerentúli Konténer",
                "leiras": "Távolsági tömegáru a Távol-Keletre (3000 km). Csak a legnagyobb raktérrel rendelkező monstrum éri meg gazdaságosan!",
                "ideális": "🚢 Konténeres Hajó (Óriási raktér)",
                "tavolsag": 3000,
                "alap_bevetel": 550000
            },
            {
                "cim": "💎 Veszélyes & Villámgyors Orvosi Műszerek",
                "leiras": "Térítésmentes expressz út a Távol-Keletre (3000 km), de csak akkor kapod meg a prémium pénzt, ha azonnal odaér!",
                "ideális": "✈️ Cargo Repülő (Villámgyors)",
                "tavolsag": 3000,
                "alap_bevetel": 700000
            }
        ]

        # Minden naphoz sorsolunk egy feladatot a kor alapján, hogy konzisztens maradjon a körön belül
        random.seed(st.session_state.kor * 99)
        aktiv_feladat = random.choice(feladatok_lista)

        st.info(f"### {aktiv_feladat['cim']}\n{aktiv_feladat['leiras']}")

        jarmuvek = {
            "🚐 Helyi Furgon (Olcsó, stabil)": {"kapacitas": 20, "koltseg_km": 40},
            "🚛 Nagy Teherautó (A győztes!)": {"kapacitas": 60, "koltseg_km": 120},
            "🚢 Konténeres Hajó (Óriási raktér)": {"kapacitas": 150, "koltseg_km": 280},
            "✈️ Cargo Repülő (Villámgyors)": {"kapacitas": 80, "koltseg_km": 650}
        }

        valasztott_jarmu = st.selectbox("Válaszd ki a feladathoz illő szállítóeszközt:", list(jarmuvek.keys()))
        j = jarmuvek[valasztott_jarmu]

        mennyiseg = st.slider("Mennyi árut pakolsz be?", 1, j["kapacitas"], 15)
        gyorshajtas = st.checkbox("⚡ Sietsz a határidő miatt? (Extra rizikó és sebesség)")

        if st.button("🚀 Megbízás teljesítése!", type="primary"):
            tavolsag = aktiv_feladat["tavolsag"]
            alap_koltseg = tavolsag * j["koltseg_km"]
            kedvezmeny_faktor = (100 - st.session_state.uzemanyag_kedvezmeny) / 100
            ut_koltseg = int(alap_koltseg * kedvezmeny_faktor)

            # Ellenőrzés, hogy eltalálta-e az ideális járművet
            helyes_jarmu = (valasztott_jarmu == aktiv_feladat["ideális"])

            extra_birsag = 0
            if gyorshajtas and random.random() < 0.30:
                extra_birsag = 35000
                st.error("📸 Traffipax elkapott a gyorshajtásért! -35,000 Ft bírság.")

            raktar_szorzó = 1 + (st.session_state.raktar_szint - 1) * 0.15

            if helyes_jarmu:
                bevetel = int(aktiv_feladat["alap_bevetel"] * raktar_szorzó)
                if gyorshajtas and extra_birsag == 0:
                    bevetel = int(bevetel * 1.2) # Bónusz a gyorsaságért
                
                profit = bevetel - ut_koltseg - extra_birsag
                st.session_state.penz += profit
                st.success(f"🎯 **Tökéletes járműválasztás!** A megbízó megelégedett. Tiszta profit: **+{profit:,} Ft**")
            else:
                # Rossz jármű választás büntetése
                vesztesseg_birsag = 60000
                st.session_state.penz -= (ut_koltseg + vesztesseg_birsag)
                profit = -ut_koltseg - vesztesseg_birsag
                st.error(f"❌ **Rossz logisztikai döntés!** Ez a jármű alkalmatlan volt erre a feladatra (vagy túl drága volt fenntartani). Útiköltség + 60k kártérítési kötbér! Veszteség: **{profit:,} Ft**")

            passziv_bevetel = (st.session_state.soforok_szama - 1) * 15000
            st.session_state.penz += passziv_bevetel

            # Rivális okosabban növekszik
            st.session_state.rivalis_penz += random.randint(50000, 95000)
            st.session_state.kor += 1
            st.rerun()

    else:
        st.balloons()
        st.markdown("# 🏆 Vége a 5 napos logisztikai kihívásnak!")
        st.markdown(f"### A te céged tőkéje: **{st.session_state.penz:,} Ft**")
        st.markdown(f"### A rivális MegaLog Kft. tőkéje: **{st.session_state.rivalis_penz:,} Ft**")

        if st.session_state.penz > st.session_state.rivalis_penz:
            st.success("🥇 Zseniális logisztikai menedzser vagy! Te nyertél!")
        else:
            st.error("🥈 A MegaLog Kft. jobban elemezte a feladatokat. Próbáld újra!")

        if st.button("🔄 Új játék indítása"):
            st.session_state.indul = False
            st.rerun()
