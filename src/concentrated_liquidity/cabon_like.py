import numpy as np
import matplotlib.pyplot as plt

class CarbonDeFiCurve:
    def __init__(self, P_high, P_low, y_int, token_name):
        self.P_high = P_high
        self.P_low = P_low
        self.y_int = y_int
        self.a = np.sqrt(P_high - P_low)
        self.b = np.sqrt(P_low)
        self.z = y_int
        self.token_name = token_name
    
    def calculate_y(self, x):
        """Calculate the token balance y given the parameter x."""
        return self.z * (self.z - x * self.b * (self.a + self.b)) / (self.z + x * self.a * (self.a + self.b))
    
    def plot_curve(self, x_range, ax):
        """Plot the DeFi curve for the given range of x values."""
        x_values = np.linspace(*x_range, 400)
        y_values = self.calculate_y(x_values)
        
        ax.plot(x_values, y_values, label=f'{self.token_name} Curve ({self.token_name} balance vs x)')
        
        ax.set_xlabel('x (NOT A TOKEN BALANCE)')
        ax.set_ylabel('y (Token Balance)')
        ax.legend()
        ax.grid(True)
        ax.set_title(f'Carbon DeFi Curve for {self.token_name}')
    
    def delta_y(self, delta_x, x):
        numerator = delta_x * self.z**2 * (self.a + self.b)**2
        denominator = x * self.a * (self.a + self.b) + self.z * ((x + delta_x) * self.a * (self.a + self.b) + self.z)
        return -(numerator / denominator)


    def effective_price(self, delta_x, x):
        """Calculate the effective price given a change in parameter x."""
        return self.delta_y(delta_x, x) / delta_x
    
    def marginal_price(self, y):
        """Calculate the marginal price given the token balance y."""
        return -(self.a * (y / self.z) + self.b) ** 2
    
    def delta_x(self, delta_y, y):
        """Calculate the change in parameter x given a change in token balance y."""
        return -(delta_y * self.z**2) / ((self.a * y + self.b * self.z) * (self.a * (y + delta_y) + self.b * self.z))

    def calculate_x_0(self):
        """Calculate the initial x value."""
        return  (self.z / (self.a * np.sqrt(self.b) * np.sqrt(self.a + self.b))) * ((np.sqrt(self.b) * np.sqrt(self.a + self.b) - self.b) / np.sqrt(self.b) * np.sqrt(self.a + self.b))
    
    def calculate_y_0(self):
        """Calculate the initial y value."""
        return ((self.z * np.sqrt(self.b) * np.sqrt(self.a + self.b)) / self.a) * ((np.sqrt(self.b) * np.sqrt(self.a + self.b) - self.b) / np.sqrt(self.b) * np.sqrt(self.a + self.b))



# parameters for both curves
P_high_rice = 5
P_low_rice = 1
y_int_rice = 300

P_high_yam = 6
P_low_yam = 2
y_int_yam = 100

# curves
rice_curve = CarbonDeFiCurve(P_high_rice, P_low_rice, y_int_rice, 'RICE')
yam_curve = CarbonDeFiCurve(P_high_yam, P_low_yam, y_int_yam, 'YAM')

# x_range for plotting
x_range = (0, 20)

# subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))


rice_curve.plot_curve(x_range, ax1)
yam_curve.plot_curve(x_range, ax2)



# Simulation of RICE to YAM conversion
delta_y_rice = 20
x_rice_initial = 10  # Chosen arbitrary value for the initial x-value for RICE curve
y_rice_initial = rice_curve.calculate_y(x_rice_initial)
y_rice_final = y_rice_initial + delta_y_rice
marginal_price_rice = rice_curve.marginal_price(y_rice_initial)


x_yam_initial = x_rice_initial  # Assume initial x for YAM is same as RICE

# Calculate the corresponding delta_x for YAM
delta_x_rice = rice_curve.delta_x(delta_y_rice, y_rice_initial)
effective_price_rice = rice_curve.effective_price(delta_y_rice, delta_x_rice)


y_yam_initial = yam_curve.calculate_y(x_yam_initial)


# Useing 
delta_y_yam = delta_y_rice / effective_price_rice

