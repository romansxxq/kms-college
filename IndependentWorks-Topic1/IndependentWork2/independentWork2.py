
text = "Комп'ютер"

print(f"Символів у рядку: {len(text)}")
print(f"Байтів у UTF-8: {len(text.encode('utf-8'))}")

print(f"{'Символ':<8} {'Unicode':<10} {'UTF-8 (hex)':<12} | {'Байти'}")
print("-" * 45)

for char in text:
    unicode_point = f"U+{ord(char):04X}"
    utf8_bytes = " ".join(f"{b:02X}" for b in char.encode("utf-8"))
    byte_count = len(char.encode("utf-8"))
    print(f"{char:<8} {unicode_point:<10} {utf8_bytes:<12} | {byte_count}")
