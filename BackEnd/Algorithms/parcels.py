''' w l h
    s1 : [0.85, 1.1, 0.95]
    s2 : [0.92, 1.3, 1.1]
    s3 : [1.1, 1.4, 1.3]

    m1 : [1.7, 1.9, 1.2]
    m2 : [1.85, 2.1, 1.3]
    m3 : [1.9, 2.2, 1.4]

    l1 : [2.1, 2.55, 2.2]
    l2 : [2.3, 2.7, 2.4]
    l3 : [2.8, 3.1, 2.4]
'''

from distutils.log import info


class Info:
    containers_data = {
            "20Standard" : [2.4, 5.895, 2.392],
            '40Standard' : [2.4, 12.029, 2.392],
            '40HighCube' : [2.4, 12.024, 2.697],
            'Small' : [2.37, 5.9, 2.24], 
            'Large' : [2.37, 12, 2.4] #32.428728
        }
    containers_weight = {
        '20Standard' : 21700,
        '40Standard' : 27400,
        '40HighCube' : 27400,
        'Small' : 21700,
        'Large' : 27400
    }
    parcels_data = {
            "ssp" : [0.76, 1.12, 0.54], 
            "smp" : [0.76, 1.12, 0.73],
            "hssp" : [0.76, 1.12, 1.09],

            "mlp" : [1.1, 1.8, 0.73],
            "mp" : [1.1, 1.8, 1.09],

            "lp" : [1.515, 2.22, 0.73],
            "lhp" : [1.515, 2.22, 0.85],

            "etc" : [1.1, 1.5, 1],

            'zero' : [0, 0, 0]
        }
    stack_info = {
        101 : [0.76, 1.12, 1.09],
        102 : [0.76, 1.12, 0.73],
        103 : [0.76, 1.12, 0.54],
        104 : [1.1, 1.8, 1.09],
        105 : [1.1, 1.8, 0.73],
        106 : [1.515, 2.22, 0.73],
        201 : [0.76, 1.12, 2.17],
        202 : [0.76, 2.24, 2.24],
        203 : [0.76, 2.24, 2.24],
        204 : [2.2, 1.5, 2.4],
        205 : [2.28, 1.12, 2.18],
        206 : [2.28, 1.12, 2.19],
        207 : [1.515, 2.22, 2.31],
        208 : [2.28, 1.12, 2.17]
    }

    stack_members = {
        101 : {'fl_1' : ['hssp'], 
                'fl_2' : ['hssp']},
        102 : {'fl_1' : ['smp'],
                'fl_2' : ['smp'],
                'fl_3' : ['smp']},
        103 : {
            'fl_1' : ['ssp'],
            'fl_2' : ['ssp'],
            'fl_3' : ['ssp'],
            'fl_4' : ['ssp']
        },
        104 : {
            'fl_1' : ['mp'],
            'fl_2' : ['mp']
        },
        105 : {
            'fl_1' : ['mlp'],
            'fl_2' : ['mlp'],
            'fl_3' : ['mlp']
        },
        106 : {
            'fl_1' : ['lp'],
            'fl_2' : ['lp'],
            'fl_3' : ['lp']
        },
        201 : {
            'fl_1' : ['ssp'],
            'fl_2' : ['ssp'],
            'fl_3' : ['hssp']
        },
        202 : {
            'fl_1' : ['smp', 'smp'],
            'fl_2': ['etc']
        },
        203 : {
            'fl_1' : ['ssp', 'ssp'],
            'fl_2' : ['etc']
        },
        204 : {
            'fl_1' : ['etc', 'etc'],
            'fl_2' : ['lhp']
        },
        205 : {
            'fl_1' : ['hssp', 'hssp', 'hssp'],
            'fl_2' : ['mp']
        },
        206 : {
            'fl_1' : ['smp', 'smp', 'smp'],
            'fl_2' : ['smp', 'smp', 'smp'],
            'fl_3' : ['mlp']
        },
        207 : {
            'fl_1' : ['lhp'],
            'fl_2' : ['lp'],
            'fl_3' : ['lp']
        },
        208 : {
            'fl_1' : ['ssp', 'ssp', 'ssp'],
            'fl_2' : ['ssp', 'ssp', 'ssp'],
            'fl_3' : ['mp']
        }
    }
    def get_parcels_info(parcel_name=None):
        if parcel_name != None:
            return Info.parcels_data[parcel_name]
        else :
            return Info.parcels_data
        
    def get_container_info(container_name=None):
        if container_name != None:
            return Info.containers_data[container_name]
        else :
            return Info.containers_data

    def get_stack_info(stack_name):
        return Info.stack_info[stack_name]

    def get_stack_members(stack_name):
        return Info.stack_members[stack_name]
    
    def get_container_weight(container_id):
        return Info.containers_weight[container_id]
