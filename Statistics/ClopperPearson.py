import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom

# calculate clopper pearson interval for a single pseudo experiment
def GetClopperPearsonInterval(npassed, ntotal, cl = 0.68):
    cp_up = 1.0
    cp_down = 0.0
    eff_estimate = npassed*1.0/ntotal
    prob = binom.cdf(npassed, ntotal, eff_estimate)
    while prob > (1.-cl)/2.:
        eff_estimate += 0.001
        prob = binom.cdf(npassed, ntotal, eff_estimate)
    cp_up = eff_estimate
    eff_estimate = npassed*1.0/ntotal
    prob = binom.cdf(npassed-1, ntotal, eff_estimate)
    while (1.-prob) > (1.-cl)/2.:
        eff_estimate -= 0.001
        prob = binom.cdf(npassed-1, ntotal, eff_estimate)
    cp_down = eff_estimate
    return [cp_down,cp_up]

# calculate clopper pearson interval for an array of pseudo experiments -> vectorized -> faster
def GetClopperPearsonIntervalV(npassed, ntotal, cl=0.68):
    eff_estimate = npassed/ntotal
    prob = binom.cdf(npassed, ntotal, eff_estimate)
    edge_reached = np.logical_not(prob > (1.-cl)/2.)
    while not np.all(edge_reached):
        eff_estimate = np.where(edge_reached, eff_estimate, eff_estimate+0.001)
        prob = binom.cdf(npassed, ntotal, eff_estimate)
        edge_reached = np.where(prob > (1.-cl)/2., False, True)
    cp_up = eff_estimate
    eff_estimate = npassed/ntotal
    prob = binom.cdf(npassed-1, ntotal, eff_estimate)
    edge_reached = np.logical_not((1.-prob) > (1.-cl)/2.)
    while not np.all(edge_reached):
        eff_estimate = np.where(edge_reached, eff_estimate, eff_estimate-0.001)
        prob = binom.cdf(npassed-1, ntotal, eff_estimate)
        edge_reached = np.where((1.-prob) > (1.-cl)/2., False, True)
    cp_down = eff_estimate
    return np.array([cp_down,cp_up])

# initilaize two random generators for the two corresponding pseudo experiments
rng1 = np.random.default_rng()

rng2 = np.random.default_rng()

# number of pseudo experiments
nexperiments = 100

# parameters for first efficiency pseudoexperiment
true_eff1 = 0.95
ntotal1 = 100
nexperiments1 = nexperiments

# parameters for second efficiency pseudoexperiment
true_eff2 = 0.99
ntotal2 = 200
nexperiments2 = nexperiments

# throws first pseudoexperiments and calculate the estimated efficiencies
passed1 = rng1.binomial(n=ntotal1, p=true_eff1, size=nexperiments1)

effs1 = passed1/ntotal1

# thorw second pseudoexperiments and calculate the estimated efficiencies
passed2 = rng2.binomial(n=ntotal2, p=true_eff2, size=nexperiments2)

effs2 = passed2/ntotal2

#print(effs1)
#print(effs2)

# Calculate Clopper-Pearson intervals for all the pseudo experiments
intervals1=GetClopperPearsonIntervalV(passed1,ntotal1)
intervals2=GetClopperPearsonIntervalV(passed2,ntotal2)

#print(intervals1)
#print(intervals2)

# count the number of times the true efficiencies are within the CP intervals
true_in_interval1 = np.count_nonzero((intervals1[0]<=true_eff1)&(intervals1[1]>=true_eff1))
true_in_interval2 = np.count_nonzero((intervals2[0]<=true_eff2)&(intervals2[1]>=true_eff2))

print("Number of intervals1 that contain the true value 1: ", true_in_interval1)
print("Number of trials 1: ", nexperiments1)
print("Coverage1: ", true_in_interval1/nexperiments1)

print("Number of intervals2 that contain the true value 2: ", true_in_interval2)
print("Number of trials 2: ", nexperiments2)
print("Coverage2: ", true_in_interval2/nexperiments2)