delta_x_yam = yam_curve.delta_x(delta_y_yam, yam_curve.calculate_y(x_yam_initial))
# Calculate the effective price and marginal price for YAM
effective_price_yam = yam_curve.effective_price(delta_y_yam, delta_x_yam)
marginal_price_yam = yam_curve.marginal_price(y_yam_initial)


# Update the initial YAM balance
y_yam_final = y_yam_initial + delta_y_yam



# Calculate y_values for both curves
x_values = np.linspace(*x_range, 400)
y_values_rice = rice_curve.calculate_y(x_values)
y_values_yam = yam_curve.calculate_y(x_values)


ax1.plot(x_values, y_values_rice, 
         label=f'{rice_curve.token_name} Curve:\n'
               f'$y = \\frac{{z(z - x \\cdot b \\cdot (a + b))}}{{z + x \\cdot a \\cdot (a + b)}}$\n'
               f'P_high: {rice_curve.P_high}, P_low: {rice_curve.P_low}, a: {rice_curve.a:.2f}, b: {rice_curve.b:.2f}, z: {rice_curve.z:.2f}\n'
               f'Effective Price: {effective_price_rice:.2f}, Marginal Price: {marginal_price_rice:.2f}',
         color='red')

ax2.plot(x_values, y_values_yam, 
         label=f'{yam_curve.token_name} Curve:\n'
               f'$y = \\frac{{z(z - x \\cdot b \\cdot (a + b))}}{{z + x \\cdot a \\cdot (a + b)}}$\n'
               f'P_high: {yam_curve.P_high}, P_low: {yam_curve.P_low}, a: {yam_curve.a:.2f}, b: {yam_curve.b:.2f}, z: {yam_curve.z:.2f}\n'
               f'Effective Price: {effective_price_yam:.2f}, Marginal Price: {marginal_price_yam:.2f}',
         color='blue')



ax1.scatter([x_rice_initial], [y_rice_initial], color='red', zorder=5, label=f'{rice_curve.token_name} Initial ({x_rice_initial:.2f}, {y_rice_initial:.2f})', marker='o')
ax1.scatter([x_rice_initial + delta_x_rice], [y_rice_final], color='green', zorder=5, label=f'{rice_curve.token_name} Final ({x_rice_initial + delta_x_rice:.2f}, {y_rice_final:.2f})', marker='o')

ax1.annotate('', xy=(x_rice_initial + delta_x_rice, y_rice_final), xytext=(x_rice_initial, y_rice_initial), arrowprops=dict(facecolor='red', arrowstyle='-|>'))



ax2.scatter([x_yam_initial], [y_yam_initial], color='blue', zorder=5, label=f'{yam_curve.token_name} Initial ({x_yam_initial:.2f}, {y_yam_initial:.2f})', marker='o')
ax2.scatter([x_yam_initial + delta_x_yam], [y_yam_final], color='green', zorder=5, label=f'{yam_curve.token_name} Final ({x_yam_initial + delta_x_yam:.2f}, {y_yam_final:.2f})', marker='o')

ax2.annotate('', xy=(x_yam_initial + delta_x_yam, y_yam_final), xytext=(x_yam_initial, y_yam_initial), arrowprops=dict(facecolor='blue', arrowstyle='-|>'))


ax1.legend(loc='upper right')
ax2.legend(loc='upper right')

plt.tight_layout()

# Print the results
print(f'Delta_x for YAM: {delta_x_yam}')
print(f'Delta_x for RICE: {delta_x_rice:.2f}')
print(f'RICE Initial y: {y_rice_initial:.2f}')
print(f'YAM Initial y: {y_yam_initial:.2f}')
print(f'YAM Final y: {y_yam_final:.2f}')
print(f'RICE Delta y: {delta_y_rice:.2f}')
print(f'RICE Final y: {y_rice_final:.2f}')
print(f'RICE Effective Price: {effective_price_rice:.2f}')
print(f'RICE Marginal Price: {marginal_price_rice:.2f}')
print(f'YAM Initial x: {x_yam_initial:.2f}')
print(f'YAM Delta y: {delta_y_yam:.2f}')
print(f'YAM Effective Price: {effective_price_yam:.2f}')
print(f'YAM Marginal Price: {marginal_price_yam:.2f}')

plt.show()