groups = {
    'remote': {
        'contributor' : {
            'host': '192.168.0.45',
            'port': '5432',
            'user': 'json_contributor',
            'password': 'json_contributor',
            'driver': 'postgresql',
            'db_name': 'promis'
        },
        'root' : {
            'host': '192.168.0.45',
            'port': '5432',
            'user': 'postgres',
            'password': 'XHTDJeujlbt',
            'driver': 'postgresql',
            'db_name': 'promis'
        }
    },
    'local': {
        'contributor' : {
            'host': 'localhost',
            'port': '3306',
            'user': 'root',
            'password': 'littlelover',
            'driver': 'mysql',
            'db_name': 'promis'
        },
        'root' : {
            'host': 'localhost',
            'port': '3306',
            'user': 'root',
            'password': 'littlelover',
            'driver': 'mysql',
            'db_name': 'promis'
        }
    }
}

use = 'local'