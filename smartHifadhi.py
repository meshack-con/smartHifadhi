import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai

# ==========================================
# 1. SETUP & CONFIGURATION
# ==========================================
st.set_page_config(page_title="Smart-Hifadhi AI Hub", layout="wide")

# API Keys
API_KEY = "AIzaSyBfbbjW6osrLr-MsRdNlju-aERfYdzkaWk"
genai.configure(api_key=API_KEY)

URL = "https://bzolhpmorjkdjfaotjgg.supabase.co"
KEY = "sb_publishable_DQIXCrVzqf-OPtZBnouoGA_FkroIASY"

st.markdown("""
    <style>
        .block-container { padding: 0rem !important; }
        header, footer { visibility: hidden !important; }
        .main { background-color: #f8fafc; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. DASHBOARD HTML (Miamala, Kutoa & Purchase)
# ==========================================
html_code = f"""
<!DOCTYPE html>
<html lang="sw">
<head>
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {{ --primary: #4361ee; --success: #2ecc71; --danger: #e74c3c; --dark: #0f172a; --ai: #f1c40f; }}
        body {{ font-family: 'Inter', sans-serif; background: #f8fafc; margin: 0; padding: 10px; }}
        .nav {{ background: var(--dark); color: white; padding: 15px 25px; border-radius: 12px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }}
        .grid-stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; margin-bottom: 20px; }}
        .stat-card {{ background: white; padding: 15px; border-radius: 12px; text-align: center; box-shadow: 0 2px 5px rgba(0,0,0,0.05); border-bottom: 4px solid var(--primary); }}
        .amount {{ font-size: 1.4rem; font-weight: 800; display: block; }}
        .layout {{ display: grid; grid-template-columns: 1fr 1.6fr; gap: 20px; }}
        .card {{ background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }}
        input, select {{ width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box; }}
        .btn {{ width: 100%; padding: 12px; border: none; border-radius: 8px; color: white; font-weight: bold; cursor: pointer; margin-top: 10px; }}
        h4 {{ margin: 0 0 10px 0; color: #64748b; font-size: 0.8rem; text-transform: uppercase; }}
    </style>
</head>
<body>
    <div class="nav">
        <div style="font-weight: 800;">SMART-HIFADHI AI HUB 💎</div>
        <div id="status">Syncing...</div>
    </div>

    <div class="grid-stats">
        <div class="stat-card" style="border-color:var(--success)">INVEST<br><span class="amount" id="s1">0</span></div>
        <div class="stat-card" style="border-color:var(--primary)">ESSENTIALS<br><span class="amount" id="s2">0</span></div>
        <div class="stat-card" style="border-color:var(--ai)">LIFESTYLE<br><span class="amount" id="s3">0</span></div>
        <div class="stat-card" style="border-color:var(--danger)">EMERGENCY<br><span class="amount" id="s4">0</span></div>
    </div>

    <div class="layout">
        <div class="card">
            <h4>💰 Miamala & Manunuzi</h4>
            <input type="number" id="amt" placeholder="Kiasi cha Pesa">
            <button class="btn" style="background:var(--success)" onclick="addMoney()">WEKA MAPATO (GAWA)</button>
            
            <hr style="margin:20px 0; border:0.5px solid #eee">
            
            <select id="acc_type">
                <option value="invest_acc">Uwekezaji</option>
                <option value="essential_acc">Lazima</option>
                <option value="life_acc">Lifestyle</option>
                <option value="emergency_acc">Dharura</option>
            </select>
            <input type="number" id="w_amt" placeholder="Kiasi cha kutoa">
            <button class="btn" style="background:var(--danger)" onclick="withdraw()">KUTOA / PURCHASE</button>
        </div>

        <div class="card">
            <h4>📊 Financial Analysis Chart</h4>
            <div style="height: 320px;"><canvas id="hubChart"></canvas></div>
        </div>
    </div>

<script>
    let _sup; let bal = {{}};
    window.onload = () => {{ _sup = supabase.createClient("{URL}", "{KEY}"); refresh(); }};

    async function refresh() {{
        const {{ data }} = await _sup.from('balances').select('*').limit(1);
        if(data && data.length) {{
            bal = data[0];
            const f = n => new Intl.NumberFormat().format(Math.round(n));
            document.getElementById('s1').innerText = f(bal.invest_acc);
            document.getElementById('s2').innerText = f(bal.essential_acc);
            document.getElementById('s3').innerText = f(bal.life_acc);
            document.getElementById('s4').innerText = f(bal.emergency_acc);
            updateChart(bal);
            document.getElementById('status').innerText = "Live Database ✅";
        }}
    }}

    async function addMoney() {{
        const v = parseFloat(document.getElementById('amt').value); if(!v) return;
        const upd = {{ 
            invest_acc:(bal.invest_acc||0)+(v*0.5), 
            essential_acc:(bal.essential_acc||0)+(v*0.2), 
            life_acc:(bal.life_acc||0)+(v*0.1), 
            emergency_acc:(bal.emergency_acc||0)+(v*0.1), 
            tithe_acc:(bal.tithe_acc||0)+(v*0.1) 
        }};
        await _sup.from('balances').update(upd).eq('id', bal.id);
        location.reload();
    }}

    async function withdraw() {{
        const acc = document.getElementById('acc_type').value;
        const v = parseFloat(document.getElementById('w_amt').value);
        if(!v || v > bal[acc]) {{ alert("Salio halitoshi au kiasi si sahihi!"); return; }}
        const upd = {{ [acc]: bal[acc] - v }};
        await _sup.from('balances').update(upd).eq('id', bal.id);
        location.reload();
    }}

    function updateChart(b) {{
        new Chart(document.getElementById('hubChart'), {{
            type: 'doughnut',
            data: {{
                labels: ['Invest', 'Essentials', 'Life', 'Emergency', 'Tithe'],
                datasets: [{{
                    data: [b.invest_acc, b.essential_acc, b.life_acc, b.emergency_acc, b.tithe_acc],
                    backgroundColor: ['#2ecc71', '#4361ee', '#f1c40f', '#e74c3c', '#9b59b6']
                }}]
            }},
            options: {{ maintainAspectRatio: false }}
        }});
    }}
</script>
</body>
</html>
"""
components.html(html_code, height=620)

# ==========================================
# 3. AI HUB: PREDICTION, ANALYSIS & ADVICE
# ==========================================
st.divider()
st.subheader("🧠 Smart-Hifadhi AI Analysis Hub")

# Sehemu ya Kuchagua Kazi ya AI
option = st.selectbox("Chagua Kazi ya AI:", 
                      ["Uchambuzi wa Matumizi (Analysis)", 
                       "Utabiri wa Akiba ya Baadaye (Prediction)", 
                       "Ushauri wa Kifedha (Financial Advice)"])

if "ai_messages" not in st.session_state:
    st.session_state.ai_messages = []

# Kuchakata AI
if st.button("Anza Uchambuzi wa AI"):
    with st.spinner("AI Hub inasoma data zako halisi..."):
        try:
            # Tafuta modeli
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            selected_model = next((m for m in available_models if 'flash' in m), available_models[0])
            model = genai.GenerativeModel(selected_model)

            # Context ya AI (System Instruction)
            base_prompt = f"Wewe ni Smart-Hifadhi AI Hub. Kazi yako ni kufanya {option}. "
            
            if option == "Uchambuzi wa Matumizi (Analysis)":
                task_prompt = "Chambua mgao wa 50/20/10/10/10 na uniambie kama matumizi yangu ni salama."
            elif option == "Utabiri wa Akiba ya Baadaye (Prediction)":
                task_prompt = "Kama nitaendelea kuweka kiasi hiki kila mwezi, nitakuwa na kiasi gani baada ya miezi 6? Tabiri maendeleo yangu."
            else:
                task_prompt = "Nipe ushauri wa kibiashara na uwekezaji kulingana na salio langu la sasa."

            response = model.generate_content(f"{base_prompt}\n{task_prompt}. Jibu kwa Kiswahili fasaha na kifupi.")
            st.info(response.text)
            
        except Exception as e:
            st.error(f"Hitilafu: {str(e)}")

# Chat Input kwa maswali mengine
st.write("---")
if user_query := st.chat_input("Uliza swali lolote kuhusu bajeti yako..."):
    with st.chat_message("user"): st.write(user_query)
    with st.chat_message("assistant"):
        try:
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            selected_model = next((m for m in available_models if 'flash' in m), available_models[0])
            model = genai.GenerativeModel(selected_model)
            
            res = model.generate_content(f"Mtumiaji anasema: {user_query}. Jibu kama mshauri wa fedha kwa Kiswahili.")
            st.write(res.text)
        except:
            st.error("AI imeshindwa kuunganisha.")