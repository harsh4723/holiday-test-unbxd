import pandas as pd
import requests
import json

from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


# Example usage

csv_file_path = 'UkASCf.csv'
df = pd.read_csv(csv_file_path)

req  = 10
# url = "https://search.unbxd.io" + df['ClientRequestURI'][0]
# print(url)
# res = requests.get(url)
# jres = json.loads(res.content)
# prod_array =  jres.get('response').get('products')
# print(prod_array[0].get('autosuggest'))

def remove_query_param_from_path(path, param_to_remove):
    parsed_url = urlparse(path)
    query_params = parse_qs(parsed_url.query)
    if param_to_remove in query_params:
        del query_params[param_to_remove]
    new_query = urlencode(query_params, doseq=True)
    updated_path = urlunparse(parsed_url._replace(query=new_query))
    
    return updated_path


for i in range(0,req):
    updated_path = remove_query_param_from_path(df['ClientRequestURI'][i], "json.wrf")
    if "/search" in updated_path:
        continue
    url = "https://search.unbxd.io" + updated_path
    try:
        demo_url = "http://internal-a0484b72775f611ed98b10284fd5d35d-2106550818.eu-west-2.elb.amazonaws.com"+ updated_path
        res = requests.get(url)
        demo_res = requests.get(demo_url)
        jres = json.loads(res.content)
        jres_demo = json.loads(demo_res.content)
        num_pro = jres.get('response').get('numberOfProducts')
        num_pro_demo = jres_demo.get('response').get('numberOfProducts')
        #print(f"num_pro {num_pro} num_pro_demo {num_pro_demo}")
        prod_array =  jres.get('response').get('products')
        pro_array_demo = jres_demo.get('response').get('products')
        if num_pro != num_pro_demo :
            print(f"num pro different for {url} prod {num_pro_demo}")
        if len(prod_array) != len(pro_array_demo):
            print("len prod array is different for url", url)
            continue
        for i in range(0, len(prod_array)):
            if prod_array[i].get("autosuggest") != pro_array_demo[i].get("autosuggest"):
                print("autosuggest is different for url", url)
                break
            if prod_array[i].get("doctype") != pro_array_demo[i].get("doctype"):
                print("autosuggest product type is different for url", url)
                break
    except Exception as e:
        print("exception for url",url)

print("Finished comparing")




