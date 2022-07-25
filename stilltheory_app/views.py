import base64
from dataclasses import dataclass
from fileinput import close
import hashlib
from logging import log
import random
from aiohttp import web

import string
from asgiref.sync import sync_to_async

from urllib.parse import urlencode
from aiohttp import ClientSession, request
import aiohttp
from django.shortcuts import redirect, render
from django.urls import reverse


from django.contrib.auth import get_user_model

from .form import *
import psycopg2

from .get_games import *


conn = psycopg2.connect(
        user="postgres",
        host="127.0.0.1",
        port="5432",
        database="stilltheory_database",
        password="tahboub989" 
    )

def index(request):
    return render(request, 'stilltheory_app/homepage.html', {})

async def get_token(request):
    code_verifier = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(43, 128)))
    code_verifier = base64.urlsafe_b64encode(code_verifier.encode('utf-8'))
    code_verifier = code_verifier.decode('utf-8')
    code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8').replace('=', '')
    # code_verifier = code_verifier.encode('utf-8')
    # code = aiohttp.request.rel_url.query.get("code")


    authorize_url = (
    'https://lichess.org/oauth'
    + "/?"
    + urlencode(
        {
            "state": 'zwDR8BuZRckY0W0aVRgeZmZ7IV8FSO2u1zLIL5Yc5u72dTQOM5Nivlgiezk9fW0bxh8xKY47RmzRt9nsMLucObzS5TmHWO86EB6frBsm4qTlhRsO6dNSOTGwYeTKs2yU',
            "client_id": '9Q1aqLsGmmRGJDWdUEgYocJwiZ7yfNO4YN8PR4er',
            "response_type": "code",
            "redirect_uri": 'http://127.0.0.1:8000/login/' ,
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
        }
    )
    )
    return redirect(authorize_url)



async def login(request, code, state):
    #  is our tokenk lip_Al3w9AX8TW8puxBnPmE1
    # url = 'https://lichess.org/api/account'
    code = request.path
    # print('hello'+code)
    data = {
            "grant_type": "authorization_code",
            "code": code,
            # "code_verifier": code_verifier,
            "client_id": '9Q1aqLsGmmRGJDWdUEgYocJwiZ7yfNO4YN8PR4er',
            # "redirect_uri": 'http://127.0.0.1:8000/login', 
            # TODO: add params
        }   
                        
    async with aiohttp.ClientSession() as client_session:
        async with client_session.post('https://lichess.org/api/token', json=data) as resp:
            data = await resp.json()
            # print(data)
            token = data.get("access_token")
            if token is not None:
                # TODO: "expires_in": 5270400
                return redirect("login/%s/%s/%s" % ('code_verifier', token))
            else:
                return redirect("index")

# helper method to avoid making coroutine:
def make_user(usr, fname, lname, closed, tosVio):
    User = get_user_model().objects.create_user(username = usr)  
    User.save()

async def finish_login(request, token):
    username = None
    title = ""
    closed = ""
    tosViolation = ""

# lip_Al3w9AX8TW8puxBnPmE1
    async with aiohttp.ClientSession() as client_session:
        data = {"Authorization": "Bearer %s" % token}
        async with client_session.get('https://lichess.org/api/account', headers=data) as resp:
            data = await resp.json()
            username = data.get("username")
            title = data.get("title", "")
            closed = data.get("closed", "")
            tosViolation = data.get("tosViolation", "")
            first_name = data.get("firstName", "")
            last_name = data.get("lastName", "")
    # print(username)
    # print(title)
    # print(closed)
    # print(tosViolation)
    
    sync_to_async(make_user)(username, first_name, last_name, closed, tosViolation, title)
    # user.username = username
    # user.first_name = first_name
    # user.last_name = last_name
    # sync_to_async(user.save)()

            
    return redirect('index')
def username_testpage(request):
    username = ''
    if request.method == "POST":
        form = UsernameForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']

            # add to database - for debugging only
            # step 1: check if is already user
            user_cursor = conn.cursor()
            user_cursor.execute(
                """
                SELECT id
                FROM public."user"
                WHERE username = '%s'
                """ % (username,)
            )
            conn.rollback()
            usr_id = 0
            # if we got a user, use it, else add it
           
            if user_cursor.rowcount == 0:
                user_cursor.execute(
                """
                INSERT INTO public."user"(username)
                VALUES('%s')
                """ % (username,)
                )
                conn.commit()
                get_user_cursor = conn.cursor()
                get_user_cursor.execute(
                """
                SELECT id
                FROM public."user"
                WHERE username = '%s'
                """ % (username,)
                )
                usr_id = get_user_cursor.fetchone()[0]
            else:
                usr_id = user_cursor.fetchone()[0]
            return dashboard(request, username, usr_id)
    

    return render(request, 'stilltheory_app/username.html', {})