# calculate the scale factors i.e. the ratios of the efficiencies
sfs = effs1/effs2

# true scale factor
true_sf = true_eff1/true_eff2

print("True sf: ", true_sf)

#print(sfs)

# calculate conservative uncertainty intervals for the scale factors
sfs_intervals = np.array([intervals1[0]/intervals2[1],intervals1[1]/intervals2[0]])

#print(sfs_intervals)

# count the number of times the true sf is within the interval
true_in_sf_interval = np.count_nonzero((sfs_intervals[0]<=true_sf)&(sfs_intervals[1]>=true_sf))

print("Number of sf intervals that contain the true sf: ", true_in_sf_interval)
print("Number of trials: ", nexperiments)
print("Coverage: ", true_in_sf_interval/nexperiments)

# plot some stuff
fig,ax = plt.subplots(3)

x=np.linspace(0.0, nexperiments1, num=nexperiments1)

y=effs1
y_error_low = effs1-intervals1[0]
y_error_high = intervals1[1]-effs1

ax[0].errorbar(x, y, yerr=[y_error_low,y_error_high], fmt='o', label="pseudo experiments")
ax[0].axhline(y=true_eff1, color='r', linestyle='-', label="true efficiency")
ax[0].set(ylabel="efficiency 1")
ax[0].text(0.95, 0.01, "coverage: {}".format(true_in_interval1/nexperiments1),
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax[0].transAxes,
        color='green', fontsize=15)
ax[0].text(0.65, 0.01, "sample size: {}".format(ntotal1),
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax[0].transAxes,
        color='green', fontsize=15)
ax[0].legend(loc="upper right")
#ax[0].set_title("efficiency 1")

y=effs2
y_error_low = effs2-intervals2[0]
y_error_high = intervals2[1]-effs2

ax[1].errorbar(x, y, yerr=[y_error_low,y_error_high], fmt='o', label="pseudo experiments")
ax[1].axhline(y=true_eff2, color='r', linestyle='-', label="true efficiency")
ax[1].set(ylabel="efficiency 2")
ax[1].text(0.95, 0.01, "coverage: {}".format(true_in_interval2/nexperiments2),
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax[1].transAxes,
        color='green', fontsize=15)
ax[1].text(0.65, 0.01, "sample size: {}".format(ntotal2),
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax[1].transAxes,
        color='green', fontsize=15)
ax[1].legend(loc="upper right")
#ax[1].set_title("efficiency 2")

y=sfs
y_error_low = sfs-sfs_intervals[0]
y_error_high = sfs_intervals[1]-sfs

ax[2].errorbar(x, y, yerr=[y_error_low,y_error_high], fmt='o', label="pseudo experiments")
ax[2].axhline(y=true_sf, color='r', linestyle='-', label="true sf")
ax[2].set(ylabel="scale factor")
ax[2].text(0.95, 0.01, "coverage: {}".format(true_in_sf_interval/nexperiments2),
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax[2].transAxes,
        color='green', fontsize=15)
ax[2].legend(loc="upper right")
#ax[2].set_title("scale factor")

plt.xlabel("index of pseudo experiment")
plt.suptitle("clopper pearson playground")

plt.show()

plt.clf()

n, bins, patches = plt.hist(sfs, 20, density=False, facecolor='g', alpha=0.75, label="pseudo experiments")
plt.axvline(true_sf, color='r', linestyle='dashed', linewidth=1, label="true sf")
plt.axvline(sfs.mean(), color='b', linestyle='dashed', linewidth=1, label="mean")
plt.axvline(sfs.mean()+sfs.std(), color='black', linestyle='dashed', linewidth=1, label="mean+std")
plt.axvline(sfs.mean()-sfs.std(), color='black', linestyle='dashed', linewidth=1, label="mean-std")
plt.xlabel("scale factor")
plt.ylabel("number of pseudo experiments")

plt.legend()

plt.show()
