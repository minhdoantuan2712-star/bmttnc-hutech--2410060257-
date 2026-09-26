def xoa_phan_tu(dictionary, key):
    if key in dictionary:
        del dictionary[key]
        return True
    else:
        return False

my_dict = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
print("Dictionary ban đầu:", my_dict)
key_to_delete = input("Nhập key cần xóa: ")
if xoa_phan_tu(my_dict, key_to_delete):
    print(f"Đã xóa key '{key_to_delete}'. Dictionary mới:", my_dict)
else:
    print(f"Key '{key_to_delete}' không tồn tại trong Dictionary.")