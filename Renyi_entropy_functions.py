import numpy as np
import math

def ask_for_dec():  # 询问小数点后保留位数
    while 1:
        input_string = input("请问您的数据需要保留到小数点后多少位？（请输入整数）")
        try:
            dec = int(input_string)
        except ValueError as e:
            print("请输入整数！")
            continue
        break
    return dec

def get_data_in_column():   # 获取数据中的某一列
    tmp_data = np.loadtxt("data.txt")
    while True:
        try:
            column_num = int(input("请输入要处理数据的列号："))
        except ValueError as e:
            print("请输入索引范围内的整数！")
            continue
        try:
            data = tmp_data[:, column_num]
        except IndexError as e:
            print("请输入索引范围内的整数！")
            continue
        break
    return data

def dataprocess(data, dec): # 按保留小数点后位数 dec 处理数据数组 data
    processed_data = np.round(data, decimals = dec)
    # numpy中的round函数可以实现对数组的四舍五入处理。
    return processed_data

def vec_P_generate(data):   # 生成概率向量P
    # np.unique 函数返回的第一个数组datainfo[0] 是从小到大排列的，原数据中的不重复元素。
    # 该算法基于频率估计的概率，所以第一个数组无用
    # np.unique 函数返回的第二个数组datainfo[1] 是对不重复元素出现次数的统计数组
    datainfo = np.unique(data, return_counts=True)
    np.savetxt("datainfo.txt", datainfo)
    vec_N = datainfo[1]
    np.savetxt("vec_N.txt", vec_N)
    total = np.sum(vec_N)   # np.sum() 函数对数组中的元素求和
    print(total)
    vec_P = vec_N / total
    np.savetxt("vec_P.txt", vec_P)
    return vec_P

def ask_for_alpha():    # 询问所求熵的阶数 alpha
    while True:
        input_string = input("请问所求熵的阶数是多少？（无限阶用infty，请输入非负数或infty）")
        if input_string == "infty":
            alpha = -1  # 用 -1 来标记无限
        else:
            try:
                alpha = float(input_string)
            except ValueError as e:
                print("请输入非负数或infty！")
                continue
            if alpha < 0:
                print("请输入非负数或infty！")
                continue
        break
    return alpha

def shannon_entropy(vec):   # 一阶 Rényi 熵
    for iterm in vec:
        iterm = - iterm * math.log(iterm)
    np.savetxt("vec.txt", vec)
    shannon_sum = np.sum(vec)
    return shannon_sum

def other_order_entropy(alpha, vec):    # 非一阶 Rényi 熵
    if alpha != -1:
        alpha_norm = np.linalg.norm(vec, ord = alpha)
        entropy = (1 / (1 - alpha) - 1)*math.log(alpha_norm)
    else:
        alpha_norm = np.linalg.norm(vec, ord = np.inf)
        entropy = -math.log(alpha_norm)
    return entropy
    
def calculate_entropy(alpha, vec):  # 计算 Rényi 熵的通用接口
    if alpha == 1:
        entropy = shannon_entropy(vec)
    else:
        entropy = other_order_entropy(alpha, vec)
    return entropy

def print_entropy(alpha, data): # 输出模块
    if alpha != -1:
        print(f"您数据所求的 {alpha} 阶 Rényi 熵是 {calculate_entropy(alpha, data)}")
    else:
        print(f"您数据所求的无限阶 Rényi 熵是 {calculate_entropy(alpha, data)}")
    return
