import pandas as pd

# 创建示例数据框
data = {
    'category': ['A', 'A', 'B', 'B', 'B', 'C', 'C'],
    'value': [10, 15, 20, 25, 20, 30, 35]
}
df = pd.DataFrame(data)

# 使用 pandas 的 rank 方法对数据进行排名
df['rank'] = df.groupby('category')['value'].rank(method='min', ascending=False)

print(df)



