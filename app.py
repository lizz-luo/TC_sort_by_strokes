import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="繁體中文筆畫排序工具", layout="wide")
st.title("繁體中文筆畫排序工具")

# 加入頁面註釋與資料來源聲明
st.markdown("""
> 本工具資料取自[粵語審音配字庫筆畫表](https://humanum.arts.cuhk.edu.hk/Lexis/lexi-can/)。  
> 本工具可將漢字按筆劃數排序，當首字筆劃數相同時，會排序第二個字，以此類推。
""")
st.divider() # 加上一條分隔線讓版面更整齊

# 1. 讀取筆畫資料庫 (預設唯讀 strokes.csv)
@st.cache_data
def load_stroke_dict():
    # 檢查檔案是否存在
    if os.path.exists("strokes.csv"):
        df = pd.read_csv("strokes.csv")
        # 假設第一欄是「字」，第二欄是「筆畫數」
        char_col, stroke_col = df.columns[0], df.columns[1]
        # 轉換成字典 { '字': 筆畫數 }
        return dict(zip(df[char_col].astype(str), df[stroke_col].astype(int)))
    else:
        return None

stroke_dict = load_stroke_dict()

# 若找不到資料庫，顯示錯誤並停止後續程式執行
if stroke_dict is None:
    st.error("找不到筆畫資料庫！請確保 `strokes.csv` 檔案已經放在與程式相同的目錄下。")
    st.stop()

# 2. 排序核心邏輯
def get_stroke_key(text):
    """
    將字串轉換為一組 tuple 來逐字比對。
    找不到的字預設筆畫設為 999，並以 Unicode 碼位輔助排序。
    """
    key_tuple = []
    for char in text:
        strokes = stroke_dict.get(char, 999) 
        key_tuple.append((strokes, ord(char)))
    return tuple(key_tuple)

# 3. 介面佈局：輸入與輸出
col1, col2 = st.columns(2)

with col1:
    st.subheader("輸入區")
    input_text = st.text_area("請輸入要排序的文本（每行一筆資料）：", height=400)
    start_sort = st.button("開始排序", type="primary", use_container_width=True)

with col2:
    st.subheader("輸出區")
    if start_sort:
        if input_text.strip():
            # 將文本按換行符拆分，並過濾掉空白行
            lines = [line.strip() for line in input_text.split('\n') if line.strip()]
            
            # 執行排序
            sorted_lines = sorted(lines, key=get_stroke_key)
            
            # 將結果轉回換行字串
            output_text = '\n'.join(sorted_lines)
            
            # 顯示結果與複製功能
            st.success("排序完成！請點擊下方代碼區塊 **右上角的 📋 圖示** 一鍵複製結果。")
            st.code(output_text, language="plaintext")
        else:
            st.info("請在左側輸入要排序的文本。")