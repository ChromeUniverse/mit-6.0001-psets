# inputs
annual_salary = float(input('Enter your starting annual salary: '))

# constants
total_cost = 1000000
semi_annual_raise = .07
portion_down_payment = 0.25
r = 0.04

# calculates how much can be saved in 36 months with the provided savings rate


def testSavingsRate(rate):

    current_savings = 0
    num_months = 0

    for j in range(36):
        # monthly salary with semi-annual adjustment
        monthly_salary = (annual_salary / 12) * \
            ((1 + semi_annual_raise) ** (num_months // 6))
        monthly_salary_saved = monthly_salary * (rate)
        monthly_savings_return = current_savings * r / 12

        # update savings
        total_monthly_deposit = monthly_salary_saved + monthly_savings_return
        current_savings += total_monthly_deposit

        num_months += 1

    return current_savings


start = 1
end = 10000
iterations = 0

while True:
    midpoint = (start + end) // 2
    rate = midpoint/10000
    savings = testSavingsRate(rate)
    delta = abs(savings - (total_cost * portion_down_payment))

    if (savings < (total_cost * portion_down_payment - 100)):
        start = midpoint

    if (savings > (total_cost * portion_down_payment + 100)):
        end = midpoint

    iterations += 1

    # exit condition
    if (delta <= 100):
        print(
            f'Best savings rate: {rate} \nSteps in bisection search: {iterations}')
        break

    # ran all test cases
    if (abs(start - end) <= 1):
        print("It is not possible to pay the down payment in three years.")
        break
