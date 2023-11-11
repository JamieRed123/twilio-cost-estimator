'''This code is to estimate the cost of sending an outgoing SMS message with Twilio'''
# SMS using GSM-7 encoding can have max 160 characters per segment (153 if multiple segments)
# SMS using unicode can have max of 70 characters per segment (67 if multiple segments)

# TODO: Make it so that it accounts for 16-bit unicode (1 char) and 32-bit unicode (2 char)
# TODO: Calculate cost savings if Unicode characters are removed and inform user

# Imports
import math
import secret

# User Inputs
message = secret.my_message #"This is my message here! Hopefully it won't cost me too much to send because that would be a real pain in the ass! "
code = 'long' # either "long" for long code or "short" for short code phone number
quantity = 450000 # number of users to receive message


# Constants
gsm_per_single = 160
gsm_per_multiple = 153
unicode_per_single = 70
unicode_per_multiple = 67
pricing = {
    'long':{
        'tier1':{'price':0.0079, 'quantity_bracket':150000},
        'tier2':{'price':0.0077, 'quantity_bracket':150000},
        'tier3':{'price':0.0075, 'quantity_bracket':200000},
        'tier4':{'price':0.0073, 'quantity_bracket':250000},
        'tier5':{'price':0.0071, 'quantity_bracket':250000},
        'tier6':{'price':0.0069, 'quantity_bracket':10000000000} # upper limit arbitrarily set at 10 billion
    },
    'short':{
            'tier1':{'price':0.0079, 'quantity_bracket':150000},
            'tier2':{'price':0.0077, 'quantity_bracket':150000},
            'tier3':{'price':0.0075, 'quantity_bracket':200000},
            'tier4':{'price':0.0073, 'quantity_bracket':250000},
            'tier5':{'price':0.0071, 'quantity_bracket':250000},
            'tier6':{'price':0.0069, 'quantity_bracket':10000000000} # upper limit set at 10 billion
        }
} # as of now the pricing is the same for both long and short code but that is subject to change if Twilio decides


# Initialize variables
gsm_count = 0
unicode_count = 0
message_char_list = list(message)
unicode_char_list = []

# Calculate number of GSM-7 and Unicode characters
for char in message_char_list:
    if ord(char) < 127 or char in {'^', '{', '}', '\\', '[', ']', '~', '|', '€'}:
        gsm_count += 1
    else:
        unicode_count += 1
        unicode_char_list.append(char)

# Calculate n umber of segments
if unicode_count == 0: # all text sent as GSM-7
    total_char_count = gsm_count
    gsm_only = True
    if total_char_count <= gsm_per_single: # single segment needed
        segments = 1
    else: # multiple segments needed
        segments = math.ceil(total_char_count/gsm_per_multiple)
else: # at least one unicode character so all text converted to unicode
    total_char_count = gsm_count + unicode_count
    gsm_only = False
    if total_char_count <= unicode_per_single:
        segments = 1
    else: # multiple segments needed
        segments = math.ceil(total_char_count/unicode_per_multiple)


# Calculate costs
total_cost = 0
quantity_left = quantity
if code.lower() == 'long' or 'short': # check for correct code format to determine pricing
    for n in range(1, len(pricing['short'])+1):
        pps = pricing[code][f"tier{n}"]['price']
        quantity_bracket = pricing[code][f"tier{n}"]['quantity_bracket']
        if quantity_left > quantity_bracket: # quantity more than bracket
            total_cost += pps*segments*quantity_bracket
            quantity_left -= quantity_bracket
        else: # quantity less than current bracket max
            total_cost += pps*segments*quantity_left
            quantity_left = 0
            break
else: # code format entered incorrectly
    print(f'Error: "{code}" is not a recognized input. Use "short" for short code or "long" for long code phone numbers.')


# Outputs
print(f'Message: {message}')
if gsm_only:
    print(f'This message uses {segments} segments and uses only GSM-7 characters')
else:
    if unicode_count == 1: # format 'character' to singular
        print(f'This message uses {segments} segments and includes {unicode_count} Unicode character: {str(unicode_char_list)[1:-1]}')
    else:  # format 'characters' to plural
        print(f'This message uses {segments} segments and includes {unicode_count} Unicode characters: {str(unicode_char_list)[1:-1]}')
    print('Hint: To reduce number of segments (and thus costs) consider removing the Unicode characters.')
print(f'The cost to send this message to all {quantity} users is ${total_cost:.2f} plus carrier fees that may apply')
unit_cost = round(total_cost/quantity, 5)
print(f'The cost per user is: ${unit_cost}')




