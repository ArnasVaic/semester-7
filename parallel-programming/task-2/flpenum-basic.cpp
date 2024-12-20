#include <iostream>
#include <cmath>
#include <time.h>
#include <sys/time.h>
#include <mpi.h>
#include <assert.h>

using namespace std;

//===== Globalus kintamieji ===================================================

struct demand_point_t
{
	double latitude;
	double longitude;
	double population;
};

int numDP = 5000; // Vietoviu skaicius (demand points, max 10000)
int numPF = 5;	  // Esanciu objektu skaicius (preexisting facilities)
int numCL = 55;	  // Kandidatu naujiems objektams skaicius (candidate locations)
int numX = 3;	  // Nauju objektu skaicius

demand_point_t *demandPoints;	 // Geografiniai duomenys
double **distanceMatrix = new double*[numDP]; // Masyvas atstumu matricai saugoti

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

	MPI_Datatype MPI_DemandPoint;
	int lengths[3] = {1, 1, 1};
	MPI_Aint offsets[3];
	offsets[0] = offsetof(demand_point_t, latitude);
	offsets[1] = offsetof(demand_point_t, longitude);
	offsets[2] = offsetof(demand_point_t, population);
	MPI_Datatype types[3] = {MPI_DOUBLE, MPI_DOUBLE, MPI_DOUBLE};

	MPI_Type_create_struct(3, lengths, offsets, types, &MPI_DemandPoint);
	MPI_Type_commit(&MPI_DemandPoint);

	int world_rank, world_size;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);

	//printf("[rank=%d] allocating demandPoints (%d bytes)\n", world_rank, numDP * sizeof(demand_point_t));
	demandPoints = new demand_point_t[numDP];
	if ( 0 == world_rank )
	{
		loadDemandPoints();		// Duomenu nuskaitymas is failo
	}

	MPI_Bcast(demandPoints, numDP, MPI_DemandPoint, 0, MPI_COMM_WORLD);
	
	double t_start = getTime(); // Algoritmo vykdymo pradzios laikas
	
	//----- Atstumu matricos skaiciavimas -------------------------------------

	// Each process evaluates approximately numDP / (world_size - 1) (round up) lines in the matrix
	const int lines_count = ceil(static_cast<double>(numDP) / (world_size - 1));

	if ( 0 == world_rank )
	{
		printf("lines per process: %d\n", lines_count);	
	}

	// example numDP=6789, world_size=12
	// lines_count = 618
	// process 0: receives initialized matrix lines
	// process 1: 0, 12, 24, ..., 6798 (last index, will be skipped)
	// ...
	// process 11: 11, 23, 35, ..., 6791 (last index, will be skipped)

	// initialize distance matrix
	for ( int i = 0; i < numDP; ++i )
	{
		distanceMatrix[ i ] = new double[ i + 1 ] { 0 };
		assert( distanceMatrix[ i ] != nullptr );
	}

	if( 0 != world_rank )
	{
		int messages_sent = 0;

		double *local_result = new double[ numDP ];

		for ( int i = 0; i < lines_count; ++i )
		{
			const int line_index = (world_rank - 1) + i * (world_size - 1);

			// since the matrix is triangular, each results 
			// will always be of length line_index + 1
			const int result_length = line_index + 1;

			if ( result_length > numDP )
			{
				break;
			}

			// printf("[rank=%d,index=%d,send]\n", world_rank, line_index);

			//printf("[rank=%d] allocating local_result (%d bytes)\n", world_rank, result_length * sizeof(double));
			

			demand_point_t const& from = demandPoints[ line_index ];

			for ( int j = 0; j < result_length; ++j )
			{
				demand_point_t const& to = demandPoints[ j ];
				local_result[ j ] = HaversineDistance( from, to ); 
			}

			if ( (i % 2) == 0 )
			{
				//printf("[rank=%d] sending line of length: ", world_rank, result_length);
			}

			MPI_Send(local_result, numDP, MPI_DOUBLE, 0, line_index, MPI_COMM_WORLD);
			++messages_sent;

			//printf("[rank=%d] freeing local_result (%d bytes)\n", world_rank, numDP * sizeof(double));
		}

		printf("[slave=%d] messages sent: %d\n", world_rank, messages_sent);
	}

	if ( 0 == world_rank )
	{
		// Only master process needs the entire matrix
		// when gathering results it will initialize each line
		//printf("[rank=%d] allocating distanceMatrix (%d bytes)\n", world_rank, numDP * sizeof(double*));

		double *buffer = new double[ numDP ];

		int messages_received = 0;
		MPI_Status status;
		for ( int i = 1; i < world_size; ++i )
		{
			// Each process will send approximately lines_count messages, but not exactly
			// some processes may send one less, depending on the last index
			const int max_line_index = i - 1 + (lines_count - 1) * (world_size - 1);

			const int actual_line_count = max_line_index + 1 > numDP ? lines_count - 1 : lines_count;

			// printf("[rank=%d] max line index to be awaited: %d\n", i, max_line_index);
			printf("[slave=%d] line count for this process: %d\n", i, actual_line_count);

			for ( int j = 0; j < actual_line_count; ++j )
			{	
				//printf("[rank=%d,index=%d,recv]\n", i, line_index)

				MPI_Recv(buffer, numDP, MPI_DOUBLE, MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, &status);
				++messages_received;

				const int line_index = status.MPI_TAG;
				const int buffer_length = line_index + 1;
				memcpy(distanceMatrix[ line_index ], buffer, buffer_length * sizeof(double));
			}
		}

		printf("[master] messages received: %d\n", messages_received);
	}

	double t_matrix = getTime();

	if ( 0 == world_rank )
	{
		cout << "Matricos skaiciavimo trukme: " << t_matrix - t_start << endl;
	} 

	if( 0 == world_rank )
	{
		// send matrix to all other processes
		for ( int i = 1; i < world_size; ++i )
		{
			printf("[master] sending distance matrix to process: %d (total: %d arrays)\n", i, numDP);
			for( int j = 0; j < numDP; ++j )
			{
				double *row = distanceMatrix[j];
				MPI_Send(row, j + 1, MPI_DOUBLE, i, j, MPI_COMM_WORLD);
			}
		}
	}
	else
	{
		MPI_Status status;
		for ( int i = 0; i < numDP; ++i )
		{
			double *row = distanceMatrix[i];
			MPI_Recv(row, i + 1, MPI_DOUBLE, 0, i, MPI_COMM_WORLD, &status);
		}
		printf("[slave=%d] receiving distance matrix (total: %d arrays)\n", world_rank, numDP);
		// printf("[slave=%d] distanceMatrix[4]: ", world_rank);
		// for ( int i = 0; i < 5; ++i )
		// {
		// 	cout << distanceMatrix[4][i] << " ";
		// }
		// cout << '\n';
	}

	// //----- Pradines naujo ir geriausio sprendiniu reiksmes -------------------

	if( 0 == world_rank )
	{
		for (int i = 0; i < numX; i++)
		{ // Pradines naujo ir geriausio sprendiniu koordinates: [0,1,2,...]
			X[i] = i;
			bestX[i] = i;
		}
		u = evaluateSolution(X); // Naujo sprendinio naudingumas (utility)
		bestU = u;				 // Geriausio sprendinio sprendinio naudingumas

		//----- Visų galimų sprendinių perrinkimas --------------------------------
		MPI_Status status;
		int messages_sent = 0;
		// Receive request for/send tasks
		while ( increaseX(X, numX - 1, numCL) == true )
		{
			int tmp;
			MPI_Recv(&tmp, 1, MPI_INT, MPI_ANY_SOURCE, 0, MPI_COMM_WORLD, &status);
			//printf("[master] received task request from slave: %d.\n", status.MPI_SOURCE);

			MPI_Send(X, numX, MPI_INT, status.MPI_SOURCE, 0, MPI_COMM_WORLD);
			//printf("[master] send task to slave: %d.\n", status.MPI_SOURCE);

			++messages_sent;
		}

		// Collect results
		for ( int messages_received = 0; messages_received < messages_sent; ++messages_received )
		{
			MPI_Recv(&u, 1, MPI_DOUBLE, MPI_ANY_SOURCE, 1, MPI_COMM_WORLD, &status);

			if ( u > bestU )
			{
				bestU = u;
				memcpy(bestX, X, numX * sizeof(double));
			}
		}

		//printf("[master] messages sent: %d\n", messages_sent);

		// When all tasks are completed send termination signals to unblock slave processes
		for (int i = 1; i < world_size; ++i) {
			MPI_Send(&X, numX, MPI_INT, i, 2, MPI_COMM_WORLD);
		}
	}
	else
	{
		while(true)
		{
			// Request task
			//printf("[slave=%d] requesting task.", world_rank);
			MPI_Send(&world_rank, 1, MPI_INT, 0, 0, MPI_COMM_WORLD);

			MPI_Status status;
			MPI_Recv(X, numX, MPI_INT, 0, MPI_ANY_TAG, MPI_COMM_WORLD, &status);

			// Check if termination task
			if( 2 == status.MPI_TAG )
			{
				//printf("[slave=%d] closing receiver.\n", world_rank);
				break;
			}

			u = evaluateSolution(X);

			//printf("[slave=%d] sending result.", world_rank);
			MPI_Send(&u, 1, MPI_DOUBLE, 0, 1, MPI_COMM_WORLD);
		}
	}


	//----- Rezultatu spausdinimas --------------------------------------------
	double t_finish = getTime(); // Skaiciavimu pabaigos laikas

	if ( 0 == world_rank )
	{
		cout << "Sprendinio paieskos trukme: " << t_finish - t_matrix << endl;
		cout << "Algoritmo vykdymo trukme: " << t_finish - t_start << endl;
		cout << "Geriausias sprendinys: ";
		for (int i = 0; i < numX; i++)
			cout << bestX[i] << " ";
		cout << "(" << bestU << " procentai rinkos)" << endl;
	}
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