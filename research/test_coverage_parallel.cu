#define THREADS_PER_BLOCK 1024
#define NB_BLOCKS 1

#include "cuda_runtime.h"
#include "device_launch_parameters.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

// Runs the coverage program
__global__ void coverage(char** input, int iterations)
{
    int thread_index = threadIdx.x;
    int nbr_threads = blockDim.x;
    for (int i = thread_index; i < iterations; i = i + nbr_threads) {
        system(input[i]);
        system(input[i + 1]);
    }
}

int main(int argc, char* argv[])
{
    // Check for user input validity
    if (argc != 3) {
        printf("Wrong number of arguments\n");
        return 1;
    }

    // Get user input
    char* input_filename = argv[1];
    int file_length = atoi(argv[2]);

    // Allocate memory
    char** input;
    cudaMallocManaged((void**) &input, file_length * sizeof(char*));
    for (int i = 0; i < file_length; i++)
        cudaMallocManaged((void**)&input[i], 1024 * sizeof(char));

    // Parse input file
    //char line[1024];
    FILE* input_file = fopen(input_filename, "r");

    for (int i = 0; i < file_length; i++) {
        fgets(input[i], 1024, input_file);
    }
    fclose(input_file);

    coverage << <NB_BLOCKS, THREADS_PER_BLOCK >> > (input, file_length/2);
    cudaDeviceSynchronize();

    //Clean
    cudaFree(input);
    return 0;
}