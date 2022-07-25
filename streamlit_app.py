from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
from forex_python.converter import CurrencyRates
from sigfig import round





"""
# SUNiCE Brew Converter
"""

curr = st.selectbox('Choose Currency:', ['USD', 'EUR','GBP'])
st.text('\n\n')
unit_type = st.selectbox('Choose units product price is quoted in:', ['Barrels','Liters'])
st.text('\n\n')
vol_type = st.selectbox('Choose units quantity being purchased is quoted in:',['Barrels','Liters'])
st.text('\n\n')
unit_price = float(st.text_input('Enter quoted price per unit'))
st.text('\n\n')
num = float(st.text_input('Enter quantity being purchased'))



# with st.echo(code_location='below'):
#     #total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
#     #num_turns = st.slider("Number of turns in spiral", 1, 100, 9)
#     curr = st.selectbox('Choose Currency', ['USD', 'EUR','GBP'])
#
#
#     Point = namedtuple('Point', 'x y')
#     data = []
#
#     points_per_turn = total_points / num_turns
#
#     for curr_point_num in range(total_points):
#         curr_turn, i = divmod(curr_point_num, points_per_turn)
#         angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
#         radius = curr_point_num / total_points
#         x = radius * math.cos(angle)
#         y = radius * math.sin(angle)
#         data.append(Point(x, y))
#
#     st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
#         .mark_circle(color='#0068c9', opacity=0.5)
#         .encode(x='x:Q', y='y:Q'))


    #curr = int(input())

    # print('Enter pricing unit: 1 for barrels, 2 for liters')
    # unit_type = float(input())
    #
    # print('Enter volume unit: 1 for barrels, 2 for liters')
    # vol_type = float(input())
    #
    # print('Enter unit price')
    # unit_price = float(input())
    #
    # print('Enter quantity')
    # num = float(input())
    #
if unit_type == 'Barrels':
    if vol_type == 'Barrels':
        price = unit_price * num
        quantity = num * 117.348
    elif vol_type == 'Liters':
        price = unit_price * (num / 117.348)
        quantity = num

elif unit_type == 'Liters':
    if vol_type == 'Barrels':
        price = unit_price * num
        quantity = num * 117.348
    elif vol_type == 'Liters':
        price = unit_price * num
        quantity = num
else:
    pass


weaker_abv = 0


# if vol_type == 'Barrels':
#     quantity = quantity * 117.348
# elif vol_type == 'Liters':
#     quantity = quantity * 3.78541
# else:
#     pass
#
# if uni == 'Barrels':
#     unit = 'Beer Barrels'
# elif unit == 'Liters':
#     unit = 'Gallons'
# else:
#     unit = 'Liters'


stronger_abv = float(st.text_input('Enter brew ABV'))

weaker_abv = 0

required_abv_abv = float(st.text_input('Enter target ABV'))


weaker_req = stronger_abv - required_abv_abv
stronger_req = required_abv_abv - weaker_abv

required_stronger = round((stronger_req / (stronger_req + weaker_req)), sigfigs=4)
required_weaker = round((weaker_req / (stronger_req + weaker_req)), sigfigs=4)
percent_total_volume = round(quantity / required_stronger, sigfigs=3)
weaker_total_volume = percent_total_volume * required_weaker
total_oz = percent_total_volume * 33.814
cases = total_oz / 240

if curr == 'USD':
    price = round(unit_price * num, sigfigs = 8)
    curr_unit = 'USD'
elif curr == 'EUR':
    c = CurrencyRates()
    rate = float(c.get_rate('EUR', 'USD'))
    price = round(unit_price * rate * num * 1.01, sigfigs=8)
    curr_unit = 'EUR'
elif curr == 'GBP':
    c = CurrencyRates()
    rate = float(c.get_rate('GBP', 'USD'))
    price = round(unit_price * num * rate * 1.01, sigfigs=8)
    curr_unit = 'GBP'

st.text('\n\n')
st.markdown("""---""")

st.write(num)
st.write(unit_price)
st.write(f'You will need to add {round(weaker_total_volume, sigfigs=4)} liters of water to the {quantity} liters of brew.\n')
st.write(f'Total volume is {percent_total_volume} liters| {round(total_oz, sigfigs=4)} fluid ounces\n')
st.write(f'The batch will produce a total of {round(cases, sigfigs=6)} cases\n')
if curr != 'USD':
    st.write(f'The total cost for this order is ${price} at the current {curr_unit}/USD exchange rate of {rate} including'
        ' an assumed transaction fee of 1%.')
else:
    st.write(f'The total cost for this order is ${price}')


