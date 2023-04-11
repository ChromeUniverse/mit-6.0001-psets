# inputs
annual_salary = float(input('Enter your annual salary: '))
portion_saved = float(
    input('Enter the percent of your salary to save, as a decimal: '))
total_cost = float(input('Enter the cost of your dream home: '))

# constants
portion_down_payment = 0.25
r = 0.04

# savings state
current_savings = 0
num_months = 0

while True:
    monthly_salary_saved = annual_salary / 12 * portion_saved
    monthly_savings_return = current_savings * r / 12

    # update savings
    total_monthly_deposit = monthly_salary_saved + monthly_savings_return
    current_savings += total_monthly_deposit
    num_months += 1

    # exit condition
    if (current_savings > total_cost * portion_down_payment):
        break

print(f'Number of months: {num_months}')
