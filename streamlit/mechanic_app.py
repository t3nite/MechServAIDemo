import streamlit as st
import json
import requests
from pathlib import Path

JOBS_FILE = Path("active_jobs.json")

# FastAPI endpoint kuittaukseen
MECHANIC_API_COMPLETE_URL = "http://localhost:8000/jobs/complete"


def load_active_jobs():
    if not JOBS_FILE.exists():
        return []

    raw = JOBS_FILE.read_bytes()

    for enc in ("utf-8", "cp1252", "latin-1"):
        try:
            txt = raw.decode(enc)
            if not txt.strip():
                return []
            data = json.loads(txt)

            # jos tiedosto oli “väärässä” enkoodauksessa, korjaa se heti UTF-8:ksi
            if enc != "utf-8":
                JOBS_FILE.write_text(
                    json.dumps(data, indent=4, ensure_ascii=False),
                    encoding="utf-8",
                    newline="\n",
                )

            return data if isinstance(data, list) else []
        except Exception:
            continue

    st.error("active_jobs.json on rikki / väärässä merkistössä eikä sitä saatu luettua.")
    return []


def save_active_jobs(jobs):
    JOBS_FILE.write_text(
        json.dumps(jobs, indent=4, ensure_ascii=False),
        encoding="utf-8",
        newline="\n",
    )


st.set_page_config(page_title="MechServAI - Mekaanikko", layout="wide", page_icon="🔧")
st.title("🔧 Mekaanikon Työjono")

active_jobs = load_active_jobs()

if not active_jobs:
    st.info("Ei uusia huoltopyyntöjä.")
else:
    for idx, job in enumerate(active_jobs):
        if not isinstance(job, dict):
            continue
        if "vehicle_make" not in job:
            # ignoraa mahdolliset roskaobjektit
            continue

        make = job.get("vehicle_make", "?")
        model = job.get("vehicle_model", "?")
        year = job.get("year", "?")
        plate = job.get("plate_number", "?")

        with st.expander(f"TYÖ #{job.get('id', idx)}: {make} {model} ({year}) - {plate}"):
            st.write(f"**Asiakas:** {job.get('customer_name', '-')}")
            st.write(f"**Työ:** {job.get('operation_code','-')} - {job.get('description','-')}")
            st.write(f"**Mekaanikko:** {job.get('mechanic', 'Ei määritelty')}")
            st.write(f"**Bay/Lift:** {job.get('bay_lift', 'Ei määritelty')}")
            st.write(f"**Kesto:** {job.get('duration_min', 0)} min")
            st.write(f"**Työn hinta:** {job.get('labor_total_brutto',0)/100:.2f} €")
            st.write(f"**Osien hinta:** {job.get('parts_total_brutto',0)/100:.2f} €")
            st.write(f"**Yhteensä:** {job.get('total_price_brutto',0)/100:.2f} €")

            parts = job.get("parts", []) or []
            if parts:
                st.subheader("Osat:")
                for part in parts:
                    if not isinstance(part, dict):
                        continue
                    st.write(
                        f"- {part.get('name','?')} ({part.get('brand','?')}): "
                        f"{part.get('price_brutto',0)/100:.2f} €"
                    )

            notes = st.text_area(
                "Mekaanikon havainnot:",
                value=job.get("notes", "") or "",
                key=f"notes_{job.get('id', idx)}",
                height=120,
            )

            if st.button("✅ Merkitse valmiiksi", key=f"btn_{job.get('id', idx)}"):
                job_id = job.get("id")
                if not job_id:
                    st.error("Työltä puuttuu id.")
                    st.stop()

                try:
                    r = requests.post(
                        MECHANIC_API_COMPLETE_URL,
                        json={
                            "id": str(job_id),
                            "notes": notes,
                            "completed_by": job.get("mechanic"),
                        },
                        timeout=10,
                    )

                    if r.status_code == 200:
                        try:
                            res = r.json()
                        except Exception:
                            st.error(f"Kuittaus epäonnistui: {r.text}")
                            st.stop()

                        if res.get("status") == "ok":
                            st.success("Työ kuitattu valmiiksi ja tallennettu.")
                            st.rerun()
                        else:
                            st.error(f"Kuittaus epäonnistui: {res}")
                    else:
                        st.error(f"Kuittaus epäonnistui: {r.status_code} {r.text}")

                except Exception as e:
                    st.error(f"Yhteysvirhe kuittauksessa: {e}")
