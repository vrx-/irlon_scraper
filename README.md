Building module to get irlon data from lake Okeechobbe

https://irlon.org/

[LO-L1B](https://irlon.org/?health=Off&quality=On&units=Metric&duration=3%20days&maps=storm_tracks&legend=Off&forecast=Point&hti=&nhc=undefined&sst=&current=&datum=MLLW&windPrediction=wind%20speed%20prediction&region=&bbox=-80.7934,27.1389,-80.7934,27.1389&iframe=null&mode=home&platform=LO-L1B-WQ&skipState=undefined) (Bottom)

[LO-L1S](https://irlon.org/?health=Off&quality=On&units=Metric&duration=3%20days&maps=storm_tracks&legend=Off&forecast=Point&hti=&nhc=undefined&sst=&current=&datum=MLLW&windPrediction=wind%20speed%20prediction&region=&bbox=-80.7934,27.1389,-80.7934,27.1389&iframe=null&mode=home&platform=LO-L1S-WQ&skipState=undefined) (Surface)

Currently module has 3 functions

	get_irlon(params='all', level='both', start='2021-07-12', end='now')

Obtain data from server

input:
    **params** (string or list of strings): 'all', or a selection of the parameters available. Default is 'all'.
    **level** (string): S (surface), B (bottom), or 'both'. Default is 'both'.
    **start** (string): start date with format yyyy-mm-dd. Default start of operations '2021-07-12'.
    **end** (string): end day with format yyyy-mm-dd or 'now'. Default is 'now'.
    param options:
        * 'CDOM', 
        * 'CDOM+Fluorescence', 
        * 'Chlorophyll', 
        * 'Chlorophyll+(blue)+fluorescence', 
        * 'Phycocyanin+fluorescence', 
        * 'Turbidity', 
        * 'Dissolved+oxygen', 
        * 'Oxygen+saturation', 
        * 'Specific+conductance', 
        * 'Water+temperature', 
        * 'pH', 
        * 'Nitrate', 
        * 'Phosphate',  
        * 'Water+pressure', 
        * 'Instrument+depth'

output: pandas dataframe with requested parms plus quality control variables for those params


	apply_qc(df)

Remove QC columns and replace variables with nan when QC is not good
input : irlon dataframe with qc variables
output: QC masked dataframe

	params()
Prints posibilities of paramas to chose from if not 'all' 

for examples of usage see notebooks.


