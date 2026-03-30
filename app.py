import streamlit as st
import pandas as pd
import os

# 設定網頁標題與寬版顯示
st.set_page_config(page_title="繁體中文筆畫排序工具", layout="wide")

# 加上 Emoji 讓標題看起來更輕鬆活潑 🎉
st.title("📚 繁體中文筆畫排序工具 ✨")

# 依照要求加入來源註釋與規則說明
st.markdown("""
> 📖 **資料來源**：本工具資料取自[粵語審音配字庫筆畫表](https://humanum.arts.cuhk.edu.hk/Lexis/lexi-can/)。  
> 🔢 **排序規則**：本工具可將漢字按筆劃數排序，當首字筆劃數相同時，會排序第二個字，以此類推。
""")
st.divider() # 加上一條分隔線讓版面更整齊

# 1. 讀取筆畫資料庫 (默默在背景讀取 strokes.csv 📂)
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
    st.error("🚨 找不到筆畫資料庫！請確保 `strokes.csv` 檔案已經放在與程式相同的目錄下。")
    st.stop()

# 2. 排序核心邏輯 🧠
def get_stroke_key(text):
    key_tuple = []
    for char in text:
        strokes = stroke_dict.get(char, 999) 
        key_tuple.append((strokes, ord(char)))
    return tuple(key_tuple)

# 3. 介面佈局：確保左右完美對齊 ⚖️
col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 輸入區")
    # 使用 label_visibility="collapsed" 隱藏標籤，讓輸入框與標題的距離更緊湊完美
    input_text = st.text_area(
        "輸入區隱藏標籤", 
        height=400, 
        label_visibility="collapsed", 
        placeholder="請在此輸入要排序的文字，每行一筆資料...\n\n例如：\n蘋果\n香蕉\n西瓜"
    )
    start_sort = st.button("🪄 開始排序", type="primary", use_container_width=True)

with col2:
    st.subheader("📋 輸出區")
    
    # 根據是否點擊排序，決定輸出區顯示的內容
    if start_sort:
        if input_text.strip():
            lines = [line.strip() for line in input_text.split('\n') if line.strip()]
            sorted_lines = sorted(lines, key=get_stroke_key)
            output_text = '\n'.join(sorted_lines)
            
            # 輸出框 (字號與高度和輸入區完全一致！)
            st.text_area("輸出區隱藏標籤", value=output_text, height=400, label_visibility="collapsed")
            st.success("🎉 排序完成！請點擊上方文字框，全選 (Ctrl+A / ⌘+A) 並複製內容 ✨")
        else:
            # 輸入為空時的防呆顯示
            st.text_area("輸出區隱藏標籤", value="", height=400, label_visibility="collapsed", placeholder="等待輸入中... 😴")
            st.warning("💡 請先在左側輸入要排序的文本喔！")
    else:
        # 預設狀態也顯示等高的 text_area，保持版面左右絕對對齊
        st.text_area("輸出區隱藏標籤", value="", height=400, label_visibility="collapsed", placeholder="排序後的結果會顯示在這裡 🌟")
        st.info("👈 請在左側輸入文字，然後點擊下方「開始排序」按鈕")