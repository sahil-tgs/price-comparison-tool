Setup:
1. clone repo
2. ``` cd price-comparison-tool ```
3. create .venv ``` python3 -m venv .venv ```
4. Activate .venv ``` source venv/bin/activate ``` for linux or ``` .\venv\Scripts\activate ``` for windows
5. run: ``` pip install -r requirements.txt ```
6. run: ``` playwright install chromium ```
7. make 2 terminals, one for streamlit and other for fastAPI
8. run fastAPI backend: ``` python -m app.main ```
9. run streamlit: ``` streamlit run streamlit_app.py ```
