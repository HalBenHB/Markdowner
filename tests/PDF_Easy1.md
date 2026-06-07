# FIN 302 Corporate Finance
**Spring 2022-2023**

**Problem Set #1**

1. You want to create a portfolio equally as risky as the market, and you have $1,000,000 to invest. Given this information, fill in the rest of the following table:

| Asset | Investment | Beta |
| :--- | :--- | :--- |
| Stock A | $195,000 | 0.9 |
| Stock B | $340,000 | 1.15 |
| Stock C | | 1.29 |
| Risk-free asset | | |

We know the total portfolio value and the investment of two stocks in the portfolio, so we can find the weight of these two stocks. The weights of Stock A and Stock B are:

$$w_A = \$195,000 / \$1,000,000 = .195$$

$$w_B = \$340,000 / \$1,000,000 = .340$$

Since the portfolio is as risky as the market, the $\beta$ of the portfolio must be equal to one. We also know the $\beta$ of the risk-free asset is zero. We can use the equation for the $\beta$ of a portfolio to find the weight of the third stock. Doing so, we find:

$$\beta_P = 1 = w_A(.90) + w_B(1.15) + w_C(1.29) + w_{Rf}(0)$$

$$1 = .195(.90) + .34(1.15) + w_C(1.29)$$

Solving for the weight of Stock C, we find:

$$w_C = .33604651$$

So, the dollar investment in Stock C must be:

$$Invest\ in\ Stock\ C = .33604651(\$1,000,000) = \$336,046.51$$

We also know the total portfolio weight must be one, so the weight of the risk-free asset must be one minus the asset weight we know, or:

$$1 = w_A + w_B + w_C + w_{Rf} = 1 - .195 - .340 - .33604651 - w_{Rf}$$

$$w_{Rf} = .12895349$$

So, the dollar investment in the risk-free asset must be:

$$Invest\ in\ risk\text{-}free\ asset = .12895349(\$1,000,000) = \$128,953.49$$

2. Consider the following information about Stocks I and Stock II:

| State of Economy | Probability of state of Economy | Rate of Return if state Occurs (Stock I) | Rate of Return if state Occurs (Stock II) |
| :--- | :---: | :---: | :---: |
| Recession | 0.25 | 0.02 | -0.25 |
| Normal | 0.5 | 0.21 | 0.09 |
| Boom | 0.25 | 0.06 | 0.44 |

The market risk premium is 7 percent, and the risk-free rate is 4 percent. Which stock has the most systematic risk? Which one has the most total risk? Which stock is riskier? Explain.

The amount of systematic risk is measured by the $\beta$ of an asset. Since we know the market risk premium and the risk-free rate, if we know the expected return of the asset we can use the CAPM to solve for the $\beta$ of the asset.

The expected return of Stock I is:

$$E(R_I) = .25(.02) + .50(.21) + .25(.06) = .1250,\ or\ 12.50\%$$

Using the CAPM to find the $\beta$ of Stock I, we find:

$$.1250 = .04 + .07\beta_I$$

$$\beta_I = 1.21$$

The total risk of the asset is measured by its standard deviation, so we need to calculate the standard deviation of Stock I. Beginning with the calculation of the stock’s variance, we find:

$$\sigma_I^2 = .25(.02 - .1250)^2 + .50(.21 - .1250)^2 + .25(.06 - .1250)^2$$

$$\sigma_I^2 = .00743 \quad \sigma_I = (.00743)^{1/2} = .0862,\ or\ 8.62\%$$

Using the same procedure for Stock II, we find the expected return to be:

$$E(R_{II}) = .25(-.25) + .50(.09) + .25(.44) = .0925$$

Using the CAPM to find the $\beta$ of Stock II, we find:

$$.0925 = .04 + .07\beta_{II} \quad \beta_{II} = 0.75$$

And the standard deviation of Stock II is:

$$\sigma_{II}^2 = .25(-.25 - .0925)^2 + .50(.09 - .0925)^2 + .25(.44 - .0925)^2$$

$$\sigma_{II}^2 = .05952 \quad \sigma_{II} = (.05952)^{1/2} = .2440,\ or\ 24.40\%$$

Although Stock II has more total risk than I, it has much less systematic risk, since its beta is much smaller than I’s. Thus, I has more systematic risk, and II has more unsystematic and more total risk. Since unsystematic risk can be diversified away, I is actually the “riskier” stock despite the lack of volatility in its returns. Stock I will have a higher risk premium and a greater expected return.