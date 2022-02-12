import pickle

arr_size = 512000000
arr = bytearray(arr_size)

result = {
    "suite_id": 233,
    "results": [{"result": {"value": float(arr_size) / 1024 / 1024}}]
}

print(pickle.dumps(result))
