import pandas  as pd

df = pd.read_excel('/Users/huangjack/PycharmProjects/codeformyself/pandas处理数据/tripadvisor_booking.xlsx')
print(df)
df['new_line'] = df['booking_url'].agg(lambda x: x.split('?')[0])
df.to_csv('new_excel.csv')
print(df['new_line'])
