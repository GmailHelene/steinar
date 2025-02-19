import streamlit as st
import openai
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

def hent_gpt_svar(prompt):
    """
    Forsøker å kalle openai.ChatCompletion.create (eksisterte i openai==0.28, 
    men var eksperimentelt). Du kan måtte bytte til 'gpt-3.5-turbo' 
    om 'gpt-4' ikke fungerer i 0.28.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Evt. "gpt-4" om du har tilgang, men usikkert i 0.28
            messages=[
                {"role": "system", "content": "Du er en ekspert på steinidentifikasjon."},
                {"role": "user", "content": prompt}
            ]
        )
        # Returner svaret fra første "choice"
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Feil ved henting av GPT-svar: {str(e)}"

# Test kall (i terminalen) - fjern eller kommenter ut hvis du ikke vil teste i Streamlit
if __name__ == "__main__":
    test_prompt = "Beskriv hvordan jeg kan identifisere obsidian."
    svar = hent_gpt_svar(test_prompt)
    print(svar)

# --- Streamlit UI ---
st.title("Stein- og Meteoritt-Identifikasjonssystem")
st.header("Kunnskapsbank og identifikasjon for sjeldne stener og meteoritter")

st.markdown("""
**Grunninformasjon:**

- **Stener** dekker alt fra vanlige, terrestriske bergarter til sjeldne meteoritter og verdifulle edelstener.
- **Terrestriske bergarter**: F.eks. granitt, basalt, sandstein og marmor.
- **Meteoritter**: Bergarter fra verdensrommet, ofte ekstremt gamle.
- **Edelstener**: Spesielt utvalgte steiner med høy estetisk og økonomisk verdi.
""")

valg = st.radio("Hva ønsker du å gjøre?", 
                ("Teste identifikasjonsveilederen ved å beskrive en funnet stein", 
                 "Velge en bestemt kategori"))

if valg == "Teste identifikasjonsveilederen ved å beskrive en funnet stein":
    st.subheader("Beskriv steinen du har funnet")
    bilde_fil = st.file_uploader("Last opp et bilde", type=["jpg", "jpeg", "png"])
    farge = st.text_input("Farge")
    storrelse = st.text_input("Størrelse (f.eks. 1x1 cm)")
    vekt = st.text_input("Vekt (f.eks. 1,1 gram)")
    detaljer = st.text_input("Andre detaljer")
    
    if st.button("Send"):
        bilde_info = bilde_fil.name if bilde_fil is not None else "Ingen bilde opplastet"
        prompt = (
            f"Jeg har funnet en stein med følgende egenskaper:\n"
            f"Bilde: {bilde_info}\n"
            f"Farge: {farge}\n"
            f"Størrelse: {storrelse}\n"
            f"Vekt: {vekt}\n"
            f"Andre detaljer: {detaljer}\n"
            "Gi en vurdering av hvilken type stein dette kan være, og foreslå tester for videre identifisering."
        )
        with st.spinner("Henter svar fra GPT..."):
            svar = hent_gpt_svar(prompt)
        st.success("Ferdig!")
        st.text_area("Resultat", value=svar, height=300)

elif valg == "Velge en bestemt kategori":
    st.subheader("Velg en kategori")
    kategori = st.selectbox("Velg en kategori", ("Terrestriske bergarter", "Meteoritter", "Edelstener"))
    
    if st.button("Send"):
        if kategori == "Terrestriske bergarter":
            prompt = ("Gi en oversikt over terrestriske bergarter. "
                      "Forklar at de deles inn i magmatiske, sedimentære og metamorfe bergarter, "
                      "og gi eksempler som granitt, basalt, sandstein og marmor.")
        elif kategori == "Meteoritter":
            prompt = ("Gi en oversikt over meteoritter. "
                      "Forklar at de er bergarter fra verdensrommet med underkategorier "
                      "som stein-, jern- og stein-jern meteoritter.")
        else:  # Edelstener
            prompt = ("Gi en oversikt over edelstener. "
                      "Forklar at de er spesielt utvalgte steiner med høy estetisk og økonomisk verdi.")
        
        with st.spinner("Henter svar fra GPT..."):
            svar = hent_gpt_svar(prompt)
        st.success("Ferdig!")
        st.text_area("Resultat", value=svar, height=300)

st.markdown("**Merk:** Denne koden er ment for openai==0.28, og ChatCompletion var eksperimentell i den versjonen.")


### Viktig:
# 1. Lag en requirements.txt med:
#    openai==0.28
#    streamlit
#    python-dotenv
#    ...
#
# 2. Installer med `pip install -r requirements.txt`
# 3. Kjør lokalt med: `streamlit run app.py`
# 4. Deploy til Streamlit Cloud ved å peke til dette repoet.
