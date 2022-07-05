import base64
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

from stilltheory_app.views import node_to_js

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

def dashboard(request, username, usr_id):
    # get
    prepare_database(username, usr_id)
    
    cursor = conn.cursor()
    # using 0 in next line just as placeholder. should use request.USER in future
    cursor.execute("""
    WITH RECURSIVE opening_tree_visual AS (
        SELECT id, parent_id, position, opening_variation,
                to_char(id,'9999') AS path
        FROM opening_tree
        WHERE parent_id IS NULL AND user_id = '%s'

        UNION ALL

        SELECT o.id, o.parent_id, o.position, o.opening_variation,
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
    data_dump = cursor.fetchall()
    data += data_dump[0][2] + '\n' 
    for i in range(1, len(data_dump)):
        data += data_dump[i][2] + '\n'
    # data_l = data.split('\n')
    # convert moves into openings:
    # final_data = """"""
    # for line in data_l:
    #     line_l = line.split(' ')
    #     fff = ""
    #     for i in range(0, len(line_l)):
    #         final_line_l = line_l[0:i + 1]
    #         final_line = ' '.join(final_line_l)
    #         find_opening_cursor = conn.cursor()
    #         print(final_line)
    #         find_opening_cursor.execute(
    #             """
    #             SELECT opening_variation_name
    #             FROM opening_variation_look_up
    #             WHERE opening_variation_position = '%s'
    #             """ % (final_line,)
    #         )
    #         final_final = find_opening_cursor.fetchone()
    #         fff += final_final[0]
    #         if i < len(line_l) - 1:
    #             fff += '   '
    #         final_data += fff + '\n'
    # print(final_data)
    tree = {}
    for line in data.split("\n"):
        node = tree
        for n in line.split(' '):
            node.setdefault(n, {})
            node = node[n]
    
    list_to_js = node_to_js(tree)
    # str_to_js = ""
    # for x in list_to_js:
    #     str_to_js += x
    # print(str_to_js)
    str_list = str(list_to_js)
    
    # make user see opening names instead of positions
    for i in range(0, len(str_list) - 8):
        if (str_list[i] == 'n' and str_list[i + 1] == 'a' and str_list[i + 2] == 'm' and str_list[i + 3] == 'e'):
            startIndex = i + 8
            position = ''
            for j in range(startIndex, len(str_list)):
                if str_list[j] == '\'':
                    break
                position += str_list[j]
            # print(position)
            opening_name = ''
            find_opening_cursor = conn.cursor()
            find_opening_cursor.execute(
                """
                SELECT opening
                FROM moves  
                WHERE position = '%s'
                """ % (position,)
            )
            opening_name = find_opening_cursor.fetchone()
            # if opening_name == None:
                # print('hello' + position)
            # else: 
            # print(opening_name)
        # elif (str_list[i] == 'p' and str_list[i + 1] == 'a' and str_list[i + 2] == 'r' and str_list[i + 3] == 'e' and str_list[i + 5] == 'n' and str_list[i + 6] == 't'): 




    str_list = ('[{\'name\': \'Repertoire\', \'parent\': null, \'children\': ') + (str_list) + ('}];')
    # print(str_list)

    # return render(request, 'stilltheory_app/dashboard.html', {'str': str_list})   
    def node_to_js(tree, parent=4):
        return [{
                "name": name,
                "parent": parent,
                "children": node_to_js(node, name)
            }
            for name, node in tree.items()
        ]

        

# # import base64
# from dataclasses import dataclass
# from fileinput import close
# import hashlib
# from logging import log
# import random
# from aiohttp import web

# import string
# from asgiref.sync import sync_to_async

# from urllib.parse import urlencode
# from aiohttp import ClientSession, request
# import aiohttp
# from django.shortcuts import redirect, render
# from django.urls import reverse


# from django.contrib.auth import get_user_model

# from .form import *
# import psycopg2

# from .get_games import *


# conn = psycopg2.connect(
#         user="postgres",
#         host="127.0.0.1",
#         port="5432",
#         database="stilltheory_database",
#         password="tahboub989" 
#     )

# def index(request):
#     return render(request, 'stilltheory_app/homepage.html', {})

# async def get_token(request):
#     code_verifier = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(43, 128)))
#     code_verifier = base64.urlsafe_b64encode(code_verifier.encode('utf-8'))
#     code_verifier = code_verifier.decode('utf-8')
#     code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
#     code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8').replace('=', '')
#     # code = aiohttp.request.rel_url.query.get("code")


#     data = {
#             "grant_type": "authorization_code",
#             "code": 'jfsPz4j2olZpUn0MwZJE46yc8Yt2YB',
#             "code_verifier": code_verifier,
#             "client_id": '9Q1aqLsGmmRGJDWdUEgYocJwiZ7yfNO4YN8PR4er',
#             "redirect_uri": 'http://127.0.0.1:8000/login', 
#             # TODO: add params
#         }

#     async with aiohttp.ClientSession() as client_session:
#         async with client_session.post('https://lichess.org/api/token', json=data) as resp:
#             data = await resp.json()
#             # print(data)
#             token = data.get("access_token")
#             if token is not None:
#                 # TODO: "expires_in": 5270400
#                 return redirect("login/%s/%s/%s" % (code_verifier, code_challenge, token))
#             else:
#                 return redirect("index")

# def login(request, code_verifier, code_challenge, token):
    
#     #  is our tokenk lip_Al3w9AX8TW8puxBnPmE1
#     # url = 'https://lichess.org/api/account'
#     authorize_url = (
#             'https://lichess.org/oauth'
#             + "/?"
#             + urlencode(
#                 {
#                     "state": 'zwDR8BuZRckY0W0aVRgeZmZ7IV8FSO2u1zLIL5Yc5u72dTQOM5Nivlgiezk9fW0bxh8xKY47RmzRt9nsMLucObzS5TmHWO86EB6frBsm4qTlhRsO6dNSOTGwYeTKs2yU',
#                     "client_id": '9Q1aqLsGmmRGJDWdUEgYocJwiZ7yfNO4YN8PR4er',
#                     "response_type": "code",
#                     "redirect_uri": 'http://127.0.0.1:8000/finish_login/%s' % (token,),
#                     "code_challenge": code_challenge,
#                     "code_challenge_method": "S256",
#                 }
#             )
#         )
#     return redirect(authorize_url)

# # helper method to avoid making coroutine:
# def make_user(usr, fname, lname, closed, tosVio):
#     User = get_user_model().objects.create_user(username = usr)  
#     User.save()

# async def finish_login(request, token):
#     username = None
#     title = ""
#     closed = ""
#     tosViolation = ""

# # lip_Al3w9AX8TW8puxBnPmE1
#     async with aiohttp.ClientSession() as client_session:
#         data = {"Authorization": "Bearer %s" % token}
#         async with client_session.get('https://lichess.org/api/account', headers=data) as resp:
#             data = await resp.json()
#             username = data.get("username")
#             title = data.get("title", "")
#             closed = data.get("closed", "")
#             tosViolation = data.get("tosViolation", "")
#             first_name = data.get("firstName", "")
#             last_name = data.get("lastName", "")
#     # print(username)
#     # print(title)
#     # print(closed)
#     # print(tosViolation)
    
#     sync_to_async(make_user)(username, first_name, last_name, closed, tosViolation, title)
#     # user.username = username
#     # user.first_name = first_name
#     # user.last_name = last_name
#     # sync_to_async(user.save)()

            
#     return redirect('index')
# def username_testpage(request):
#     username = ''
#     if request.method == "POST":
#         form = UsernameForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']

#             # add to database - for debugging only
#             # step 1: check if is already user
#             user_cursor = conn.cursor()
#             user_cursor.execute(
#                 """
#                 SELECT id
#                 FROM public."user"
#                 WHERE username = '%s'
#                 """ % (username,)
#             )
#             conn.rollback()
#             usr_id = 0
#             # if we got a user, use it, else add it
           
#             if user_cursor.rowcount == 0:
#                 user_cursor.execute(
#                 """
#                 INSERT INTO public."user"(username)
#                 VALUES('%s')
#                 """ % (username,)
#                 )
#                 conn.commit()
#                 get_user_cursor = conn.cursor()
#                 get_user_cursor.execute(
#                 """
#                 SELECT id
#                 FROM public."user"
#                 WHERE username = '%s'
#                 """ % (username,)
#                 )
#                 usr_id = get_user_cursor.fetchone()[0]
#             else:
#                 usr_id = user_cursor.fetchone()[0]
#             return dashboard(request, username, usr_id)
    

#     return render(request, 'stilltheory_app/username.html', {})

# def dashboard(request, username, usr_id):
#     # get
#     prepare_database(username, usr_id)
    
#     cursor = conn.cursor()
#     # using 0 in next line just as placeholder. should use request.USER in future
#     cursor.execute("""
#     WITH RECURSIVE opening_tree_visual AS (
#         SELECT id, parent_id, position, opening_variation,
#                 to_char(id,'9999') AS path
#         FROM opening_tree
#         WHERE parent_id IS NULL AND user_id = '%s'

#         UNION ALL

#         SELECT o.id, o.parent_id, o.position, o.opening_variation,
#                 opening_tree_visual.path || '->' || to_char(o.id,'9999')
#         FROM opening_tree o, opening_tree_visual
#         WHERE o.parent_id = opening_tree_visual.id AND user_id = '%s'
#         )
#         SELECT *
#         FROM opening_tree_visual
#         order by path;
#     """ % (usr_id, usr_id,))
#     conn.commit()

    
#     data = """"""
#     data_dump = cursor.fetchall()
#     data += data_dump[0][3] + '\n' + data_dump[0][3] + '   '
#     for i in range(1, len(data_dump)):
#         if data_dump[i][1] is None:
#             data += '\n' + data_dump[i][3] + '\n'
#         elif data_dump[i][1] == data_dump[i - 1][0] and data_dump[i - 1][1] is None:
#             data += data_dump[i][3]
#         elif data_dump[i][1] == data_dump[i - 1][0]:
#             data += '   ' + data_dump[i][3]
#         else:
#             data += '\n'
#             for j in range(find_null(data_dump, find_elem(data_dump, data_dump[i][1])), find_elem(data_dump, data_dump[i][1]) + 1):
#                 if j == find_null(data_dump, find_elem(data_dump, data_dump[i][1])):
#                     data += data_dump[j][3]
#                 else:
#                     data += '   ' + data_dump[j][3]
#             data += '   ' + data_dump[i][3]
#     data = data.replace('\n\n', '\n')
#     print(data)
#     tree = {}
#     for line in data.split("\n"):
#         node = tree
#         for n in line.split('   '):
#             node.setdefault(n, {})
#             node = node[n]
    
#     list_to_js = node_to_js(tree)

#     str_list = str(list_to_js)
#     str_list = ('[{\'name\': \'Repertoire\', \'parent\': null, \'children\': ') + (str_list) + ('}];')

#     return render(request, 'stilltheory_app/dashboard.html', {'str': str_list})    


# def find_elem(arr, x):
#     for i in range(0, len(arr)):
#         if arr[i][0] == x:
#             return i

# def find_null(arr, x):
#     for i in range(x, -1, -1):
#         if arr[i][1] == None:
#             return i

# def node_to_js(tree, parent=4):
#     return [{
#             "name": name,
#             "parent": parent,
#             "children": node_to_js(node, name)
#         }
#         for name, node in tree.items()
#     ]
