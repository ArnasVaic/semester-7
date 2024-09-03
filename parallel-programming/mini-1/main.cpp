#include <iostream>
#include <random>
#include <chrono>

using namespace std;

//=============================================================================

void GenerateMatrix(int **&A, int rows, int cols) {
   A = new int*[rows];
   for (int i=0; i<rows; i++) {
      A[i] = new int[cols];
      for (int j=0; j<cols; j++) {
         A[i][j] = (double)rand()/RAND_MAX;
      }
   }
}

//-----------------------------------------------------------------------------

void SortRow(int *A, int cols) {
   int t;
   for (int i=0; i<cols-1; i++)
      for (int j=0; j<cols-1; j++)
         if (A[j] > A[j+1]) { t = A[j]; A[j] = A[j+1]; A[j+1] = t; }
}

//=============================================================================

int main() {
   srand(time(NULL));
   int rows = 128000;         // Number of rows
   int cols = 400;            // Number of columns
   int **A;                   // Matrix
   double ts; 
   
   // Generate matrix
   auto b1 = std::chrono::steady_clock::now();
   GenerateMatrix(A, rows, cols);
   auto e1 = std::chrono::steady_clock::now();

   // Sort rows of the matrix
   auto b2 = std::chrono::steady_clock::now();
   for (int i=0; i<rows; i++) {
      SortRow(A[i], cols);
   }
   auto e2 = std::chrono::steady_clock::now();

   auto d1 = std::chrono::duration_cast<std::chrono::nanoseconds>(e1 - b1).count();
   auto d2 = std::chrono::duration_cast<std::chrono::nanoseconds>(e2 - b2).count();

   std::cout << "D1: " << d1 << "[ns]" << std::endl;
   std::cout << "D2: " << d2 << "[ns]" << std::endl;
}