Problem Statement

The objective is to derive and prove the equivalence of the price P0​ of a pool token in a liquidity pool, given a bonding curve. We need to show that P0​ can be calculated using the following formula and prove its equivalence to other forms:
P0=x0⋅Phigh−y0y0/Plow−x0
P0​=y0​/Plow​−x0​x0​⋅Phigh​−y0​​

where:

    PhighPhigh​ is the maximum price of the pool token,
    PlowPlow​ is the minimum price of the pool token,
    (x0,y0)(x0​,y0​) is a point on the bonding curve,
    P0P0​ is the price of the pool token at that point.

We also need to show that P0P0​ is equivalent to:

    Phigh−PlowPhigh​−Plow​

    ​
    y0x0x0​y0​​
    yintxintxint​yint​​

where xintxint​ and yintyint​ represent the x and y intercepts of the bonding curve respectively.

The virtual curve helps in modeling, while the real curve applies to actual liquidity in the pool with intercepts bounding the price ranges. The derived formulas and equivalences are important for demonstrating the underlying principles of AMMs like Uniswap.

Key Concepts

    Bonding Curve: A curve representing the relationship between the reserve amounts of two tokens in a liquidity pool.
    Invariant Function: For Uniswap v3, the invariant function x⋅y=k is adjusted to handle concentrated liquidity, where the product of reserves is constant over a specific price range.
    Virtual, Actual, and Real Curves:
        Virtual Curve: A hypothetical curve used to model liquidity over a price range, not necessarily touching the axes.
        Actual Curve: The curve representing the real state of the pool’s reserves.
        Real Curve: When applying the virtual curve in practice, resulting in a curve that has specific intercepts.