import argparse, time, csv, requests

parser = argparse.ArgumentParser(description = 'Sync Products from Mononoth to PIM')
parser.add_argument('-input_file', type=str, default='product_codes.csv', help='Product Codes to Sync')
parser.add_argument('-env', type=str, required='true', help='Environment to sync (qa/stag/prod)')
parser.add_argument('-jwt_token', type=str, required='true', help='JWT Token')
args = parser.parse_args()

def syncProduct(headers, env, product_code):
    url = "https://prdmgt-data-api.{}.noths.com/api/pim/v1/legacy/products/{}/product-id".format(env, product_code)
    return requests.get(url, headers = headers)

with open(args.input_file, "r") as input_file:
    reader = csv.reader(input_file)

    headers = { 'x-id-token': args.jwt_token }

    for row in reader:
        status_code = syncProduct(headers, args.env, row[0]).status_code
        if (status_code != 200):
            print(row[0] + " failed to sync, status code: " + str(status_code))
        time.sleep(1) # delay to avoid overloading PIM api

    input_file.close()
