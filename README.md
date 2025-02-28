# TMB_high
How to identify TMB high patients

# What is TMB (Tumor Mutational Burden)?
"TMB high" typically refers to a high Tumor Mutational Burden (TMB) in the context of cancer research and immunotherapy. TMB is a measure of the number of mutations present in a tumor's DNA. A high TMB indicates that there are a large number of mutations in the tumor.

In cancer research, TMB high is often associated with better responses to certain types of immunotherapy, such as immune checkpoint inhibitors. Tumors with high TMB may have a higher likelihood of being recognized by the immune system as foreign, leading to a stronger immune response against the tumor.

Researchers and clinicians may use TMB as a biomarker to predict response to immunotherapy and to guide treatment decisions for cancer patients. High TMB is one of the factors considered when assessing a patient's suitability for immunotherapy treatment.

It's important to note that the interpretation of TMB results and its clinical significance may vary depending on the specific cancer type, treatment approach, and individual patient characteristics.

# Why we need to identify TMB high?
Identifying patients with high Tumor Mutational Burden (TMB) in cancer research and clinical practice is important for several reasons:

Predicting Response to Immunotherapy: High TMB has been associated with better responses to immune checkpoint inhibitors, a type of immunotherapy that helps the immune system recognize and attack cancer cells. Patients with high TMB may have a higher likelihood of responding positively to immunotherapy compared to those with low TMB.

Guiding Treatment Decisions: TMB can serve as a predictive biomarker for selecting patients who are more likely to benefit from immunotherapy. Identifying patients with high TMB can help oncologists tailor treatment plans and make informed decisions about the most appropriate therapeutic approach.

Personalized Medicine: Precision medicine aims to customize healthcare decisions and treatments based on individual patient characteristics, including genetic makeup. TMB assessment allows for a more personalized approach to cancer treatment by identifying patients who are likely to respond to specific therapies.

Prognostic Value: In some cancer types, high TMB has been associated with improved overall survival and progression-free survival rates. Identifying patients with high TMB may help in predicting the prognosis and disease outcome, allowing for better patient management and follow-up care.

Research and Clinical Trials: Identifying patients with high TMB is crucial for conducting research studies and clinical trials focused on immunotherapy and targeted therapies. By including patients with high TMB, researchers can evaluate the efficacy and safety of novel treatments in a specific subgroup of patients.

Overall, identifying patients with high TMB is essential for optimizing cancer treatment strategies, improving patient outcomes, advancing research in the field of immuno-oncology, and moving towards more personalized and effective cancer care.

# The threshold for TMB-high
In fact, there is no efficient way to determine the TMB-high threshold. The golden standard for determining the TMB-high threshold involves identifying TMB values where there is a significant improvement in ICI treatment outcomes. Sequencer, sequencing panel, cancer species, and ICI drugs used have a significant impact on TMB high.
So, obviously, here are several strategies for TMB-high threshold determination:
1. To practice, as the golden standard requires
2. Use the hard thresholding presented by FDA, such as > 10 mu/Mb for pembrolizumab user
3. Use the soft thresholding presented by statistics, this method will be mainly discussed here

# Soft thresholding determination
We assumed that there is only one dimension TMB score data without ICI outcomes in a big dataframe, which is calculated by filtered VCF file, with no germline or low-quality variants.
Here, I used WES and a unofficial panel covering 2.01 Mb gene exon regions. The first thing is to verfy the "consistence" between TMB scores from WES and unofficial panel.
```R
## cosine similarity
df <- read.table('TMB_score_WES.txt', sep='\t', header = TRUE)
tmb <- df$TMB_score
wes <- df$WES
sum(tmb*wes) / (sqrt(sum(tmb^2))*sqrt(sum(wes^2))) ## 0.9923412

## spearman correlation
cor.test(tmb, wes, method=c("spearman")) ## 0.9217614 
```
Undoubtedly, the panel is qualified for the high correlation.
Then, we need to split the big dataframe according to the cancer type using type_split.py script.
```python
## split merged file into small dataframe according to cancer type
def split_store(merged_file, store_path):
    df = merged_file
    dfs = {}
    for type_val, group in df.groupby('cancer_type'):
        dfs[type_val] = group
        
    for type_val, sub_df in dfs.items():
        file_name = f"{type_val}_data.tsv"
        output_path = store_path + '/' + file_name
        sub_df.to_csv(output_path, index=False, sep='\t', encoding='utf')
        print(f"save {type_val} to {file_name}")
```
There are several methods for one-dimension data cluster, such as Kmeans and Jerks. Here I recommond Kmeans, because Jerks cost too much time, and never output the center for each cluster.
The script used in this ariticle were KMeans4one_dimension.py and Jerks.py.
I selected non-small cell lung cancer as an example, with 86 pantients, outputing 6.111765 as the result, while 75 and 80 quantiles were 8.375 and 9.5 respectively. In general, as clinical trial do, they prefered median/quantile75/quantile80 as the TMB-high score threshold. I thind their choices are true, because we don't need to consider too much for one dimensional data.
