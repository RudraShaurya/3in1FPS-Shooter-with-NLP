models = {
    'adventure': {'enemy': {'model': 'assets/adventure/Bug.obj',
                            'texture': 'assets/adventure/basecolor.png',
                            'color': '#ffffff'},
                  'background': {'texture': 'assets/adventure/background.jpg'},
                  'building': {'model': 'assets/adventure/Trees.obj',
                               'texture': 'assets/adventure/klp_leaf_A_col.tga',
                               'color': '#ffffff',
                               'scale': 5},
                  'ground': {'texture': 'grass',
                             'color': '#ffffff'},
                  'speed': 1},


    'horror': {'enemy': {'model': 'assets/horror/Seraph.obj',
                         'texture': '',
                         'color': '#ffffff'},
               'background': {'texture': 'assets/horror/background.jpg'},
               'building': {'model': 'assets/horror/pillar.obj',
                            'texture': 'assets/horror/marble.jpg',
                            'color': '#000000',
                            'scale': 0.002},
               'ground': {'texture': '',
                          'color': '#000000'},
               'speed': 3},

    'fantasy': {'enemy': {'model': 'assets/fantasy/hellokitty.obj',
                          'texture': 'assets/fantasy/basecolor.jpeg',
                          'color': '#f4c2c2'},
                'background': {'texture': 'assets/fantasy/background.jpg'},
                'building': {'model': 'assets/fantasy/Candycane.obj',
                             'texture': '',
                             'color': '#ffc0cb',
                             'scale': 5},
                'ground': {'texture': 'grass',
                           'color': '#ffffff'},
                'speed': 1}
}
SIZE = 256
BASE_SPEED = 8
ENEMY_COUNT = 20
SECRET_KEY = "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"
PROMPT = 'Can you classify this sentence into 3 categories and only answer me the category and nothing else - ' \
         'Horror, Fantasy and Adventure(shooting games, action games are in Adventure) - '
