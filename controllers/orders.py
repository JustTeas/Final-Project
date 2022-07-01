from flask import Flask, render_template, request, redirect, session, flash
from models.order import Order
from models.user import User
from __init__ import app
from werkzeug.datastructures import ImmutableMultiDict
from datetime import *
import random

import socket

methods_JSON=[{'method': 'Carry Out','price':0}, {'method': 'Delivery','price':10}]
size_JSON=[{'size': 'Small','price':10}, {'size': 'Medium','price':15}, {'size': 'Large','price':20}, {'size': 'X-Large','price':25}]
bowl_JSON=[{'bowl': 'Thin Bowl','price':0}, {'bowl': 'Hand Tossed','price':5}, {'bowl': 'Stuffed bowl','price':10}]
quantity_JSON=[{'qty': 1}, {'qty': 2}, {'qty': 3}, {'qty': 4}, {'qty': 5}]
toppings_JSON = [{'topping':'Pepperoni','price':1},{'topping':'Olives','price':1},{'topping':'Bacon','price':1},{'topping':'Peppers','price':1},{'topping':'Pineapple','price':1},{'topping':'Spinach','price':1},]

@app.route('/user/new_order')
def new_order():
    data = {
        'id':session['id']
    }
    user=User.get_by_id(data)
    return render_template("/user/craft_a_burrito.html", user=user,all_methods= methods_JSON, all_sizes=size_JSON, all_bowl=bowl_JSON, all_quantities=quantity_JSON,all_toppings=toppings_JSON)

@app.route('/user/favorite_order')
def crafted_fav_burrito():
    data = {
        'id' : session['id']
    }
    user=User.get_by_id(data)
    return render_template("/user/crafted_fav_burrito.html", user=user)


@app.route('/user/random_order')
def start_craft_a_burrito():
    random_burrito = {
        'method' : random.choice(methods_JSON),
        'size' : random.choice(size_JSON),
        'bowl' : random.choice(bowl_JSON),
        'quantity' : random.choice(quantity_JSON),
        'toppings' : random.choice(toppings_JSON)
        }
    data = {
        'id' : session['id']
    }
    print(random_burrito)
    user=User.get_by_id(data)
    return render_template("/user/crafted_burrito.html", user=user, all_methods= methods_JSON, all_sizes=size_JSON, all_bowl=bowl_JSON, all_quantities=quantity_JSON, all_toppings=toppings_JSON, random_burrito=random_burrito)

@app.route('/user/send_order',methods=['POST'])
def send_order_details():
    
    session_data = request.form
    toppings_list = []
    for v in session_data.values():
        for t in toppings_JSON:
            if v == t['topping']:
                toppings_list.append(v)
    data = {
        'method':request.form['method'],
        'size':request.form['size'],
        'bowl':request.form['bowl'],
        'quantity':int(request.form['quantity']),
        'toppings': ", ".join(toppings_list),
        'number_of_toppings': len(toppings_list),
        'user_id': int(session['id'])
    }
    data['order_total'] = calcOrderTotal(data)
    print(data)
    session['user_session_orders'] = [data] + session['user_session_orders']
    
    session['user_session_grand_total'] = calcGrandTotal(session['user_session_orders'])
    
    #print("Now Printing the session data: ",session['user_session_orders'])
    
    return redirect("/user/order")

def calcOrderTotal(info):
    num_sum = 0
    
    for m in methods_JSON:
        print(m['method'], m['price'])
        if info['method'] == m['method']:
            num_sum += m['price']
            
    for s in size_JSON:
        print(s['size'], s['price'])
        if info['size'] == s['size']:
            num_sum += s['price']
            
    for c in bowl_JSON:
        print(c['bowl'], c['price'])
        if info['bowl'] == c['bowl']:
            num_sum += c['price']

    num_sum += info['number_of_toppings'] * 1
    
    num_sum = (num_sum * int(info['quantity']))
    return num_sum

def calcGrandTotal(info):
    num_sum = 0
    for i in info:
        #print(i['order_total'])
        num_sum += int(i['order_total'])
    return num_sum

@app.route('/user/cancel_order')
def remove_orders():
    session['user_session_orders'] = []
    session['user_session_grand_total'] = 0
    return redirect("/user/quick_options")

@app.route('/user/submit_order',methods=['GET'])
def post_orders():
    for ord in session['user_session_orders']:
        print(ord)
        data = {
            'method': ord['method'],
            'size': ord['size'],
            'bowl': ord['bowl'],
            'quantity': ord['quantity'],
            'toppings': ord['toppings'],
            'number_of_toppings': ord['number_of_toppings'],
            'user_id': session['id']
            }
        Order.save_order(data)
        
    session['user_session_orders'] = []
    session['user_session_grand_total'] = 0
        
    return redirect ("/user/quick_options")

def validate_order ( order ):
    is_valid = True

    if len(order['method']) < 1 or order['method'].isspace():
        flash("Method is blank","order")
        is_valid = False
            
    if len(order['size']) < 1 or order['size'].isspace():
        flash("Size is blank","order")
        is_valid = False

    if len(order['bowl']) < 1 or order['bowl'].isspace():
        flash("Bowl is blank","order")
        is_valid = False
        
    if len(order['quantity']) < 1 or order['quantity'].isspace():
        flash("Quantity is less than 1","order")
        is_valid = False

    return is_valid