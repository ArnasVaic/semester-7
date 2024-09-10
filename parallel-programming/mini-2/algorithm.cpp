#include <iostream>
#include <random>

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
   int cols = 200;            // Number of columns
   int **A;                // Matrix
   double ts; 
   
   // Generate matrix
   GenerateMatrix(A, rows, cols);

   // Sort rows of the matrix
   for (int i=0; i<rows; i++) {
      SortRow(A[i], cols);
   }
}