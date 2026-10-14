#include <fstream>
#include <string>
#include <iostream>
#include <vector>
#include <iomanip>
#include <chrono>

int main() {
    // Геометрична прогресія розмірів масиву: від 16 КБ до 64 МБ
    std::vector<size_t> sizes_bytes = {
        16 * 1024,        // 16 KB (вміщується в L1)
        64 * 1024,        // 64 KB (перехід L1 -> L2)
        256 * 1024,       // 256 KB (вміщується в L2)
        1024 * 1024,      // 1 MB (перехід L2 -> L3)
        4 * 1024 * 1024,  // 4 MB (вміщується в L3)
        16 * 1024 * 1024, // 16 MB (вміщується в L3)
        64 * 1024 * 1024  // 64 MB (перевищує L3, вихід у DRAM)
    };

    const int STEP = 16; // крок 16 елементів int (64 байти = 1 рядок кешу)

    std::cout << std::left << std::setw(15) << "Size of Array"
              << std::setw(20) << "Elements (int)"
              << std::setw(25) << "Average Time (ms)" << "\n";
    std::cout << std::string(60, '-') << "\n";

    for (size_t bytes : sizes_bytes) {
        size_t count = bytes / sizeof(int);
        std::vector<int> arr(count, 1);

        // Прогрів кешу (warm-up)
        volatile int sum = 0;
        for (size_t i = 0; i < count; i += STEP) {
            sum += arr[i];
        }

        // Кількість повторів для точного усереднення
        size_t iterations = 100000000 / (count / STEP + 1);
        if (iterations < 100) iterations = 100;

        auto start = std::chrono::high_resolution_clock::now();

        for (size_t iter = 0; iter < iterations; ++iter) {
            for (size_t i = 0; i < count; i += STEP) {
                sum += arr[i];
            }
        }

        auto end = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double, std::milli> elapsed = end - start;

        double time_per_pass = elapsed.count() / iterations;

        std::string size_str = (bytes < 1024 * 1024)
            ? std::to_string(bytes / 1024) + " KB"
            : std::to_string(bytes / (1024 * 1024)) + " MB";

        std::cout << std::left << std::setw(15) << size_str
                  << std::setw(20) << count
                  << std::setw(25) << std::fixed << std::setprecision(5) << time_per_pass << "\n";
    }

    return 0;
}