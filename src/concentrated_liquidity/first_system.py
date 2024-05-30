import matplotlib.pyplot as plt
import numpy as np


class LiquidityPool:
    def __init__(self, x0, y0, A):
        self.x0 = x0
        self.y0 = y0
        self.A = A
        self.invariant = self.A ** 2 * self.x0 * self.y0

    def bonding_curve(self, x_range):
        """the bonding curve for a given range of x values."""
        bonding_curve_values = (self.invariant / ((self.A - 1) * x_range + self.x0)) - (self.y0 * (self.A - 1))
        return bonding_curve_values

    def calculate_y(self, x):
        return (self.invariant / ((self.A - 1) * x + self.x0)) - (self.y0 * (self.A - 1))

    def price_curve_derivative(self, x):
        return -((self.A ** 2 * self.x0 * self.y0) / ((x + self.x0 * (self.A - 1)) ** 2))

    def calculate_marginal_rate(self, x, y):
        return -((y + self.y0 * (self.A - 1)) / (x + self.x0 * (self.A - 1)))

    def calculate_phigh(self):
        return (self.A ** 2 / (self.A - 1) ** 2) * (self.y0 / self.x0)

    def calculate_plow(self):
        return ((self.A - 1) ** 2 / self.A ** 2) * (self.y0 / self.x0)

def set_balances_and_A():
    # Set parameters for Pool 1
    A1 = 3
    x0_1 = 40
    y0_1 = 270

    # Set parameters for Pool 2
    A2 = 3
    x0_2 = 100
    y0_2 = 133.33333333333333

    return A1, A2, x0_1, y0_1, x0_2, y0_2

def plot_bonding_curves(pool1, pool2, delta_x):
    fig, (ax1) = plt.subplots(1, 1, figsize=(16, 8))

    # Plot bonding curves
    x_range = np.linspace(0, 100, 101)
    y_range_pool1 = pool1.bonding_curve(x_range)
    y_range_pool2 = pool2.bonding_curve(x_range)


    label_pool1 = (f'Bonding Curve Pool 1\nx0={pool1.x0}, y0={pool1.y0}, A={pool1.A}, '
                   f'phigh={pool1.calculate_phigh()}, plow={round(pool1.calculate_plow(), 4)}\n' # Adjusted precision for the displayed plow1 and phigh2(below)
                   f'Formula: y = {pool1.A ** 2 * pool1.y0} / (({pool1.A} - 1) * x + {pool1.x0}) - ({pool1.y0} * ({pool1.A} - 1))')
    
    label_pool2 = (f'Bonding Curve Pool 2\nx0={pool2.x0}, y0={pool2.y0}, A={pool2.A}, '
                   f'phigh={round(pool2.calculate_phigh(), 4)}, plow={pool2.calculate_plow()}\n'
                   f'Formula: y = {pool2.A ** 2 * pool2.y0} / (({pool2.A} - 1) * x + {pool2.x0}) - ({pool2.y0} * ({pool2.A} - 1))')



    ax1.plot(x_range, y_range_pool1, label=label_pool1, color='blue')
    ax1.plot(x_range, y_range_pool2, label=label_pool2, color='green')

    # Adjusting initial conditions for Pool 1
    initial_TKNX_balance_pool1 = pool1.x0
    initial_TKNY_balance_pool1 = pool1.y0
    new_TKNX_balance_pool1 = initial_TKNX_balance_pool1 + delta_x
    new_TKNY_balance_pool1 = pool1.calculate_y(new_TKNX_balance_pool1)

    # Marginal rates for Pool 1
    initial_marginal_rate_pool1 = pool1.calculate_marginal_rate(initial_TKNX_balance_pool1, initial_TKNY_balance_pool1)
    final_marginal_rate_pool1 = pool1.calculate_marginal_rate(new_TKNX_balance_pool1, new_TKNY_balance_pool1)

    # Adjusting initial conditions for Pool 2
    initial_TKNX_balance_pool2 = pool2.x0
    initial_TKNY_balance_pool2 = pool2.y0
    
    # Print phigh and plow 
    print(f"Pool 1 phigh: {pool1.calculate_phigh()}, plow: {pool1.calculate_plow()}")
    print(f"Pool 2 phigh: {pool2.calculate_phigh()}, plow: {pool2.calculate_plow()}")

    # Print initial balances
    print(f"Initial balance Pool 1: ({initial_TKNX_balance_pool1}, {initial_TKNY_balance_pool1})")
    print(f"Initial balance Pool 2: ({initial_TKNX_balance_pool2}, {initial_TKNY_balance_pool2})")


    ax1.set_xlabel('Token X Balance')
    ax1.set_ylabel('Token Y Balance')
    ax1.set_title('Bonding Curves')
    ax1.legend()
    ax1.grid(True)

    # axis limits
    plt.xlim(0, 200)
    plt.ylim(0, 1000)

   
    plt.tight_layout()
    plt.show()

def main():
    A1, A2, x0_1, y0_1, x0_2, y0_2 = set_balances_and_A()

    # Ensuring P_low1 = P_high2
    assert np.isclose(LiquidityPool(x0_1, y0_1, A1).calculate_plow(), LiquidityPool(x0_2, y0_2, A2).calculate_phigh()), f"P_low1 ({LiquidityPool(x0_1, y0_1, A1).calculate_plow()}) does not equal P_high2 ({LiquidityPool(x0_2, y0_2, A2).calculate_phigh()})"

    # Create Pool 1
    pool1 = LiquidityPool(x0_1, y0_1, A1)

    # Create Pool 2
    pool2 = LiquidityPool(x0_2, y0_2, A2)

    # Change in Token X (swap scenario)
    delta_TKNX = 30

    # Plot the bonding curves
    plot_bonding_curves(pool1, pool2, delta_TKNX)

if __name__ == "__main__":
    main()
