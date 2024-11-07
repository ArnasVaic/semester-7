#include <iostream>
#include <cmath>
#include <time.h>
#include <sys/time.h>
#include <mpi.h>
#include <cstddef>
#include <assert.h>

using namespace std;

struct demand_point_t
{
	double latitude;
	double longitude;
	double population;
};

//===== Globalus kintamieji ===================================================

// initial config: 5000, 5, 55, 3

int numDP = 4; // Vietoviu skaicius (demand points, max 10000)
int numPF = 1;	  // Esanciu objektu skaicius (preexisting facilities)
int numCL = 1;	  // Kandidatu naujiems objektams skaicius (candidate locations)
int numX = 1;	  // Nauju objektu skaicius

demand_point_t *demandPoints = new demand_point_t[numDP];	 // Geografiniai duomenys
double **distanceMatrix; // Masyvas atstumu matricai saugoti

int *X = new int[numX];		// Naujas sprendinys
int *bestX = new int[numX]; // Geriausias rastas sprendinys
double u, bestU;			// Naujo sprendinio ir geriausio sprendinio naudingumas (utility)

//===== Funkciju prototipai ===================================================

double getTime();
void loadDemandPoints();
double HaversineDistance(demand_point_t const& p1, demand_point_t const& p2);
double HaversineDistance(int i, int j);
double evaluateSolution(int *X);
int increaseX(int *X, int index, int maxindex);

//=============================================================================

