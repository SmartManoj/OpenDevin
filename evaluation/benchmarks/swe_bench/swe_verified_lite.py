import json

import toml

swe_verified_lite = [
    'astropy__astropy-12907',
    'astropy__astropy-14182',
    'astropy__astropy-14365',
    'astropy__astropy-14995',
    'django__django-10914',
    'django__django-11099',
    'django__django-11133',
    'django__django-11179',
    'django__django-11815',
    'django__django-11848',
    'django__django-11964',
    'django__django-11999',
    'django__django-12125',
    'django__django-12308',
    'django__django-12708',
    'django__django-13028',
    'django__django-13033',
    'django__django-13158',
    'django__django-13315',
    'django__django-13401',
    'django__django-13551',
    'django__django-13590',
    'django__django-13658',
    'django__django-13925',
    'django__django-13933',
    'django__django-13964',
    'django__django-14017',
    'django__django-14155',
    'django__django-14238',
    'django__django-14534',
    'django__django-14580',
    'django__django-14608',
    'django__django-14672',
    'django__django-14752',
    'django__django-14787',
    'django__django-14855',
    'django__django-14915',
    'django__django-14999',
    'django__django-15252',
    'django__django-15695',
    'django__django-15814',
    'django__django-15851',
    'django__django-16139',
    'django__django-16255',
    'django__django-16527',
    'django__django-16595',
    'django__django-17087',
    'matplotlib__matplotlib-23299',
    'matplotlib__matplotlib-23314',
    'matplotlib__matplotlib-23476',
    'matplotlib__matplotlib-24149',
    'matplotlib__matplotlib-24970',
    'matplotlib__matplotlib-25311',
    'matplotlib__matplotlib-25332',
    'psf__requests-2317',
    'pydata__xarray-4094',
    'pylint-dev__pylint-7080',
    'pytest-dev__pytest-7432',
    'pytest-dev__pytest-7490',
    'scikit-learn__scikit-learn-10297',
    'scikit-learn__scikit-learn-13142',
    'scikit-learn__scikit-learn-13439',
    'scikit-learn__scikit-learn-13496',
    'scikit-learn__scikit-learn-13779',
    'scikit-learn__scikit-learn-14087',
    'scikit-learn__scikit-learn-14894',
    'scikit-learn__scikit-learn-14983',
    'scikit-learn__scikit-learn-25747',
    'sphinx-doc__sphinx-11445',
    'sphinx-doc__sphinx-8595',
    'sphinx-doc__sphinx-8721',
    'sympy__sympy-12419',
    'sympy__sympy-12481',
    'sympy__sympy-13031',
    'sympy__sympy-13480',
    'sympy__sympy-13647',
    'sympy__sympy-15345',
    'sympy__sympy-16792',
    'sympy__sympy-17139',
    'sympy__sympy-17630',
    'sympy__sympy-17655',
    'sympy__sympy-18189',
    'sympy__sympy-18199',
    'sympy__sympy-18698',
    'sympy__sympy-20154',
    'sympy__sympy-20590',
    'sympy__sympy-21379',
    'sympy__sympy-21612',
    'sympy__sympy-21847',
    'sympy__sympy-22714',
    'sympy__sympy-23262',
    'sympy__sympy-24066',
    'sympy__sympy-24213',
]

