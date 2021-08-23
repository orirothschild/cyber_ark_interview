# cyber_ark_interview


## invoking this lambda

to invoke this lambda we must:

1. send a GET http request to the API gateway serving this lambda with the right resource, aka :https://qsxdnxx5ri.execute-api.us-east-1.amazonaws.com/default/invoke
2. set query params to invoke one of the three functions, using the KEY "action" and function name as value
    a. ?action=top_ten, will return a list of the top ten countires with most new cases this week
    b. ?action=avg_cases, will return the avg cases per 100KM^2 per country alphabeticly
    c. ?action=most infected, will return a list of 5 countries with moist new confirmed cases in the last 10 days
3.  if action key is not specified, an error will result specifing the required key


