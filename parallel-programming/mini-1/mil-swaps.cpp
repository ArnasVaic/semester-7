#include <random>

int main() {
    int a = 0;
    int b = 1;
    int t;
    for (int i = 0; i < 1000000000; ++i) {
        t = b;
        b = a;
        a = t;
    }
}