# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1fFdc2VmR-WlTYkAvXl4vUG8F83HKnJmQ
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA

df = pd.read_csv('X.csv',parse_dates=True,usecols=['Date','Close'],index_col=0)
df.index = df.index.strftime("%Y-%d-%m")
df_diff = df.diff().dropna()


plt.figure(figsize=(10, 6))
plot_acf(df, lags=20, ax=plt.gca())
plt.title('Autocorrelation Function (ACF)')
plt.xlabel('Lag')
plt.ylabel('Autocorrelation')
plt.grid(True)
plt.show()

# Plot PACF
plt.figure(figsize=(10, 6))
plot_pacf(df, lags=20, ax=plt.gca())
plot_pacf(df_diff,lags = 20)
plt.title('Partial Autocorrelation Function (PACF)')
plt.xlabel('Lag')
plt.ylabel('Partial Autocorrelation')
plt.grid(True)
plt.show()

result = seasonal_decompose(df,'multiplicative',period=12)
result.plot()
plt.show()

# Perform ADF test
res = adfuller(df_diff)

# Extract and print the test statistic and p-value
print('ADF Statistic:', res[0])
print('p-value:', res[1])

df.diff().plot()

exchange_rate_df = df.copy(deep=True)
df_diff.plot()

# Assuming your data is stored in a DataFrame named 'exchange_rate_df'
train_size = int(len(exchange_rate_df) * 0.8)  # 80% training data
train_data = exchange_rate_df.iloc[:train_size]
test_data = exchange_rate_df.iloc[train_size:]

# Define ARIMA model
# Replace p, d, q with appropriate values
p = 1
d = 1
q = 1
model = ARIMA(train_data, order=(p, d, q))

# Fit ARIMA model
arima_model = model.fit()

print(arima_model.summary())

# Number of steps to forecast
n_steps = len(test_data)

# Make predictions
predictions = arima_model.forecast(steps=n_steps)

# Compare predictions with actual values
plt.plot(test_data.index, test_data, label='Actual')
plt.plot(test_data.index, predictions, label='Predicted')
plt.title('ARIMA Forecast')
plt.xlabel('Date')
plt.ylabel('Exchange Rate')
plt.legend()
plt.show()

# Calculate MAE
mae = np.mean(np.abs(predictions.values - test_data.values))
print('Mean Absolute Error (MAE):', mae)

# ETS Decomposition
result = seasonal_decompose(df, model ='multiplicative',period=12)

result.plot()

# To install the library
!pip install pmdarima
# Import the library
from pmdarima import auto_arima

# Ignore harmless warnings
import warnings
warnings.filterwarnings("ignore")

# Fit auto_arima function to AirPassengers dataset
stepwise_fit = auto_arima(train_data, start_p = 1, start_q = 1,
						max_p = 3, max_q = 3, m = 12,
						start_P = 0, seasonal = True,
						d = None, D = 1, trace = True,
						error_action ='ignore', # we don't want to know if an order does not work
						suppress_warnings = True, # we don't want convergence warnings
						stepwise = True)		 # set to stepwise

# To print the summary
stepwise_fit.summary()

from statsmodels.tsa.statespace.sarimax import SARIMAX

model = SARIMAX(train_data,
                order = (1, 0, 1),
                seasonal_order =(2, 1, 0, 12))

result = model.fit()
print(result.summary())

# Number of steps to forecast
n_steps = len(test_data)

# Make predictions
predictions = result.forecast(steps=n_steps)

start = len(train_data)
end = len(train_data) + len(test_data) - 1

# Predictions for one-year against the test set
predictions = result.predict(start, end,
                             typ = 'levels').rename("Predictions")

plt.plot(test_data.index, test_data, label='Actual')
plt.plot(test_data.index, predictions, label='Predicted')
plt.title('ARIMA Forecast')
plt.xlabel('Date')
plt.ylabel('Exchange Rate')
plt.legend()
plt.show()

# Calculate MAE
mae = np.mean(np.abs(predictions.values - test_data.values))
print('Mean Absolute Error (MAE):', mae)

# Rolling prediction
history = [x for x in train_data['Close']]
predic = []
for t in range(0,len(test_data)):
    model = SARIMAX(history,  order = (1, 0, 1),  seasonal_order =(2, 1, 0, 12))
    result = model.fit()
    pred = result.forecast(steps=1)
    predic.append(pred)
    history.append(test_data['Close'][t])

plt.plot(test_data.index, test_data, label='Actual')
plt.plot(test_data.index, predic, label='Predicted')
plt.gca().xaxis.set_major_locator(plt.MaxNLocator(20))
plt.xticks(rotation=45)
plt.title('ARIMA Forecast')
plt.xlabel('Date')
plt.ylabel('Exchange Rate')
plt.legend()
plt.show()

# Calculate MAE
mae = np.mean(np.abs(predictions.values - test_data.values))
print('Mean Absolute Error (MAE):', mae)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import SimpleExpSmoothing

