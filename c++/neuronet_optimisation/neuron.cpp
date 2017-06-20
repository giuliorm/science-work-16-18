#include "neuron.h"
inline double randomreal()
{
    int i1 = rand();
    int i2 = rand();
    while(i1==RAND_MAX)
        i1 =rand();
    while(i2==RAND_MAX)
        i2 =rand();
    double mx = RAND_MAX;
    return (i1+i2/mx)/mx;
}


int min_index(float* err, int n, float* min_err)
{
	float min=100;
	int min_ind =0 ;
	for(int i=0; i<n; i++)
	{
		if(abs(err[i])<min&&err[i]!=0)
		{
			min = abs(err[i]);
			min_ind = i;
		}
	};
	if(min_err!=0)
		*min_err = min;
	return min_ind;
};

int max_index(float* err, int n)
{
	float max=0;
	int max_ind =0 ;
	for(int i=0; i<n; i++)
	{
		if(abs(err[i])>max)
		{
			max = abs(err[i]);
			max_ind = i;
		}
	};
	
	return max_ind;
};

inline void norm(float len, float* grad, int n)
{
	float l = 0;
	for(int i=0; i<n; i++)
		l += grad[i]*grad[i];
	l = sqrt(l);

	for(int i=0; i<n; i++)
		grad[i] = grad[i]/l*len;
};

inline bool isfinite(float value)
{
  return value !=  std::numeric_limits<float>::infinity() &&
         value != -std::numeric_limits<float>::infinity();
}

inline float uniformRand(float l, float r)
{
	{
		float a=randomreal();
		float x=a*r+l;		
		return x;
	}
};

inline float rsmd(float* fit, const float* sample, int len, int factor)
{
	float smd=0;
	for(int i=0; i<len/factor; ++i)
		smd+=pow((fit[i*factor]-sample[i*factor]),2);

	smd = smd/len*factor;
	return smd;
};

inline void step_calc(float* fit_step, float p_smd, float n_smd)
{
	if(abs(p_smd-n_smd)<p_smd*0.01&&*fit_step<0.1)
		*fit_step = *fit_step*1.5;
	else
		*fit_step = *fit_step/2;
}


void rand_init(int n, float* arr, float l, float r)
{
	for(int i=0; i<n; i++)
		arr[i] = uniformRand(l,r);
}

IdGenerator::IdGenerator(int len)
{lastId=0; refundId.reserve(len);}

void IdGenerator::returnId(int id)
{refundId.push_back(id);}

int IdGenerator::getId()
{
	if(refundId.size()==0)
	{	lastId++;
		return lastId;}
	else
	{	int r=refundId.back();
		refundId.pop_back();;
		return r;}
};

NeuroNet::NeuroNet(int nneurons, int nIter, float *i_value, float *i_weight):
	cur_wnum(nneurons*nneurons), cur_nnum(nneurons), iter_count(0)
{
	id_gen = new IdGenerator();
	weight.resize(cur_wnum,0);
	value.resize(cur_nnum,0);
	init_value.resize(cur_nnum,0);
	grad.resize(cur_nnum+cur_wnum,0);
	trajectory.reserve(T_LEN);

	memcpy(&(value[0]), i_value, cur_nnum*sizeof(float));
	init_value = value;
	memcpy(&(weight[0]), i_weight, cur_wnum*sizeof(float));
};

NeuroNet::~NeuroNet()
{
	trajectory.clear();
	value.clear();
	weight.clear();
	grad.clear();
	delete id_gen;
};

void NeuroNet::alterWeight(const float *a_weight)
{
	for(int i=0; i<cur_wnum; i++)
		weight[i]+=a_weight[i];
};

void NeuroNet::alterValue(const float *a_value)
{
	for(int i=0; i<cur_nnum; i++)
		value[i]+=a_value[i];
	init_value = value;
};

void NeuroNet::alterWeight(int id, float w)
{
	weight[id]+=w;
	calculate();
	weight[id]-=w;
	value = init_value;
};

void NeuroNet::alterValue(int id, float v)
{
	value[id]+= v;
	calculate();
	value = init_value;
};

