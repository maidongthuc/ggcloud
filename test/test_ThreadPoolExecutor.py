import time
from concurrent.futures import ThreadPoolExecutor

def task(name, index):
    print(f"Start {name} - Index: {index}")
    time.sleep(4)  # Giả lập tác vụ I/O
    print(f"End {name} - Index: {index}")
    return f"Result from {name} - Index: {index}"

names = ["A", "B", "C", "D", "E"]

with ThreadPoolExecutor(max_workers=3) as executor:
    futures = []
    
    # Dùng vòng loop để submit task với index
    for index, name in enumerate(names):
        future = executor.submit(task, name, index)
        futures.append(future)
    
    # Lấy kết quả theo thứ tự
    results = []
    for future in futures:
        result = future.result()
        results.append(result)

# In kết quả
for result in results:
    print(result)


# def function_sum(a, b, function_tru):
#     """
#     Hàm tính tổng hai số.
#     Args:
#         a (int): Số thứ nhất.
#         b (int): Số thứ hai.
#     Returns:
#         int: Tổng của a và b.
#     """
#     c = function_tru(a, b)
#     c = c + 1
#     return c

# def function_tru(a, b):
#     """
#     Hàm tính hiệu hai số.
#     Args:
#         a (int): Số thứ nhất.
#         b (int): Số thứ hai.
#     Returns:
#         int: Hiệu của a và b.
#     """
#     return a - b

# d = function_sum(5, 3, function_tru)
# print(d)