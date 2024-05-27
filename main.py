import streamlit as st
import pandas as pd

def assign_interview_dates(df):
    # 評価に基づいてソート（A > B > C）
    df.sort_values(by='評価', ascending=False, inplace=True)
    
    # 割り当てられた日程を保持する辞書
    assigned_dates = {}
    
    # 各候補者の面接日を割り当てる
    for index, row in df.iterrows():
        name = row['名前']
        preferences = [row['第1候補日'], row['第2候補日'], row['第3候補日']]
        
        for date in preferences:
            if date not in assigned_dates:
                assigned_dates[date] = name
                break
   
    # 結果をDataFrameに変換
    results_df = pd.DataFrame(list(assigned_dates.items()), columns=['日付', '名前'])
    # 日付でソート
    results_df['日付'] = pd.to_datetime(results_df['日付'])  # 日付形式に変換
    results_df.sort_values(by='日付', inplace=True)

    return results_df

def main():
    st.title('面接日程割り当てアプリ')
    
    # ファイルアップロード
    uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        if st.button('面接日程を割り当てる'):
            result_df = assign_interview_dates(df)
            st.write('割り当て結果:')
            st.dataframe(result_df)

            # 結果をCSVフォーマットでダウンロード可能にする
            csv = result_df.to_csv(index=False).encode('utf-8')
            st.download_button(label="結果をCSVとしてダウンロード",
                               data=csv,
                               file_name='assigned_dates.csv',
                               mime='text/csv')
            
            # 結果をテキストとしてコピーするボタン
            text_results = result_df.to_csv(index=False, header=False, sep='\t')
            st.download_button(label="結果をコピー",
                               data=text_results,
                               file_name='results.txt',
                               mime='text/plain',
                               on_click=lambda: st.write("結果をコピーしました！"))

if __name__ == '__main__':
    main()