def truy_cap_phan_tu(tupl):
    first_element = tupl[0]
    last_element = tupl[-1]
    return first_element, last_element

input_eval = input("Nhập danh sách các phần tử (cách nhau bởi dấu phẩy): ")
my_tuple = tuple(input_eval.split(','))
first, last = truy_cap_phan_tu(my_tuple)
print("Phần tử đầu tiên:", first)
print("Phần tử cuối cùng:", last)