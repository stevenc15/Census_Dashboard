echo "Fetching Data"
python3 scripts/fetch_data.py

echo "Preprocessing data"
python3 scripts/preprocess_data.py

echo "Run App"
streamlit run app.py
&
echo "Pipeline complete"