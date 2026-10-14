import matplotlib.pyplot as plt

sizes = [
    16 * 1024,
    64 * 1024,
    256 * 1024,
    1024 * 1024,
    4 * 1024 * 1024,
    16 * 1024 * 1024,
    64 * 1024 * 1024
]

times = [0.00008, 0.00051, 0.00209, 0.00923,
         0.03673, 0.18901, 1.77781]

plt.plot(sizes, times, marker="o")

# Логарифмічна вісь розміру робочого набору
plt.xscale("log", base=2)

plt.title("Залежність часу доступу від розміру масиву")
plt.xlabel("Розмір масиву, байт")
plt.ylabel("Час проходу, мс")
plt.grid(True, which="both")
plt.tight_layout()

plt.savefig("cache_graph.png", dpi=150)
plt.show()