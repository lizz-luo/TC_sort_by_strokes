import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="繁體中文筆畫排序工具", layout="wide")
st.title("繁體中文筆畫排序工具")

st.markdown("""
> 本工具資料取自[粵語審音配字庫筆畫表](https://humanum.arts.cuhk.edu.hk/Lexis/lexi-can/)。  
> 本工具可將漢字按筆劃數排序，當首字筆劃數相同時，會排序第二個字，以此類推。
""")
st.divider()

@st.cache_data
def load_stroke_dict():
    if os.path.exists("strokes.csv"):
        df = pd.read_csv("strokes.csv")
        char_col, stroke_col = df.columns[0], df.columns[1]
        return dict(zip(df[char_col].astype(str), df[stroke_col].astype(int)))
    else:
        return None

stroke_dict = load_stroke_dict()

if stroke_dict is None:
    st.error("找不到筆畫資料庫！請確保 `strokes.csv` 檔案已經放在與程式相同的目錄下。")
    st.stop()

# ⚠️ 修正後的核心邏輯
def get_stroke_key(text):
    """
    先提取所有字的筆畫數組成一個 tuple，再提取所有字的 Unicode 組成另一個 tuple。
    Python 排序時，會優先把「整串筆畫序列」比對完，
    筆畫序列完全平手時，才會去看 Unicode 序列。
    """
    strokes = []
    unicodes = []
    for char in text:
        # 找不到的字預設為 999 畫，排到最後
        strokes.append(stroke_dict.get(char, 999))
        unicodes.append(ord(char))
        
    # 回傳格式：( (筆畫1, 筆畫2...), (Unicode1, Unicode2...) )
    return (tuple(strokes), tuple(unicodes))

col1, col2 = st.columns(2)

with col1:
    st.subheader("輸入區")
    input_text = st.text_area("請輸入要排序的文本（每行一筆資料）：", height=400)
    start_sort = st.button("開始排序", type="primary", use_container_width=True)

with col2:
    st.subheader("輸出區")
    if start_sort:
        if input_text.strip():
            lines = [line.strip() for line in input_text.split('\n') if line.strip()]
            sorted_lines = sorted(lines, key=get_stroke_key)
            output_text = '\n'.join(sorted_lines)
            
            st.success("排序完成！請點擊下方代碼區塊右上角的 📋 圖示一鍵複製結果。")
            st.code(output_text, language="plaintext")
        else:
            st.info("請在左側輸入要排序的文本。")
