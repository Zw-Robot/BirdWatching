import pandas as pd
df1 = pd.read_excel(r"C:\Users\Robot\Desktop\附件2.xlsx")
df2 = pd.read_excel(r"C:\Users\Robot\Desktop\附件3.xlsx")
df2.columns.values[0] = "data"
df2.columns.values[1] = "id"
df1.columns.values[0] = "data"
df1.columns.values[2] = "id"
merdf = pd.merge(df1,df2,on=['id','data'])
merdf.to_excel("./1.xlsx")