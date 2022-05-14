# コールセンター、HR、工場部門に対するAIソリューション調査

#csvインストール
df_all <- read.csv("factor_analysis - シート1.csv",header = TRUE)
df_all

#相関係数行列
cor_matrix <- cor(df_all[,2:10])
cor_matrix

#プロマックス回転によって因子分析
fac_anal <- factanal(df_all[,2:10],3,rotation = "promax")
fac_anal

#最後にクロンバックαを算出し、質問項目の信頼性をチェック
#①音声に関する質問項目のクロバックα→-0.28
library(psy)
tmp1 <- df_all[2:4]
tmp1
sum_score <- rowSums(tmp1)
tmp2 <- cbind(tmp1,sum_score)
tmp2
cronbach(tmp2[,1:3])

#②言語に関する質問項目のクロバックα→0.91
library(psy)
tmp3 <- df_all[5:7]
sum_score <- rowSums(tmp3)
tmp4 <- cbind(tmp3,sum_score)
cronbach(tmp4[,1:3])

#③画像に関する質問項目のクロンバックα→0.94
library(psy)
tmp5 <- df_all[8:10]
sum_score <- rowSums(tmp5)
tmp6 <- cbind(tmp5,sum_score)
cronbach(tmp6[,1:3])

