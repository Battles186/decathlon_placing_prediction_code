# Analysis of decathlon placing data.

library(ggplot2)
library(fitdistrplus)
library(DescTools)
library(car)
library(randomForest)
library(boot)

# Preparatory things to ensure that the analysis can be reproduced.
set.seed(20260104)

# Load data.
data <- read.csv("data/data_mark_postprocessed.csv")
names_current <- names(data)
# names_new <- c()
# for (name in names_current) {
# 	if (substring(name, 1, 1) == 'X') {
# 		names_new <- c(names_new, substring(name, 2))
# 	} else {
# 		names_new <- c(names_new, name)
# 	}
# }
# names(data) <- names_new

# Define outcome and predictors.
outcome <- 'pos'
predictors <- c(
	'X100_speed', 'lj', 'sp', 'hj', 'X400_speed',
	'X110h_speed', 'dt', 'pv', 'jt', 'X1500_speed'
)

# Determine the distribution of the outcome variable.
hist(data[['pos']])
# Fit curves.
pois_fit <- fitdist(data[[outcome]], distr='pois', method='mle')
gamma_fit <- fitdist(data[[outcome]], distr='gamma', method='mle')
# Simulate data.
data_pois <- rpois(n=length(data[[outcome]]), lambda=coef(pois_fit)[1])
data_gamma <- rgamma(
	n=length(data[[outcome]]),
	shape=coef(gamma_fit)[1],
	rate=coef(gamma_fit)[2],
)
# Use Kilmogorov-Smirnov to test if the distributions are different.
ks_result_pois <- ks.test(data[[outcome]], data_pois)
ks_result_gamma <- ks.test(data[[outcome]], data_gamma)

print(ks_result_pois)
print(ks_result_gamma)

# Fit a gamma model to the data.
form <- paste(outcome, "~", paste(predictors, collapse=" + "))

# Subset the data for easier model fitting.
data_subset <- data[c(outcome, predictors)]

# Use robust scaling on the predictors.
data_scaled <- data_subset
data_scaled[predictors] <- RobScale(data_subset[predictors])

# Fit gamma model to the data.
model <- glm(
	form,
	data=data_scaled,
	# Log link works, but deviance was vastly lower with
	# identity link. I think we should supply some parameter
	# guesses or remove outliers. Alternatively, could fit
	# model with times rather than speeds since it seemed
	# to work then.
	family=Gamma(link="log"),
	control=list(trace=TRUE),
)

# Look at variance inflation factors to see if we should
# refit without them.
vif_ <- vif(model)
print(any(vif_ > 5))
plot(fitted(model), data_scaled[['pos']])

# Look at influential outliers.
inf_m <- influence.measures(model)
inf_m_col_sums <- colSums(inf_m$is.inf)

idx_inf_multiple <- which(rowSums(inf_m$is.inf) > 1)

# Subset the data.
data_scaled_no_outliers <- data_scaled[-idx_inf_multiple, ]

# Refit without influential outliers.
model_updated <- glm(
	form,
	data=data_scaled_no_outliers,
	# Log link works, but deviance was vastly lower with
	# identity link. I think we should supply some parameter
	# guesses or remove outliers. Alternatively, could fit
	# model with times rather than speeds since it seemed
	# to work then.
	family=Gamma(link="log"),
	control=list(trace=TRUE),
)
plot(fitted(model_updated), data_scaled_no_outliers$pos)

# It seems like there's a very poor model fit at or above
# placings of 16 or higher. Refit without those observations.
# idx_placing_above_10 <- which(data_scaled_no_outliers['pos'] > 10)
# data_scaled_no_outliers_sub_11 <- data_scaled_no_outliers[-idx_placing_above_10, ]
# model_updated_sub_11 <- glm(
# 	form,
# 	data=data_scaled_no_outliers_sub_11,
# 	family=Gamma(link="log"),
# 	control=list(trace=TRUE),
# )
# hist(data_scaled_no_outliers_sub_11[['pos']])
# plot(fitted(model_updated_sub_11), data_scaled_no_outliers_sub_11[['pos']])

# Look at model coefficients.
print(coef(model_updated))

pred.gamma <- predict.glm(model_updated, newdata=data_scaled_no_outliers, type="response")
rmse.gamma <- sqrt(mean(pred.gamma - data_scaled_no_outliers$pos)^2)
mae.gamma <- mean(abs(pred.gamma - data_scaled_no_outliers$pos))

# Plot coefficients.

data.frame.coef = data.frame(
	names=toupper(names(coef(model_updated))[2:11]),
	values=as.numeric(coef(model_updated))[2:11]
)

png("output/images/glm_coef.png")
ggplot(
	data = data.frame.coef,
	mapping = aes(x = names, y = values)
) + geom_col()
dev.off()

# ==== Random Forest ====

