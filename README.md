# CIS Internet QoS Dashboard

This project provides a public dashboard comparing internet quality indicators (QoS) across CIS countries, powered by data from Speedtest.net.

## Features
- Automated monthly data update (1st of each month, 1 PM Baku time)
- Interactive dashboard (Streamlit + Plotly)
- Easy deployment to Streamlit Community Cloud (free!)

---

## 1. Upload Files to GitHub
1. Create a new repository on GitHub.
2. Upload these files to your repo:
   - `dashboard.py`
   - `update_cis_data.py`
   - `cis_new` (your data file)
   - `requirements.txt`
   - `.streamlit/schedules.yaml` (see below)

---

## 2. Deploy to Streamlit Community Cloud
1. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud) and sign in with GitHub.
2. Click "New app", select your repo, and set `dashboard.py` as the entry point.
3. Click "Deploy". Your dashboard will be live at a public URL!

---

## 3. Automated Data Update (Scheduled)
Streamlit Community Cloud supports scheduled execution. This project is set to run `update_cis_data.py` automatically at 1 PM Baku time (UTC+4) on the 1st day of each month.

### How it works:
- The schedule is configured in `.streamlit/schedules.yaml` (already provided).
- On schedule, `update_cis_data.py` runs and updates `cis_new`.
- The dashboard always displays the latest data.

---

## 4. Manual Update (Optional)
If you want to update the data manually:
1. Run `update_cis_data.py` locally.
2. Commit and push the new `cis_new` file to GitHub.
3. Your dashboard will reflect the update.

---

## 5. Local Development
To run locally:
```bash
pip install -r requirements.txt
streamlit run dashboard.py
```

---

## 6. Support
If you need help, visit the [Streamlit docs](https://docs.streamlit.io/) or contact your project maintainer.
