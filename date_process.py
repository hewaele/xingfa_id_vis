import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

data = pd.read_csv('./pre_result.csv')

#0 索引  1 error_num,  2  extra_num,  3  img_name,  4  omit_num,   5 pre_id,  6 real_id

label_dic = {'error_num':1, 'extra_num':2, 'img_name':3,
             'omit_num':4, 'pre_id':5,  'real_id':6}
#计算总体精确度
ture_id_count = 0
total_id_count = 0

for low in data.index:
    if str(data.loc[low].values[label_dic['error_num']]) == 'nan' \
            and str(data.loc[low].values[label_dic['extra_num']]) == 'nan' \
            and str(data.loc[low].values[label_dic['omit_num']]) == 'nan':
        ture_id_count += 1
    total_id_count += 1

#计算各个字符出现的次数
tmp_num_list = [str(i) for i in range(10)]
tmp_word_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
char_list = tmp_num_list + tmp_word_list
#创建字典
char_info_dict = {}
for c in char_list:
    char_info_dict[c] = {'total_count':0, 'error_count':0, 'omit_count':0, 'extra_count':0}

def update_info(low, from_label, count_label):
    tmp_char = str(data.loc[low].values[label_dic[from_label]])
    if tmp_char != 'nan':
        for c in tmp_char:
            if c in char_list:
                char_info_dict[c][count_label] += 1

#读取数据填充字典
for low in data.index:
    #总次数
    update_info(low, 'real_id', 'total_count')
    #错误
    update_info(low, 'error_num', 'error_count')
    #多检
    update_info(low, 'extra_num', 'extra_count')
    #漏检
    update_info(low, 'omit_num', 'omit_count')

print(char_info_dict)

#绘制数据图
#总错误和单体字符错误
error_char_count = 0
total_char_count = 0
for c in char_list:
    total_char_count += char_info_dict[c]['total_count']
    error_char_count += char_info_dict[c]['error_count'] + char_info_dict[c]['omit_count']\
                        + char_info_dict[c]['extra_count']

plt.grid(True)
plt.ylim([0, 1])
plt.ylabel('accuary')
plt.title('纯字符准确率和完整id准确率')
plt.bar(['id', 'char'], [ture_id_count/total_id_count,
                            (total_char_count - error_char_count)/total_char_count], width = 0.3)
plt.savefig('./picture/整体地准确率和字符准确率.png', dpi=300)
plt.show()

#绘制单个数字出现次数
plt.title('数字出现字数统计')
x1 = char_list[:10]
y1 = [char_info_dict[c]['total_count'] for c in x1[:10]]
plt.bar(x1, y1)
plt.savefig('./picture/数字出现次数.png', dpi=300)
plt.show()

#绘制单个字母出现次数
plt.title('字母出现字数统计')
x2 = char_list[10:]
y2 = [char_info_dict[c]['total_count'] for c in x2]
plt.bar(range(len(x2)), y2, tick_label=x2)
plt.savefig('./picture/字母出现次数.png', dpi=300)
plt.show()

#字符错误率统计
plt.title('字符错误率统计')
x3 = char_list
y3 = []
for xi in x3:
    if char_info_dict[xi]['total_count'] == 0:
        y3.append(0)
    else:
        y3.append(char_info_dict[xi]['error_count']/(char_info_dict[xi]['total_count']))
plt.bar(range(len(x3)), y3, tick_label=x3)
plt.savefig('./picture/字符错误率.png', dpi=300)
plt.show()

#字符错误率统计
plt.title('字符准确率统计')
x4 = char_list
y4 = []
for xi in x4:
    if char_info_dict[xi]['total_count'] == 0:
        y4.append(1)
    else:
        y4.append(1-char_info_dict[xi]['error_count']/(char_info_dict[xi]['total_count']))
plt.bar(range(len(x4)), y4, tick_label=x4)
plt.savefig('./picture/字符准确率.png', dpi=300)
plt.show()

#字符漏检率统计
plt.title('字符漏检率统计')
x5 = char_list
y5 = []
for xi in x5:
    if char_info_dict[xi]['total_count'] == 0:
        y5.append(0)
    else:
        y5.append(char_info_dict[xi]['omit_count']/(char_info_dict[xi]['total_count']))
plt.bar(range(len(x5)), y5, tick_label=x5)
plt.savefig('./picture/字符漏检率.png', dpi=300)
plt.show()

#字符多检率统计
plt.title('字符多检率统计')
x6 = char_list
y6 = []
plt.ylim([0, 0.4])
for xi in x6:
    if char_info_dict[xi]['total_count'] == 0:
        y6.append(0)
    else:
        y6.append(char_info_dict[xi]['extra_count']/(char_info_dict[xi]['total_count']))
plt.bar(range(len(x6)), y6, tick_label=x6)
plt.savefig('./picture/字符多检率.png', dpi=300)
plt.show()

#绘制错误率 准确率 漏检率 多检率 3 4 5 6
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

#plt.ylim(0, 1.5)
ax.plot(range(len(x3)), y3, '*-', label='错误率')
ax.plot(range(len(x4)), y4, 'd-', label='准确率')
ax.plot(range(len(x5)), y5, 'o-', label='漏检率')
ax.plot(range(len(x6)), y6, 'r-', label='多检率')

ax.plot(range(len(x3)),
        [(total_char_count-error_char_count)/total_char_count for i in range(len(x3))],
        '+', label='纯字符准确率')
ax.plot(range(len(x3)),
        [ture_id_count/total_id_count for i in range(len(x3))], label='id准确率')

plt.legend(loc='center right', fontsize='large')
ax.set_xticks(range(len(x6)))
ax.set_xticklabels(x6, rotation=45, fontsize='small')
ax.set_title('统计折线图')
ax.set_xlabel('字符')
ax.grid(True)
plt.savefig('./picture/统计折线图.png', dpi=300)
plt.show()