df <- data.frame(data_scaled)
samp <- sample(c(TRUE, FALSE), nrow(df), replace=TRUE, prob=c(0.7, 0.3))
df.train <- df[samp, ]
df.test <- df[!samp, ]

rf <- randomForest(
	pos ~ .,
	data = df.train
)

which.min(rf$mse)
sqrt(rf$mse[which.min(rf$mse)])

# Plot model fit.
plot(rf)

png("output/images/rf_coef.png")
varImpPlot(rf)
dev.off()

rf_tuned <- tuneRF(
	x=df.train[, -1],
	y=df.train$pos,
	ntreeTry=500,
	mtryStart=4,
	stepfactor=1.5,
	improve=0.01,
	trace=FALSE
)

rf_final <- randomForest(
	pos ~ .,
	data = df.train,
	ntree = 384,
	mtry = 8
)

pred.test <- predict(rf, df.test)

plot(pred.test, df.test$pos)

rmse.test <- sqrt(mean((pred.test - df.test$pos)^2))
mae.test <- mean(abs(pred.test - df.test$pos))

# This code taken from ~/Documents/research_projects/decathlon_career_best/coef_bootstrap_CIs.r

# Bootstrapped coefficient comparisons.
boot_iter_diff <- function(df_og, i, coef_idx_a, coef_idx_b, model_link) {
	#print("Number of data points in bootstrap sample:")
	#print(length(i))

	# Select data.
	data_boot = df_og[i, ]

	# Fit model.
	fit <- glm(pos ~ ., data=data_boot, family=Gamma(link=model_link))

	# Compute output.
	coef_out <- coefficients(fit)

	# Return the difference in means.
	return(coef_out[coef_idx_a] - coef_out[coef_idx_b])
}

# Bootstrapped confidence intervals.
boot_ci <- function(data, coef_idx_a, coef_idx_b, coef_names, model_link) {
	# Generate bootstrap object.
	boot.obj <- boot(
		data=data, statistic=boot_iter_diff, R=1000,
		coef_idx_a=coef_idx_a, coef_idx_b=coef_idx_b, model_link=model_link
	)

	png(paste("output/images/bootstrap_confidence_intervals/", coef_idx_a, 'vs', coef_idx_b, '.png', sep=''))
	plot(boot.obj)
	dev.off()

	# Generate confidence intervals.
	confidence_intervals <- boot.ci(boot.obj, type=c("bca"))

	# Print output.
	print(paste("Confidence interval for", coef_names[coef_idx_a], "-", coef_names[coef_idx_b]))
	print(confidence_intervals)

	# Return confidence intervals.
	return(confidence_intervals)
}

# Bootstrap matrix generator.
CI_bootstrap_matrix <- function(data, coef_names, event_idx_start=2, event_idx_end=11, model_link="log") {
	# Create the matrix that will store our coefficient values.
	n_coef <- event_idx_end - event_idx_start + 1
	coef_matrix <- matrix(
		0, n_coef, n_coef,
		dimnames=list(
			coef_names[event_idx_start:event_idx_end],
			coef_names[event_idx_start:event_idx_end]
		)
	)

	# Populate matrix.
	for (i in 1:n_coef) {
		for (j in 1:n_coef) {
			coef_idx_a <- event_idx_start + i - 1
			coef_idx_b <- event_idx_start + j - 1
			if (coef_idx_a != coef_idx_b) {
				# Construct confidence interval.
				ci_result <- boot_ci(
					data=data,
					coef_idx_a=coef_idx_a, coef_idx_b=coef_idx_b,
					coef_names=coef_names, model_link=model_link
				)

				# Grab bias-corrected accelerated confidence interval values.
				ci <- ci_result$bca

				print(paste("matrix idx: ", i, ", ", j, sep=""))
				print(paste("coef_idx: ", coef_idx_a, ", ", coef_idx_b, sep=""))
				print(ci)

				# If the lower bound is above 0, the whole interval is above 0 and the row coefficient
				# (corresponding to index `i`) is larger.
				if (ci[4] > 0) {
					coef_matrix[i, j] <- -10
				}
				# If the upper bound is below 0, the whole interval is below 0 and the row coefficient
				# is smaller.
				else if (ci[5] < 0) {
					coef_matrix[i, j] <- 10
				}
				# If zero is in the interval, neither is significantly larger than
				# the other at this alpha.
				else {
					coef_matrix[i, j] <- 0
				}
			}
		}
	}

	return(coef_matrix)
}

# Generate matrix of coefficient comparisons.
boot_ci_matrix_gamma <- CI_bootstrap_matrix(
	data=data_scaled_no_outliers, coef_names=names(coef(model_updated)),
	event_idx_start=2, event_idx_end=11,
	model_link="log"
)

write.csv(boot_ci_matrix_gamma, "output/boot_ci_matrix_gamma.csv")

