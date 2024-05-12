# # Imports
import matplotlib.pyplot as plt
import numpy as np


# initial token balances
initial_TKNX_balance = 10
initial_TKNY_balance = 20

# Bob's token swap scenario
delta_TKNX = 10
delta_TKNY = ((initial_TKNX_balance * initial_TKNY_balance) / (initial_TKNX_balance + delta_TKNX)) - initial_TKNY_balance

# Calculate the new Token X and Token Y balances after the swap
new_TKNX_balance = initial_TKNX_balance + delta_TKNX
new_TKNY_balance = initial_TKNY_balance + delta_TKNY

# Calculate the initial and final invariants
initial_invariant = initial_TKNX_balance * initial_TKNY_balance
final_invariant = new_TKNX_balance * new_TKNY_balance

# range of token balances for plotting
x_range = np.linspace(0, 200, 100)
y_range = initial_invariant / x_range


# Plot the bonding curve with the token swap scenario
plt.figure(figsize=(8, 6))
plt.plot(x_range, y_range, label='Bonding Curve', color='blue')
plt.scatter(initial_TKNX_balance, initial_TKNY_balance, color='red', label='Initial Point (x0, y0)')
plt.scatter(new_TKNX_balance, new_TKNY_balance, color='green', label='Final Point (x1, y1)')
plt.arrow(initial_TKNX_balance, initial_TKNY_balance, delta_TKNX, 0, color='black', linestyle='--', linewidth=1, head_width=2, head_length=2, label='Delta X')
plt.arrow(initial_TKNX_balance + delta_TKNX, initial_TKNY_balance, 0, delta_TKNY, color='black', linestyle='--', linewidth=1, head_width=2, head_length=2, label='Delta Y')
plt.xlabel('Token X Balance')
plt.ylabel('Token Y Balance')
plt.title('Bonding Curve Visualization with Token Swap')
plt.legend()
plt.grid(True)
plt.show()