openhands_lite_resolved = [
    'astropy__astropy-12907',
    'astropy__astropy-13579',
    'astropy__astropy-14096',
    'astropy__astropy-14309',
    'astropy__astropy-14369',
    'astropy__astropy-14598',
    'astropy__astropy-14995',
    'astropy__astropy-7166',
    'astropy__astropy-7336',
    'astropy__astropy-7671',
    'django__django-10880',
    'django__django-10914',
    'django__django-10973',
    'django__django-11066',
    'django__django-11095',
    'django__django-11099',
    'django__django-11119',
    'django__django-11133',
    'django__django-11163',
    'django__django-11179',
    'django__django-11211',
    'django__django-11265',
    'django__django-11276',
    'django__django-11292',
    'django__django-11333',
    'django__django-11451',
    'django__django-11532',
    'django__django-11551',
    'django__django-11603',
    'django__django-11740',
    'django__django-11749',
    'django__django-11815',
    'django__django-11880',
    'django__django-11951',
    'django__django-11999',
    'django__django-12050',
    'django__django-12143',
    'django__django-12155',
    'django__django-12193',
    'django__django-12209',
    'django__django-12276',
    'django__django-12304',
    'django__django-12419',
    'django__django-12663',
    'django__django-12708',
    'django__django-12713',
    'django__django-12741',
    'django__django-12858',
    'django__django-13023',
    'django__django-13028',
    'django__django-13033',
    'django__django-13089',
    'django__django-13109',
    'django__django-13158',
    'django__django-13279',
    'django__django-13343',
    'django__django-13363',
    'django__django-13401',
    'django__django-13406',
    'django__django-13410',
    'django__django-13417',
    'django__django-13516',
    'django__django-13569',
    'django__django-13590',
    'django__django-13658',
    'django__django-13670',
    'django__django-13741',
    'django__django-13786',
    'django__django-13809',
    'django__django-13820',
    'django__django-13821',
    'django__django-13933',
    'django__django-14007',
    'django__django-14017',
    'django__django-14089',
    'django__django-14122',
    'django__django-14238',
    'django__django-14349',
    'django__django-14373',
    'django__django-14434',
    'django__django-14493',
    'django__django-14539',
    'django__django-14580',
    'django__django-14608',
    'django__django-14672',
    'django__django-14752',
    'django__django-14765',
    'django__django-14787',
    'django__django-14855',
    'django__django-14915',
    'django__django-14999',
    'django__django-15022',
    'django__django-15103',
    'django__django-15104',
    'django__django-15128',
    'django__django-15268',
    'django__django-15277',
    'django__django-15278',
    'django__django-15315',
    'django__django-15368',
    'django__django-15382',
    'django__django-15467',
    'django__django-15499',
    'django__django-15525',
    'django__django-15561',
    'django__django-15569',
    'django__django-15572',
    'django__django-15731',
    'django__django-15814',
    'django__django-15851',
    'django__django-15916',
    'django__django-15987',
    'django__django-16032',
    'django__django-16082',
    'django__django-16100',
    'django__django-16116',
    'django__django-16136',
    'django__django-16139',
    'django__django-16145',
    'django__django-16255',
    'django__django-16333',
    'django__django-16429',
    'django__django-16485',
    'django__django-16493',
    'django__django-16527',
    'django__django-16569',
    'django__django-16595',
    'django__django-16612',
    'django__django-16661',
    'django__django-16662',
    'django__django-16801',
    'django__django-16819',
    'django__django-16899',
    'django__django-16901',
    'django__django-17029',
    'django__django-17087',
    'django__django-7530',
    'django__django-9296',
    'matplotlib__matplotlib-13989',
    'matplotlib__matplotlib-20859',
    'matplotlib__matplotlib-22719',
    'matplotlib__matplotlib-22865',
    'matplotlib__matplotlib-23314',
    'matplotlib__matplotlib-23412',
    'matplotlib__matplotlib-24026',
    'matplotlib__matplotlib-24149',
    'matplotlib__matplotlib-24570',
    'matplotlib__matplotlib-24627',
    'matplotlib__matplotlib-24970',
    'matplotlib__matplotlib-25122',
    'matplotlib__matplotlib-25287',
    'matplotlib__matplotlib-25332',
    'matplotlib__matplotlib-25775',
    'matplotlib__matplotlib-26113',
    'matplotlib__matplotlib-26291',
    'pallets__flask-5014',
    'psf__requests-1142',
    'psf__requests-1766',
    'psf__requests-2317',
    'psf__requests-5414',
    'pydata__xarray-3151',
    'pydata__xarray-3305',
    'pydata__xarray-3677',
    'pydata__xarray-3993',
    'pydata__xarray-4075',
    'pydata__xarray-4094',
    'pydata__xarray-4356',
    'pydata__xarray-4629',
    'pydata__xarray-6461',
    'pydata__xarray-6721',
    'pydata__xarray-6744',
    'pydata__xarray-7233',
    'pylint-dev__pylint-6528',
    'pylint-dev__pylint-6903',
    'pylint-dev__pylint-7277',
    'pytest-dev__pytest-10081',
    'pytest-dev__pytest-5809',
    'pytest-dev__pytest-6202',
    'pytest-dev__pytest-7205',
    'pytest-dev__pytest-7432',
    'pytest-dev__pytest-7521',
    'pytest-dev__pytest-7571',
    'pytest-dev__pytest-7982',
    'pytest-dev__pytest-8399',
    'scikit-learn__scikit-learn-10297',
    'scikit-learn__scikit-learn-10844',
    'scikit-learn__scikit-learn-11310',
    'scikit-learn__scikit-learn-11578',
    'scikit-learn__scikit-learn-12585',
    'scikit-learn__scikit-learn-13135',
    'scikit-learn__scikit-learn-13142',
    'scikit-learn__scikit-learn-13328',
    'scikit-learn__scikit-learn-13439',
    'scikit-learn__scikit-learn-13496',
    'scikit-learn__scikit-learn-13779',
    'scikit-learn__scikit-learn-14053',
    'scikit-learn__scikit-learn-14087',
    'scikit-learn__scikit-learn-14141',
    'scikit-learn__scikit-learn-14496',
    'scikit-learn__scikit-learn-14710',
    'scikit-learn__scikit-learn-14894',
    'scikit-learn__scikit-learn-15100',
    'scikit-learn__scikit-learn-25102',
    'scikit-learn__scikit-learn-25232',
    'scikit-learn__scikit-learn-25931',
    'scikit-learn__scikit-learn-26323',
    'scikit-learn__scikit-learn-9288',
    'sphinx-doc__sphinx-10449',
    'sphinx-doc__sphinx-10466',
    'sphinx-doc__sphinx-10673',
    'sphinx-doc__sphinx-7454',
    'sphinx-doc__sphinx-7910',
    'sphinx-doc__sphinx-8120',
    'sphinx-doc__sphinx-8269',
    'sphinx-doc__sphinx-8459',
    'sphinx-doc__sphinx-8475',
    'sphinx-doc__sphinx-8593',
    'sphinx-doc__sphinx-8595',
    'sphinx-doc__sphinx-8721',
    'sphinx-doc__sphinx-9230',
    'sphinx-doc__sphinx-9258',
    'sphinx-doc__sphinx-9320',
    'sphinx-doc__sphinx-9367',
    'sphinx-doc__sphinx-9698',
    'sphinx-doc__sphinx-9711',
    'sympy__sympy-11618',
    'sympy__sympy-12096',
    'sympy__sympy-12419',
    'sympy__sympy-12481',
    'sympy__sympy-13372',
    'sympy__sympy-13480',
    'sympy__sympy-13647',
    'sympy__sympy-13878',
    'sympy__sympy-14711',
    'sympy__sympy-14976',
    'sympy__sympy-15017',
    'sympy__sympy-15345',
    'sympy__sympy-15349',
    'sympy__sympy-15599',
    'sympy__sympy-15875',
    'sympy__sympy-16450',
    'sympy__sympy-16766',
    'sympy__sympy-16792',
    'sympy__sympy-16886',
    'sympy__sympy-17139',
    'sympy__sympy-17655',
    'sympy__sympy-18189',
    'sympy__sympy-19346',
    'sympy__sympy-19637',
    'sympy__sympy-19783',
    'sympy__sympy-19954',
    'sympy__sympy-20154',
    'sympy__sympy-20801',
    'sympy__sympy-21847',
    'sympy__sympy-22456',
    'sympy__sympy-22714',
    'sympy__sympy-22914',
    'sympy__sympy-23262',
    'sympy__sympy-23534',
    'sympy__sympy-23950',
    'sympy__sympy-24066',
    'sympy__sympy-24213',
    'sympy__sympy-24443',
    'sympy__sympy-24539',
    'sympy__sympy-24661',
]
# intersect
# print(len(swe_verified_lite))
r = set(swe_verified_lite) & set(openhands_lite_resolved)
r = [
    'astropy__astropy-12907',
    'astropy__astropy-14995',
    'django__django-10914',
    'django__django-11099',
    'django__django-11133',
    'django__django-11179',
    'django__django-11815',
    'django__django-11999',
    'django__django-12708',
    'django__django-13028',
    'django__django-13033',
    'django__django-13158',
    'django__django-13401',
    'django__django-13590',
    'django__django-13658',
    'django__django-13933',
    'django__django-14017',
    'django__django-14238',
    'django__django-14580',
    'django__django-14608',
    'django__django-14672',
    'django__django-14752',
    'django__django-14787',
    'django__django-14855',
    'django__django-14915',
    'django__django-14999',
    'django__django-15814',
    'django__django-15851',
    'django__django-16139',
    'django__django-16255',
    'django__django-16527',
    'django__django-16595',
    'django__django-17087',
    'matplotlib__matplotlib-23314',
    'matplotlib__matplotlib-24149',
    'matplotlib__matplotlib-24970',
    'matplotlib__matplotlib-25332',
    'psf__requests-2317',
    'pydata__xarray-4094',
    'pytest-dev__pytest-7432',
    'scikit-learn__scikit-learn-10297',
    'scikit-learn__scikit-learn-13142',
    'scikit-learn__scikit-learn-13439',
    'scikit-learn__scikit-learn-13496',
    'scikit-learn__scikit-learn-13779',
    'scikit-learn__scikit-learn-14087',
    'scikit-learn__scikit-learn-14894',
    'sphinx-doc__sphinx-8595',
    'sphinx-doc__sphinx-8721',
    'sympy__sympy-12419',
    'sympy__sympy-12481',
    'sympy__sympy-13480',
    'sympy__sympy-13647',
    'sympy__sympy-15345',
    'sympy__sympy-16792',
    'sympy__sympy-17139',
    'sympy__sympy-17655',
    'sympy__sympy-18189',
    'sympy__sympy-20154',
    'sympy__sympy-21847',
    'sympy__sympy-22714',
    'sympy__sympy-23262',
    'sympy__sympy-24066',
    'sympy__sympy-24213',
]
# print(len(r))
# load config.toml


