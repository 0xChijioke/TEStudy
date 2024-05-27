import matplotlib.pyplot as plt
import numpy as np



class LiquidityPool:
    def __init__(self, L, sqrt_P_high, sqrt_P_low):
        self.L = L
        self.sqrt_P_high = sqrt_P_high
        self.sqrt_P_low = sqrt_P_low

        # P_high and P_low from their square roots
        self.P_high = sqrt_P_high ** 2
        self.P_low = sqrt_P_low ** 2

    def invariant_function(self, x, y):
        """the invariant value."""
        return (x + self.L / self.sqrt_P_high) * (y + self.L * self.sqrt_P_low) - self.L ** 2

    def bonding_curve(self, x_range):
        """the bonding curve for a given range of x values."""
        bonding_curve_values = []
        for x in x_range:
            bonding_curve_value = self.L ** 2 / (x + self.L / self.sqrt_P_high) - self.L * self.sqrt_P_low
            bonding_curve_values.append(bonding_curve_value)
        return bonding_curve_values


    def delta_y(self, x, delta_x):
        """delta y for a given delta x."""
        delta_y = -delta_x * self.L ** 2 / ((x + self.L / self.sqrt_P_high) * (x + delta_x + self.L / self.sqrt_P_high))
        return delta_y

    def calculate_x(self, y):
        """Calculate x given y."""
        x = (self.L ** 2 / self.sqrt_P_high - y + self.L * self.sqrt_P_low) / (self.sqrt_P_high + self.L / self.sqrt_P_low)
        return x

    def calculate_y(self, x):
        """Calculate y given x."""
        y = -self.L * self.sqrt_P_low / (x * self.sqrt_P_high + self.L) + self.L ** 2 / self.sqrt_P_low
        return y

    def marginal_price(self, x, y):
        """marginal price at a given point."""
        numerator = -self.sqrt_P_high * (y + self.L * self.sqrt_P_low)
        denominator = x * self.sqrt_P_high + self.L
        marginal_price = numerator / denominator
        return marginal_price

# initial conditions for Pool 1
L1 = 130
sqrt_P_high1 = 8
sqrt_P_low1 = 4

# Pool 1
pool1 = LiquidityPool(L1, sqrt_P_high1, sqrt_P_low1)

# initial conditions for Pool 2
L2 =90
sqrt_P_high2 = sqrt_P_low1
sqrt_P_low2 = 0.4




# Pool 2
pool2 = LiquidityPool(L2, sqrt_P_high2, sqrt_P_low2)


# range of x values for plotting
x_range = np.linspace(0, 200, 500)

# bonding curves
plt.figure(figsize=(12, 8))


plt.plot(x_range, pool1.bonding_curve(x_range), label=f"Pool 1 Bonding Curve\nInvariant: x + L/√P_high * y + L*√P_low = L^2")
plt.plot(x_range, pool2.bonding_curve(x_range), label=f"Pool 2 Bonding Curve\nInvariant: x + L/√P_high * y + L*√P_low = L^2")



# axis limits
plt.xlim(0, 200)
plt.ylim(0, 500)


# Final presentation
plt.title("Visualizing Contiguous Liquidity Pools with Bonding and Price Curves")
plt.xlabel("Token X")
plt.ylabel("Token Y")
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.show()