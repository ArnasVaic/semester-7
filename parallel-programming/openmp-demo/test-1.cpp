#include <omp.h>
#include <cmath>
#include <algorithm>
#include <iostream>

using namespace std;

int main() {

    constexpr int N = 12;
    int x[N] = { 0 };

    for(int i = 0; i < N; ++i) {
        x[i] = i + 1;
    }

    const int p = omp_get_max_threads();
    printf("Number of threads: %i\n", p);

    const int chunk_size = ceil(static_cast<double>(N) / p);
    printf("Chunk size: %i\n", chunk_size);
    // https://stackoverflow.com/questions/37497016/best-practice-in-c-for-casting-between-number-types
    // 10 / 4 -> 3 chunks

    omp_set_num_threads(p);

    #pragma omp parallel
    {
        const int chunk_index = omp_get_thread_num(); 
        const int start = chunk_size * chunk_index;
        const int end = min(N, chunk_size * (chunk_index + 1) - 1);
        printf("Thread %i can access [%i, %i]\n", chunk_index, start, end);
        for(int i = start; i < end; ++i) {
            
        }
    }

    #pragma omp parallel
    {
        #pragma omp for schedule(static)
        for(int i = 0; i < N; ++i) {
            printf("%i\n", i);
        }
    }
}