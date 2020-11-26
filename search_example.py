import json
import re


#@app.route("/test1")
def test1_sel( vocabulary = 'AnalysisUnit', term = 'geo' ):
  #vocabulary = request.args.get("vocab")

  ## method 1: use a dictionary {}
  #file_names = {
  #  'AnalysisUnit'     : 'ex_response_AnalysisUnit.json'     ,
  #  'TimeMethod'       : 'ex_response_TimeMethod.json'       , 
  #  'SamplingProcedure': 'ex_response_SamplingProcedure.json', 
  #  'ModeOfCollection' : 'ex_response_ModeOfCollection.json' ,
  #  'TypeOfInstrument' : 'ex_response_TypeOfInstrument.json'
  #}
  #
  # name_file = file_names[ vocabulary ]

  ## method 2: compose filename (rely on file naming conventions)
  name_file = 'ex_response_' + vocabulary + '.json'

  with open(name_file, 'r') as ff:
    data = json.load( ff )   # read json into python dict

  # build a list of data.listOfCodes.languagePrefLabel.value
  lpls = [ code['languagePrefLabel']['value'] for code in data['listOfCodes'] ]  # list comprehension
  ## same as
  #lpls = []
  #for code in data['listOfCodes']:
  #  lpls += [ code['languagePrefLabel']['value'] ]

  ## search using regular expression package
  compiled_term = re.compile(term, re.IGNORECASE)  # compile the search term for speed

  ## make a list of indices of matching items
  matched_indices = []
  ## loop over pairs (list index, list entry)
  for ii,lpl in enumerate(lpls):
    if re.search(compiled_term, lpl):
      # if term is found in the languagePrefLabel.value string, save its index in the data.listOfCodes
      matched_indices += [ ii ]

  ## build resulting data with an empty listOfCodes
  matched_data = { 'listOfCodes' : [], 'vocab' : data['vocab'] }

  ## extend the listOfCodes list with mathed list entries using list comprehension
  matched_data['listOfCodes'] += [ data['listOfCodes'][ii] for ii in matched_indices ]

  return matched_data

  #response = Response(json.dumps(data), mimetype='application/json')
  #response.headers.add('Access-Control-Allow-Origin', '*')
  #return response


## main function invoking test1_sel() with command line arguments and printing the results for debugging purposes
if __name__ == '__main__':
  import os
  import sys

  # some defaults
  vocab, term = 'AnalysisUnit', 'omet'

  ## access command line arguments as the sys.argv list
  if len(sys.argv) > 1:
    vocab = sys.argv[1]
  if len(sys.argv) > 2:
    term = sys.argv[2]
  print 'search vocab =', vocab, 'for term =', term

  ## small protection against non-existent files
  name_file = 'ex_response_' + vocab + '.json'
  assert os.path.exists( name_file ), 'failure: non-existent example %s vocab file!'%(name_file)


  result = test1_sel( vocab, term )

  ## somehow in the dictionaries all strings became unicode strings (e.g. u'code' instead of 'code' or "code" etc.), 
  ## for nicer printout convert the json to a usual string in order to remove these unicode string prefixes
  result_str = json.dumps(result)  # convert json to a string
  print 'result =', result_str