void NeuroNet::setWeight(const float* n_weight)
{memcpy(&(weight[0]), n_weight, cur_wnum*sizeof(float));};

void NeuroNet::setValue(const float* n_value)
{
	memcpy(&(value[0]), n_value, cur_nnum*sizeof(float));
	memcpy(&(init_value[0]), n_value, cur_nnum*sizeof(float));
};

void NeuroNet::clear()
{
	value = init_value;
	iter_count=0;
};

void NeuroNet::calculate(int niter)
{
	if(trajectory.size()<=niter)
		trajectory.resize(niter,0);
	
	for(int I=0; I<niter; I++)
	{
		for(int i=0; i<cur_wnum; i++)
			value[i/cur_nnum] +=weight[i]*value[i%cur_nnum];
		
		trajectory[I]=value[0];
	}
	iter_count+=niter;
};

void NeuroNet::getWeight(float *weight_arr)
{
	for(int i=0; i<cur_wnum; i++)
			weight_arr[i]=weight[i];
};

void NeuroNet::getNeurons(float *value_arr)
{
	for(int i=0; i<cur_nnum; i++)
			value_arr[i]=value[i];
};

void NeuroNet::getTrajectory(float* fit)
{memcpy(fit, &(trajectory[0]), trajectory.size()*sizeof(float));}

void NeuroNet::addNeuron(float init_val, float* init_weight)
{
	cur_nnum+=1;
	cur_wnum = cur_nnum*cur_nnum;
	init_value.push_back(init_val);
	value.push_back(init_val);
	weight.resize(cur_wnum,0);
	grad.resize(cur_nnum+cur_wnum);
}

void NeuroNet::delNeuron()
{
	cur_nnum-=1;
	cur_wnum = cur_nnum*cur_nnum;
	init_value.pop_back();
	value.pop_back();
	weight.resize(cur_wnum,0);
	grad.resize(cur_nnum+cur_wnum);
};

float NeuroNet::gradRelease(vector <bool> arch, const float* sample, 
							int s_len, int max_iter)
{
	float prob;
	int i=0;
	for(; i<cur_wnum; i++)
		weight[i]=arch[i]*weight[i];

	float err, n_err,step_const;
	float fit_step = 100*DV;

	if(trajectory.size()<=s_len)
		trajectory.resize(s_len,0);
	
	this->calculate(s_len);
	this->clear();
	n_err = rsmd(&(trajectory[0]),sample,s_len,3);

	int m_i=0;

	grad.resize(cur_nnum+cur_wnum,0);
	err = n_err;

	for(; m_i<max_iter; m_i++)
	{
		rand_init(cur_nnum+cur_wnum,&(grad[0]),-fit_step*(n_err),2*fit_step*(n_err));
				
		err = n_err;
		i=0;
		for(; i<cur_nnum; i++)
		{
			this->alterValue(i,DV);
			grad[i] += (err-rsmd(&(trajectory[0]),sample,s_len,3))/DV;
		}

		for(; i<cur_wnum+cur_nnum; i++)
		{
			if(arch[i-cur_nnum])
			{
				this->alterWeight(i-cur_nnum,DV);
				grad[i] += (err-rsmd(&(trajectory[0]),sample,s_len,3))/DV;
			}
			else
				grad[i]=0;
		};

		norm(fit_step,&(grad[0]),grad.size());

		this->alterValue(&(grad[0]));
		this->alterWeight(&(grad[cur_nnum]));
		this->calculate(T_LEN);
		this->clear();

		n_err = rsmd(&(trajectory[0]),sample,s_len,3);

		if(n_err>err)
		{			
			prob = uniformRand(0,err);
			if((n_err-err)>prob)
			{
			for(int k=0; k<cur_nnum+cur_wnum; k++)
				grad[k]=-grad[k];
			this->alterValue(&(grad[0]));
			this->alterWeight(&(grad[cur_nnum]));
			this->calculate(T_LEN);
			this->clear();
			n_err = rsmd(&(trajectory[0]),sample,s_len,3);
			fit_step = fit_step/2;
			}
		}

		if(n_err==inf_p||n_err==inf_n||_isnan(n_err))
			return 10e30;

		step_calc(&fit_step,err,n_err);
	}
	return n_err;
};