def dashboard(request, username, usr_id, color):
    # get
    prepare_database(username, usr_id)
    
    cursor = conn.cursor()
    # using 0 in next line just as placeholder. should use request.USER in future
    if color == 'white':
        cursor.execute("""
        WITH RECURSIVE opening_tree_visual AS (
            SELECT id, parent_id, position, opening_variation, num_wins, num_losses, num_draws, fen_position,
                    to_char(id,'9999') AS path
            FROM opening_tree
            WHERE parent_id IS NULL AND user_id = '%s' AND color = 'white'

            UNION ALL

            SELECT o.id, o.parent_id, o.position, o.opening_variation, o.num_wins, o.num_losses, o.num_draws, o.fen_position,
                    opening_tree_visual.path || '->' || to_char(o.id,'9999')
            FROM opening_tree o, opening_tree_visual
            WHERE o.parent_id = opening_tree_visual.id AND user_id = '%s'
            )
            SELECT *
            FROM opening_tree_visual
            order by path;
        """ % (usr_id, usr_id,))
        conn.commit()
    else:
        cursor.execute("""
        WITH RECURSIVE opening_tree_visual AS (
            SELECT id, parent_id, position, opening_variation, num_wins, num_losses, num_draws, fen_position,
                    to_char(id,'9999') AS path
            FROM opening_tree
            WHERE parent_id IS NULL AND user_id = '%s' AND color = 'black'

            UNION ALL

            SELECT o.id, o.parent_id, o.position, o.opening_variation, o.num_wins, o.num_losses, o.num_draws, o.fen_position,
                    opening_tree_visual.path || '->' || to_char(o.id,'9999')
            FROM opening_tree o, opening_tree_visual
            WHERE o.parent_id = opening_tree_visual.id AND user_id = '%s'
            )
            SELECT *
            FROM opening_tree_visual
            order by path;
        """ % (usr_id, usr_id,))
        conn.commit()

    
    data = """"""
    # IMP: the following code uses a rather sophisticated system for ultimately sending a JSON to the template.
    # TODO: consider adding draws to total
    data_dump = cursor.fetchall()
    if data_dump[1][1] == data_dump[0][0]:
        data += data_dump[0][3] + '(((' + str(data_dump[0][4] / (data_dump[0][5] + data_dump[0][4] + data_dump[0][6])) + ')))' + '((((' + data_dump[0][7] + '))))' + '(((((' + str(int(data_dump[0][4] + data_dump[0][5] + data_dump[0][6])) + ')))))' + '\n' + data_dump[0][3] + '(((' + str(data_dump[0][4] / (data_dump[0][5] + data_dump[0][4] + data_dump[0][6])) + ')))' + '((((' + data_dump[0][7] + '))))' + '(((((' + str(int(data_dump[0][4] + data_dump[0][5] + data_dump[0][6])) + ')))))' + '   '
    else:
        data += data_dump[0][3] + '(((' + str(data_dump[0][4] / (data_dump[0][5] + data_dump[0][4] + data_dump[0][6])) + ')))' + '((((' + data_dump[0][7] + '))))' + '(((((' + str(int(data_dump[0][4] + data_dump[0][5] + data_dump[0][6])) + ')))))' + '\n' + data_dump[0][3] + '(((' + str(data_dump[0][4] / (data_dump[0][5] + data_dump[0][4] + data_dump[0][6])) + ')))' + '((((' + data_dump[0][7] + '))))' + '(((((' + str(int(data_dump[0][4] + data_dump[0][5] + data_dump[0][6])) + ')))))'
    for i in range(1, len(data_dump)):
        if data_dump[i][1] is None and i < len(data_dump) - 1 and data_dump[i + 1][1] == data_dump[i][0]:
            data += '\n' + data_dump[i][3] + '(((' + str(data_dump[i][4] / (data_dump[i][5] + data_dump[i][4] + data_dump[i][6])) + ')))' + '((((' + data_dump[i][7] + '))))' + '(((((' + str(int(data_dump[i][4] + data_dump[i][5] + data_dump[i][6])) + ')))))' + '   '
        elif data_dump[i][1] is None:
            data += '\n' + data_dump[i][3] + '(((' + str(data_dump[i][4] / (data_dump[i][5] + data_dump[i][4] + data_dump[i][6])) + ')))' + '((((' + data_dump[i][7] + '))))' + '(((((' + str(int(data_dump[i][4] + data_dump[i][5] + data_dump[i][6])) + ')))))'
        elif data_dump[i][1] == data_dump[i - 1][0] and data_dump[i - 1][1] is None:
            data += data_dump[i][3] + '(((' + str(data_dump[i][4] / (data_dump[i][5] + data_dump[i][4] + data_dump[i][6])) + ')))' + '((((' + data_dump[i][7] + '))))' + '(((((' + str(int(data_dump[i][4] + data_dump[i][5] + data_dump[i][6])) + ')))))'
        elif data_dump[i][1] == data_dump[i - 1][0]:
            data += '   ' + data_dump[i][3] + '(((' + str(data_dump[i][4] / (data_dump[i][5] + data_dump[i][4] + data_dump[i][6])) + ')))' + '((((' + data_dump[i][7] + '))))' + '(((((' + str(int(data_dump[i][4] + data_dump[i][5] + data_dump[i][6])) + ')))))'
        else:
            data += '\n'
            # for j in range(find_null(data_dump, find_elem(data_dump, data_dump[i][1])), find_elem(data_dump, data_dump[i][1]) + 1):
            #     if j == find_null(data_dump, find_elem(data_dump, data_dump[i][1])):
            #         data += data_dump[j][3]
            #     else:
            #         data += '   ' + data_dump[j][3]
            x = i   
            to_be_reversed = []
            while(data_dump[x][1] is not None):
                x = find_elem(data_dump, data_dump[x][1])
                # data += data_dump[x][3]
                to_be_reversed.append(data_dump[x][3] + '(((' + str(data_dump[x][4] / (data_dump[x][5] + data_dump[x][4] + data_dump[x][6])) + ')))' + '((((' + data_dump[x][7] + '))))' + '(((((' + str(int(data_dump[x][4] + data_dump[x][5] + data_dump[x][6])) + ')))))')
                
            to_be_reversed.reverse()
            for c in range(0, len(to_be_reversed)): 
                if c == 0:
                    data += to_be_reversed[c]
                else:
                    data += '   ' + to_be_reversed[c]
            data += '   ' + data_dump[i][3] + '(((' + str(data_dump[i][4] / (data_dump[i][5] + data_dump[i][4] + data_dump[i][6])) + ')))' + '((((' + data_dump[i][7] + '))))' + '(((((' + str(int(data_dump[i][4] + data_dump[i][5] + data_dump[i][6])) + ')))))'
    data = data.replace('\n\n', '\n')
    # print(data)
    tree = {}
    for line in data.split("\n"):
        node = tree
        for n in line.split('   '):
            node.setdefault(n, {})
            node = node[n]
    
    list_to_js = node_to_js(tree)

    str_list = str(list_to_js)
    str_list = ('[{"name": "Repertoire", "parent": null, "color": "orange", "children": ') + (str_list) + ('}];')
    if color == 'white':
        return render(request, 'stilltheory_app/dashboard_white.html', {'str': str_list})
    else:
        return render(request, 'stilltheory_app/dashboard_black.html', {'str': str_list})


def find_elem(arr, x):
    for i in range(0, len(arr)):
        if arr[i][0] == x:
            return i

# def find_null(arr, x):
#     for i in range(x, -1, -1):
#         if arr[i][1] == None:
#             return i

def node_to_js(tree, parent=4):

    return [{

            "name": name[0:name.index('(((')],
            "color": '#'+('%02x%02x%02x' % (int(255.0 * (1 - (float(name[name.index('(((')+3:name.index(')))')])))), 0, int(255.0 * float(name[name.index('(((')+3:name.index(')))')])))),
            "parent": parent,
            "position": name[name.index('((((')+4:name.index('))))')],
            "winrate": str(int(float(name[name.index('(((')+3:name.index(')))')]) * 100)) + '%',
            "numgames": str(name[name.index('(((((')+5:name.index(')))))')]),
            "children": node_to_js(node, name)
        }
        for name, node in tree.items()
    ]
# 