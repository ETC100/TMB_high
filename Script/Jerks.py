import pandas as pd


def read_table(file_path, cancer_type):
    df = pd.read_table(file_path, sep='\t', encoding='gbk')
    variants = df.loc[df['cancer_type'] == cancer_type, 'count'].values
    return variants


class Jerks:
    def __init__(self, file_path, cancer_type):
        self.data = read_table(file_path, cancer_type)

    def getaverage(self, data):
        return sum(data) / len(data)

    def partition_helper(self, data, start, group1, group2, all_partitions):
        if start == len(data):
            if group1 and group2:
                all_partitions.append([group1, group2])
            return
        self.partition_helper(data, start + 1, group1 + [data[start]], group2, all_partitions)
        self.partition_helper(data, start + 1, group1, group2 + [data[start]], all_partitions)

    def all_partitions(self):
        all_partitions = []
        self.partition_helper(self.data, 0, [], [], all_partitions)
        return all_partitions

    def get_variance(self, data):
        avg = self.getaverage(data)
        sdam = 0
        for i in range(len(data)):
            sdam += (data[i] - avg) ** 2
        return sdam

    def get_sdam(self):
        return self.get_variance(self.data)

    def get_sdcm(self, group1, group2):
        return self.get_variance(group1) + self.get_variance(group2)

    def get_best_gvf(self):
        result = self.all_partitions()
        gvf_list = []
        sdam = self.get_sdam()
        for i in range(len(result)):
            gvf = (sdam - self.get_sdcm(result[i][0], result[i][1])) / sdam
            gvf_list.append(gvf)
        max_index = gvf_list.index(max(gvf_list))
        print(result[max_index])


def main():
    jerks = Jerks(r'D:\cancer_type\TMB2.tsv', '小细胞肺癌')
    jerks.get_best_gvf()


if __name__ == "__main__":
    main()
