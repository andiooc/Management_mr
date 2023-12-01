import re

# 原始字符串
input_str = "ABCD[A1中文]BCD[B2文本]DWP[E3英文]"

# 使用正则表达式找到所有的方括号及其内部的不定长度字符串
matches = re.findall(r'\[[^\]]+\]', input_str)

# 将所有找到的匹配项拼接起来
cleaned_str = ','.join(matches)

print(cleaned_str)  # 输出: [A1中文][B2文本][E3英文]