# pprint(non_gru_resolved)
if 0:
    file = open('evaluation/swe_bench/config.toml', 'r')
    config = toml.load(file)
    instance = config['selected_ids'][0]

    idx = r.index(instance)
    new_instance = r[idx + 1]


if 1:
    status_path = 'evaluation/benchmarks/swe_bench/status.json'

    with open(status_path, 'r') as f:
        data = json.load(f)

    resolved_instances = [i[0] for i in data['resolved']][:-1]
    unresolved_instances = [i[0] for i in data['unresolved']][:-1]
    # l = (set(resolved_instances) - set(r))
    # print(len(l))
    # print(len(r))
    if 1:
        new_set = set(swe_verified_lite) & set(unresolved_instances)
        new_list = list(sorted(new_set))
        print(new_list)
        print(len(new_list))

    if 1:
        new_set = (
            set(swe_verified_lite) - set(resolved_instances) - set(unresolved_instances)
        )
        print(f'{"Total:":<20}', len(swe_verified_lite))
        print(f'{"Resolved:":<20}', len(set(resolved_instances)))
        print(f'{"Unresolved:":<20}', len(set(unresolved_instances)))
        print(
            f'{"Resolved ratio:":<20} {len(resolved_instances)/len(swe_verified_lite):.2%}'
        )
    # if new_instance in unresolved_instances:
    #     print('new instance is unresolved')
    # if new_instance in resolved_instances:
    #     print('new instance is already resolved')

# print(new_instance)
# copy(new_instance)