int main()
{

	MPI_Init(NULL, NULL);

	// Register demand point type
	MPI_Datatype MPI_DemandPoint;
	int lengths[3] = {1, 1, 1};
	MPI_Aint offsets[3];
	offsets[0] = offsetof(demand_point_t, latitude);
	offsets[1] = offsetof(demand_point_t, longitude);
	offsets[2] = offsetof(demand_point_t, population);
	MPI_Datatype types[3] = {MPI_DOUBLE, MPI_DOUBLE, MPI_DOUBLE};

	MPI_Type_create_struct(3, lengths, offsets, types, &MPI_DemandPoint);
	MPI_Type_commit(&MPI_DemandPoint);

	// Main flow
	int world_rank, world_size;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);

	if(0 == world_rank)
	{
		loadDemandPoints();
	}

	MPI_Bcast(demandPoints, numDP, MPI_DemandPoint, 0, MPI_COMM_WORLD);

	// cout << "[rank=" << world_rank << "] Broadcast received: demandPoint[" << world_rank << 
	// 	"] = { lat: " << demandPoints[world_rank].latitude << 
	// 	", lon: " << demandPoints[world_rank].longitude << 
	// 	", pop: " << demandPoints[world_rank].population << " }\n";

	double t_start = getTime(); // Algoritmo vykdymo pradzios laikas

	//----- Atstumu matricos skaiciavimas -------------------------------------
	if ( 0 == world_rank )
	{
		// Only master process needs the entire matrix
		// when gathering results it will initialize each line
		distanceMatrix = new double *[numDP];
	}

	// Each process will calculate multiple pairs of lines of this distance matrix
	// To keep the work balanced the matrix lines will come in pairs -
	// one line from the top and one from the bottom, this way there will
	// be a need to process n + 1 elements for each unit of work.

	// world size: p
	// element number: n
	// matrix size: n(n + 1)/2
	// pairs per process: ceil(n / (2 * p)) note: last process may have to process less pairs if it happens so that n is not divisible by 2 * p
	// elements per unit: n + 1 
	assert( 0 == numDP % 2 );

	const int stride = ceil(numDP / (2.0f * world_size));
	const int start = world_rank * stride;
	const int end = min(stride * ( 1 + world_rank ), numDP / 2);
	const int pairs_cnt = end - start + 1;

	// each process calculates (n + 1) * pairs_cnt values
	const int result_cnt = pairs_cnt * (numDP + 1);
	double *local_result = new double[result_cnt];

	if ( 0 == world_rank )
	{
		cout << "common params:\n";
		cout << "stride: " << stride << "\n";
	} 

	cout << "[rank=" << world_rank << "] " 
		<< "range: [" << start << "-" << end << "]"
		<< ", pairs: " << pairs_cnt
		<< '\n';

	// Iterate through pairs
	for ( int pair_index = start; pair_index < end; ++pair_index )
	{
		demand_point_t const& p1 = demandPoints[pair_index];

		// store two lines in one aray side by side

		// From:
		// l1 = start + 1
		// ┌───┐
		// 0..l1 <- distance matrix values for row=start
		// ...
		// 0.....l2 <- distance matrix values for row=n+1-start
		// └──────┘
		// l2 = n + 1 - l1 = n - start

		// To:
		// l = l1 + l2 = n + 1
		// ┌───────────┐
		// 0..l10.....l2 <- both stored in one array side by side
		
		// And all these pairs will be stored side by side inside 
		// result and are of the same length: n + 1 for each pair
		// result:
		// pair_index=0 pair_index=1 pair_index=2
		// v            v            v
 		// ┌───────────┐┌───────────┐┌───────────┐
		// 0..l10.....l20..l10.....l20..l10.....l2
		//              │    │
		//              └ pair_offset = pair_index * (n + 1) = shorter_offset
		//                   └ longer_offset = pair_index * (n + 1) + pair_index
		//                   

		const int pair_offset = pair_index * (numDP + 1);

		// Evaluate shorter line

		// writeable slice of shorter array
		const int shorter_cnt = pair_index + 1;
		double *shorter = &local_result[pair_offset];
		for ( int j = 0; j < shorter_cnt; ++j )
		{
			demand_point_t const& p2 = demandPoints[j];
			shorter[j] = HaversineDistance(p1, p2);
		}

		// Evaluate longer line
		// writeable slice of longer array
		const int longer_cnt = numDP - pair_index;
		double *longer = &shorter[shorter_cnt];
		for ( int j = 0; j < longer_cnt; ++j )
		{
			demand_point_t const& p2 = demandPoints[j];
			longer[j] = HaversineDistance(p1, p2);
		}
	}

	int *result_counts = nullptr;
	int *result_disps = nullptr;
	double *wrapped_result = nullptr;

	if ( 0 == world_rank )
	{
		result_counts = new int[world_size];
		result_disps = new int[world_size];
		for ( int i = 0; i < world_size; ++i ) {
			// Offset each process's data by N elements
			result_disps[i] = i * result_cnt;
		}
		wrapped_result = new double[world_size * result_cnt];
	}
	
	MPI_Gatherv(
		local_result, 
		result_cnt, 
		MPI_DOUBLE,
		wrapped_result,
		result_counts,
		result_disps,
		MPI_DOUBLE, 
		0, 
		MPI_COMM_WORLD);

	if ( 0 == world_rank ) {
        for (int i = 0; i < world_size; ++i) {
            cout << i << ": ";
            for (int j = 0; j < result_counts[i]; ++j) {
                cout << wrapped_result[result_disps[i] + j] << " ";
            }
            cout << "\n";
        }
    }
	

	// for (int i = 0; i < numDP; i++)
	// {
	// 	distanceMatrix[i] = new double[i + 1];
	// 	for (int j = 0; j <= i; j++)
	// 	{
	// 		distanceMatrix[i][j] = HaversineDistance(
    //             demandPoints[i].latitude, 
    //             demandPoints[i].longitude, 
    //             demandPoints[j].latitude, 
    //             demandPoints[j].longitude);
	// 	}
	// }
	double t_matrix = getTime();
	cout << "Matricos skaiciavimo trukme: " << t_matrix - t_start << endl;

	// //----- Pradines naujo ir geriausio sprendiniu reiksmes -------------------
	// for (int i = 0; i < numX; i++)
	// { // Pradines naujo ir geriausio sprendiniu koordinates: [0,1,2,...]
	// 	X[i] = i;
	// 	bestX[i] = i;
	// }
	// u = evaluateSolution(X); // Naujo sprendinio naudingumas (utility)
	// bestU = u;				 // Geriausio sprendinio sprendinio naudingumas

	// //----- Visų galimų sprendinių perrinkimas --------------------------------
	// while (increaseX(X, numX - 1, numCL) == true)
	// {
	// 	u = evaluateSolution(X);
	// 	if (u > bestU)
	// 	{
	// 		bestU = u;
	// 		for (int i = 0; i < numX; i++)
	// 			bestX[i] = X[i];
	// 	}
	// }

	// //----- Rezultatu spausdinimas --------------------------------------------
	// double t_finish = getTime(); // Skaiciavimu pabaigos laikas
	// cout << "Sprendinio paieskos trukme: " << t_finish - t_matrix << endl;
	// cout << "Algoritmo vykdymo trukme: " << t_finish - t_start << endl;
	// cout << "Geriausias sprendinys: ";
	// for (int i = 0; i < numX; i++)
	// 	cout << bestX[i] << " ";
	// cout << "(" << bestU << " procentai rinkos)" << endl;

	MPI_Finalize();
}

