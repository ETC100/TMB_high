#!/usr/bin/env Rscript
if (!require("dplyr")) install.packages("dplyr")
library(dplyr)

# 示例探针数据
# probe_data <- data.frame(
#   probe_name = c("probe1", "probe2", "probe3", ...),
#   chromosome = c("chr1", "chr1", "chr2", ...),
#   start = c(100, 150, 200, ...),
#   end = c(200, 250, 300, ...)
# )

read.table('C:\\Users\\Administrator\\Desktop\\SCLC.txt', header = TRUE) -> probe_data
colnames(probe_data) <- c('chrom', 'start', 'end')

# 按染色体和起始位置排序
probe_data <- probe_data %>%
  arrange(chrom, start)

# 合并重叠区域
merged_intervals <- list()
current_chrom <- ""
current_start <- NA
current_end <- NA

for (i in 1:nrow(probe_data)) {
  chrom <- probe_data$chrom[i]
  start <- probe_data$start[i]
  end <- probe_data$end[i]
  
  if (chrom != current_chrom || is.na(current_end) || start > current_end) {
    # 新的区域
    if (!is.na(current_chrom)) {
      merged_intervals <- append(merged_intervals, list(c(current_chrom, current_start, current_end)))
    }
    current_chrom <- chrom
    current_start <- start
    current_end <- end
  } else {
    # 合并重叠区域
    current_end <- max(current_end, end)
  }
}

# 添加最后一个区域
merged_intervals <- append(merged_intervals, list(c(current_chrom, current_start, current_end)))

# 计算总覆盖大小
sum = 0
for (i in 2:16899) {
  temp <- merged_intervals[[i]]
  sum = sum + (as.numeric(temp[3]) - as.numeric(temp[2]))
}

print(paste("Total coverage size on genome: ", sum/1000000))

as.data.frame(merged_intervals[[2]]) -> row1
for (i in 3:16899){
  row2 <- as.data.frame(merged_intervals[[i]])
  row1 <- cbind(row1, row2)
}

row1 <- t(row1)
write.table(row1, file = "D:\\cancer_type\\probe_range.tsv", sep='\t')
