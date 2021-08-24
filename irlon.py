import pandas as pd
import requests
import dateutil.parser
from datetime import datetime
import io

def get_irlon(params='all', level='both', start='2021-07-12', end='now'):
    '''
    input:
    params (string or list of strings): 'all', or a selection of the parameters available. Default is 'all'.
    level (string): S (surface), B (bottom), or 'both'. Default is 'both'.
    start (string): start date with format yyyy-mm-dd. Default start of operations '2021-07-12'.
    end (string): end day with format yyyy-mm-dd or 'now'. Default is 'now'.
    param options:
        - 'CDOM', 
        - 'CDOM+Fluorescence', 
        - 'Chlorophyll', 
        - 'Chlorophyll+(blue)+fluorescence', 
        - 'Phycocyanin+fluorescence', 
        - 'Turbidity', 
        - 'Dissolved+oxygen', 
        - 'Oxygen+saturation', 
        - 'Specific+conductance', 
        - 'Water+temperature', 
        - 'pH', 
        - 'Nitrate', 
        - 'Phosphate',  
        - 'Water+pressure', 
        -'Instrument+depth'

    output: pandas dataframe
    '''

    extra = []
    if params == 'all':
        params = ['CDOM', 'CDOM+Fluorescence', 'Chlorophyll', 'Chlorophyll+(blue)+fluorescence', 'Phycocyanin+fluorescence', 'Turbidity', 
        'Dissolved+oxygen', 'Oxygen+saturation', 'Specific+conductance', 'Water+temperature', 'pH', 'Nitrate', 'Phosphate',  'Water+pressure', 'Instrument+depth', ]

        extra = ['Turbidity+(470nm)', 'Turbidity+(532nm)', 'Turbidity+(650nm)']
    else:
        if isinstance(params, str):
            params = [params]

    if level == 'both':
        level = ['S', 'B']
    else:
        level = [level]

    string = ''
    for l in level:
        for p in params:
            string = string+'parameters[]=LO-L1%s-WQ+%s&' % (l, p)
        if l == 'S':
            for p in extra:
                string= string+'parameters[]=LO-L1%s-WQ+%s&' % (l, p)

    start = dateutil.parser.parse(start).strftime('%Y-%m-%dT%H:%M')

    if end == 'now':
        end = datetime.now().strftime('%Y-%m-%dT%H:%M')
    else:
        end = datetime.strptime(end, '%Y-%m-%d').strftime('%Y-%m-%dT%H:%M')
    time = 'time=%s-04:00/%s-04:00' %(start, end)

    url = 'https://irlon.org/services/download.php?'+time+'&tz=est&standard=true&output=csv&pretty=true&'+string[:-1]

    print(url)
    resp = requests.get(url, allow_redirects=False)
    skip = find_skip(resp)
    df = pd.read_csv(io.StringIO(resp.content.decode('utf-8')), parse_dates=['Time (est)'], skiprows=skip)

    df.set_index('Time (est)', inplace=True)
    return df


def find_skip(resp):
	# Finds how many rows to skip from the ironl server request
	# input: server reqiest object
	# output: int, number of rows to skip

    skip=0
    for l in resp.content.splitlines():
        if str(l)[2]=='%':
            skip+=1
    return  skip


def apply_qc(df):
	# Remove QC columns and replace variables with nan when QC is not good
	# input : irlon dataframe with qc variables
	# output: QC masked dataframe

    varl = df[[var for var in df.columns if 'quality' not in var]]
    varl_q = df[[var for var in df.columns if 'quality' in var]]
    varl_q.columns=varl.columns
    return varl.where(varl_q=='good')


def params():
	params = ['CDOM', 'CDOM+Fluorescence', 'Chlorophyll', 'Chlorophyll+(blue)+fluorescence', 'Phycocyanin+fluorescence', 'Turbidity',
	'Dissolved+oxygen', 'Oxygen+saturation', 'Specific+conductance', 'Water+temperature', 'pH',
	'Nitrate', 'Phosphate',  'Water+pressure', 'Instrument+depth']
	for p in params:
		print(p)


if __name__ == "__main__":

	from datetime import datetime
	# only surface phyco for all time since begining
	df = get_irlon(params='Phycocyanin+fluorescence', level='S')
	# apply mask
	df = apply_qc(df)
	# save file
	df.to_csv('irlon_%s.csv' % datetime.now().strftime('%Y-%m-%d'))


