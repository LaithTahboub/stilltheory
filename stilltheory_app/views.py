import subprocess
from django.shortcuts import render
from django.urls import reverse

from .form import *
import psycopg2
import js2py
from .get_games import *
from .authentication import *

conn = psycopg2.connect(
        user="postgres",
        host="127.0.0.1",
        port="5432",
        database="stilltheory_database",
        password="tahboub989" 
    )

def index(request):
    return render(request, 'stilltheory_app/homepage.html', {})

def login():
    return auth()



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
        # print('current datadump id' + str(data_dump[i][0]))
        # print('next datadump parent id' + str(data_dump[i + 1][1]))
        # print('current opening' + str(data_dump[i][3]))
        
        # if data_dump[i][1] == data_dump[i - 1][0]:
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
            print(position)
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
            print(opening_name)
        # elif (str_list[i] == 'p' and str_list[i + 1] == 'a' and str_list[i + 2] == 'r' and str_list[i + 3] == 'e' and str_list[i + 5] == 'n' and str_list[i + 6] == 't'): 




    str_list = ('[{\'name\': \'Repertoire\', \'parent\': null, \'children\': ') + (str_list) + ('}];')
    print(str_list)

    return render(request, 'stilltheory_app/dashboard.html', {'str': str_list})    

def node_to_js(tree, parent=4):
    return [{
            "name": name,
            "parent": parent,
            "children": node_to_js(node, name)
        }
        for name, node in tree.items()
    ]