//===== Funkciju implementacijos (siu funkciju LYGIAGRETINTI NEREIKIA) ========

void loadDemandPoints()
{
	FILE *f;
	f = fopen("demandPoints.dat", "r");
	for (int i = 0; i < numDP; i++)
	{
		fscanf(f, "%lf%lf%lf", &demandPoints[i].latitude, &demandPoints[i].longitude, &demandPoints[i].population);
		if ( 0 == i )
		{
			cout << "demandPoint[0] = { lat: " << demandPoints[i].latitude << ", lon: " << demandPoints[i].longitude << ", pop: " << demandPoints[i].population << " }\n";
		}
	}
	fclose(f);
}

//=============================================================================

double HaversineDistance(demand_point_t const& p1, demand_point_t const& p2)
{
	const double lat1 = p1.latitude;
	const double lon1 = p1.longitude;
	const double lat2 = p2.latitude;
	const double lon2 = p2.longitude;

	double dlat = fabs(lat1 - lat2);
	double dlon = fabs(lon1 - lon2);
	double aa = pow((sin((double)dlat / (double)2 * 0.01745)), 2) + cos(lat1 * 0.01745) *
																		cos(lat2 * 0.01745) * pow((sin((double)dlon / (double)2 * 0.01745)), 2);
	double c = 2 * atan2(sqrt(aa), sqrt(1 - aa));
	double d = 6371 * c;
	return d;
}

double HaversineDistance(int i, int j)
{
	if (i >= j)
		return distanceMatrix[i][j];
	else
		return distanceMatrix[j][i];
}

//=============================================================================

double getTime()
{
	struct timeval laikas;
	gettimeofday(&laikas, NULL);
	double rez = (double)laikas.tv_sec + (double)laikas.tv_usec / 1000000;
	return rez;
}

//=============================================================================

double evaluateSolution(int *X)
{
	double U = 0;
	double totalU = 0;
	int bestPF;
	int bestX;
	double d;
	for (int i = 0; i < numDP; i++)
	{
		totalU += demandPoints[i].population;
		bestPF = 1e5;
		for (int j = 0; j < numPF; j++)
		{
			d = HaversineDistance(i, j);
			if (d < bestPF)
				bestPF = d;
		}
		bestX = 1e5;
		for (int j = 0; j < numX; j++)
		{
			d = HaversineDistance(i, X[j]);
			if (d < bestX)
				bestX = d;
		}
		if (bestX < bestPF)
			U += demandPoints[i].population;
		else if (bestX == bestPF)
			U += 0.3 * demandPoints[i].population;
	}
	return U / totalU * 100;
}

//=============================================================================

int increaseX(int *X, int index, int maxindex)
{
	if (X[index] + 1 < maxindex - (numX - index - 1))
	{
		X[index]++;
	}
	else
	{
		if ((index == 0) && (X[index] + 1 == maxindex - (numX - index - 1)))
		{
			return 0;
		}
		else
		{
			if (increaseX(X, index - 1, maxindex))
				X[index] = X[index - 1] + 1;
			else
				return 0;
		}
	}
	return 1;
}