# Assuming your data is stored in a DataFrame named 'time_series_df' with a single column 'value'
# Replace 'time_series_df' and 'value' with your actual DataFrame and column name
time_series_df = df.copy(deep=True)
# Define the alpha parameter for exponential smoothing
alpha = 0.2  # You can adjust this value based on the smoothing level you want

model = SimpleExpSmoothing(time_series_df)
fit_model = model.fit(smoothing_level=alpha, optimized=False)  # Set optimized=False to use the provided alpha value

# Forecast future values
forecast = fit_model.forecast(steps=30)  # Change 'steps' to the number of steps you want to forecast

# Calculate confidence interval
# Assuming residuals are normally distributed, use standard deviation of residuals as standard error
std_error = np.std(fit_model.resid)
z_value = 1.96  # For 95% confidence interval
margin_error = z_value * std_error

# Calculate upper and lower bounds of confidence interval
confidence_interval_lower = forecast - margin_error
confidence_interval_upper = forecast + margin_error

# Plot the original time series, forecast, and confidence interval
plt.figure(figsize=(10, 6))
plt.plot(time_series_df.index, time_series_df, label='Actual')
plt.plot(forecast.index, forecast, label='Forecast', color='orange')
plt.fill_between(forecast.index, confidence_interval_lower, confidence_interval_upper, color='gray', alpha=0.2, label='95% Confidence Interval')
plt.title('Exponential Smoothing Forecast with Confidence Interval')
plt.xlabel('Date')
plt.ylabel('Value')
plt.legend()
plt.show()

from statsmodels.tsa.holtwinters import ExponentialSmoothing

ts_df = df.copy(deep=True).dropna()
ts_df = train_data.copy(deep=True)

exp_model = ExponentialSmoothing(ts_df,trend='add',damped_trend=False,seasonal='mul',seasonal_periods=12)
exp_res = exp_model.fit(optimized=True)

# Forecast future values
forecast = exp_res.forecast(steps=len(test_data))  # Change 'steps' to the number of steps you want to forecast

# Calculate confidence interval
# Assuming residuals are normally distributed, use standard deviation of residuals as standard error
std_error = np.std(exp_res.resid)
z_value = 1.96  # For 95% confidence interval
margin_error = z_value * std_error

# Calculate upper and lower bounds of confidence interval
confidence_interval_lower = forecast - margin_error
confidence_interval_upper = forecast + margin_error

# Plot the original time series, forecast, and confidence interval
plt.figure(figsize=(10, 6))
plt.plot(df.index, df, label='Actual')
plt.plot(forecast.index, forecast, label='Forecast', color='orange')
# plt.plot(test_data.index,test_data,label='actual',color='blue')
plt.fill_between(forecast.index, confidence_interval_lower, confidence_interval_upper, color='gray', alpha=0.2, label='95% Confidence Interval')
plt.title('Exponential Smoothing Forecast with Confidence Interval')
plt.gca().xaxis.set_major_locator(plt.MaxNLocator(20))
plt.xticks(rotation=45)
plt.xlabel('Date')
plt.ylabel('Value')
plt.legend()
plt.show()

# Rolling forecast
history = [x for x in train_data['Close']]
predic = []
upper_CI = []
lower_CI = []
for t in range(0,len(test_data)):
    exp_model = ExponentialSmoothing(history,trend='add',damped_trend=False,seasonal='mul',seasonal_periods=12)
    exp_res = exp_model.fit(optimized=True)
    forecast = exp_res.forecast()
    std_error = np.std(exp_res.resid)
    z_value = 1.96  # For 95% confidence interval
    margin_error = z_value * std_error

    # Calculate upper and lower bounds of confidence interval
    confidence_interval_lower = forecast - margin_error
    confidence_interval_upper = forecast + margin_error
    upper_CI.append(confidence_interval_upper[0])
    lower_CI.append(confidence_interval_lower[0])
    predic.append(forecast)
    history.append(test_data['Close'][t])

upper_CI

plt.plot(test_data.index, test_data, label='Actual')
plt.plot(test_data.index, predic, label='Predicted')
plt.gca().xaxis.set_major_locator(plt.MaxNLocator(20))
plt.xticks(rotation=45)
plt.title('Exponential Forecast')
plt.xlabel('Date')
plt.ylabel('Exchange Rate')
plt.legend()
plt.show()

# Calculate MAE
mae = np.mean(np.abs(predictions.values - test_data.values))
print('Mean Absolute Error (MAE):', mae)

# Plot the original time series, forecast, and confidence interval
plt.figure(figsize=(10, 6))
plt.plot(df.index, df, label='Actual')
plt.plot(test_data.index, predic, label='Forecast', color='orange')
# plt.plot(test_data.index,test_data,label='actual',color='blue')
plt.fill_between(test_data.index, upper_CI,lower_CI, color='gray', alpha=0.2, label='95% Confidence Interval')
plt.gca().xaxis.set_major_locator(plt.MaxNLocator(20))
plt.xticks(rotation=45)
plt.title('Exponential Smoothing Forecast')
plt.xlabel('Date')
plt.ylabel('Value')
plt.legend()
plt.show()
