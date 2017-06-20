#include <math.h>
#include <limits>

#include <vector>

#pragma once

using namespace std;

#define T_LEN 150
#define DV 0.0000001
#define T_STEP 0.1

inline double randomreal();

inline float uniformRand(float l, float r);

inline float rsmd(float* fit, const float* sample, int len, int factor);
inline void step_calc(float* fit_step, float p_smd, float n_smd);
void rand_init(int n, float* arr, float l, float r);
inline void norm(float len, float* grad, int n);
int min_index(float* err, int n, float* min_err=0);
int max_index(float* err, int n);

float const inf_p = 1/0.3e-55;
float const inf_n = -1/0.3e-55;

class IdGenerator
{
public:
    IdGenerator(int len = 100);
    int getId();
    void returnId(int Id);
private:
    vector <int> refundId;
             int lastId;
};

class NeuroNet
{
public:
	NeuroNet(int nneurons, int nIter, 
				  float* init_value, 
				  float* init_weight);
	~NeuroNet();

void	addNeuron(float init_val=0, float* init_weight=0);
void	delNeuron();
void	calculate(int niter=T_LEN);
void	clear();
void	alterWeight(const float* weight);
void	alterValue(const float* value);

void	alterWeight(int id, float weight);
void	alterValue(int id, float value);

void	setWeight(const float* weight);
void	setValue(const float* value);

float	gradRelease(vector <bool> arch, const float* sample, int s_len, int max_iter);


void	getWeight(float* weight);
void	getNeurons(float* value_arr);
void	getTrajectory(float* fit);

private:
IdGenerator*	id_gen;
		 int	cur_nnum;
		 int	cur_wnum;

		 int	iter_count;
vector <float>	trajectory;

vector <float>	init_value;
vector <float>	value;
vector <float>	weight;
vector <float>	grad;
};