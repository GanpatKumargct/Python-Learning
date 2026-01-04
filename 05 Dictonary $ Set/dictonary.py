a = {
"key": "value",
"harry": "code",
"marks": "100",
"list": [1, 2, 9]
}
print(a["key"]) # Output: "value"
print(a["list"]) # Output: [1, 2, 9]

print(a.items())
print(a.values())
print(a.keys())
a.update({"harry":86})

print(a)