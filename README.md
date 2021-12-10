# Product Data Migration


## Purpose

This Python script provides a way to synchronise a product from the Mononoth into PIM.

It expects a list of product codes in CSV format, with no header row. To generate the missing product codes 
see the comment on this ticket: https://notonthehighstreet.atlassian.net/browse/PIM-1417

It can be run repeatedly against existing products with no ill effects. If the product exists in PIM it simply 
won't sync it.

There is a 1-second delay occurs between each sync to avoid overloading the PIM api.

You'll need to provide the environment to run in (qa/stag/prod) and also a valid JWT token for authentication.


## Getting a valid JWT Token

In order for the API calls to work a valid JWT Token needs to be provided.

The steps to get this are as follows (for Chrome, substitute as needed for other browsers):

1. Log in to the Partner area (CMS) on the corresponding environment, e.g. https://noths.public.shared.qa.noths.com/admin
2. Right click and select Inspect to go to the Developer Tools window
3. Open the Applications tab
4. Under Storage click on Local Storage
5. Look for an entry like: CognitoIdentityServiceProvider.<random_sequence>.<login_email>.idToken
6. Take the value from this entry, this is the JWT Token you need

IMPORTANT: Only Admin accounts should be used for this script, as whilst you might pass Authentication, you need to be 
Authorised to sync the product too. Partners can't access other Partners products (or at least they shouldn't!)


## Running the script

The script should run on Python 2.7, however I've only run it on the latest v3.9. 
Will try and get someone without v3 installed to verify.

Note: it requires the *requests* library to be installed, so you'll need to install *pip* first. 
See https://stackoverflow.com/questions/17271319/how-do-i-install-pip-on-macos-or-os-x

Execute the following command:

    $ python product_sync.py -i <input_file> -e <environment> -j <jwt_token>

e.g `python product_sync.py -i product_codes.csv -e qa -j abcde`

The script defaults the file to product_codes.csv but the other two values are required or the script will reject them.

The script logs any product code that fails to sync (non 200 status code returned), so no response indicates all is well.