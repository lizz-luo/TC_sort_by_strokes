import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="繁體中文筆畫排序工具", layout="wide")
st.title("繁體中文筆畫排序工具")

# 1. 讀取筆畫資料庫
@st.cache_data
def load_stroke_dict(uploaded_file):
    # 如果使用者有上傳檔案，優先使用上傳的檔案
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    # 否則嘗試讀取同目錄下的預設檔案 (請確保檔名為 strokes.csv)
    elif os.path.exists("strokes.csv"):
        df = pd.read_csv("strokes.csv")
    else:
        return None
    
    # 假設第一欄是「字」，第二欄是「筆畫數」
    char_col, stroke_col = df.columns[0], df.columns[1]
    # 轉換成字典 { '字': 筆畫數 }
    return dict(zip(df[char_col].astype(str), df[stroke_col].astype(int)))

st.sidebar.header("資料庫設定")
uploaded_csv = st.sidebar.file_uploader("上傳筆畫庫 CSV (可選，預設讀取 strokes.csv)", type=["csv"])
stroke_dict = load_stroke_dict(uploaded_csv)

if stroke_dict is None:
    st.warning("找不到筆畫資料庫！請在側邊欄上傳您的 CSV 檔案，或是將檔案命名為 `strokes.csv` 放在同一目錄下。")

# 2. 排序核心邏輯
def get_stroke_key(text):
    """
    將字串轉換為一組 tuple，例如 "你好" -> ((7, 20320), (6, 22909))
    Python 比較 tuple 時，會先比第一個元素，相同再比第二個，完美符合逐字排序需求。
    """
    key_tuple = []
    for char in text:
        # 若資料庫中找不到該字，預設筆畫數設為 999 (排到最後面)，並用 Unicode 碼位當第二排序鍵防呆
        strokes = stroke_dict.get(char, 999) 
        key_tuple.append((strokes, ord(char)))
    return tuple(key_tuple)

# 3. 介面佈局：輸入與輸出
col1, col2 = st.columns(2)

with col1:
    st.subheader("輸入區")
    input_text = st.text_area("請輸入要排序的文本（每行一筆資料）：", height=400)
    start_sort = st.button("開始排序", type="primary")

with col2:
    st.subheader("輸出區")
    if start_sort:
        if not stroke_dict:
            st.error("請先提供筆畫資料庫。")
        elif input_text.strip():
            # 將文本按換行符拆分，並過濾掉空白行
            lines = [line.strip() for line in input_text.split('\n') if line.strip()]
            
            # 執行排序
            sorted_lines = sorted(lines, key=get_stroke_key)
            
            # 將結果轉回換行字串並顯示
            output_text = '\n'.join(sorted_lines)
            st.text_area("排序結果：", value=output_text, height=400)
        else:
            st.info("請在左側輸入要排序的文本。")