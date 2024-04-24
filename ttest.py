from scipy import stats
from statsmodels.stats.multitest import fdrcorrection

def ttest(group1, group2):
    if (
        stats.levene(
            group1,
            group2,
        )[1]
        > 0.05
    ):
        variant_eaual = True
    else:
        variant_eaual = False
    t, p = stats.ttest_ind(
        group1,
        group2,
        equal_var=variant_eaual,
    )
    # print("\tp:{}".format(p))
    return t, p