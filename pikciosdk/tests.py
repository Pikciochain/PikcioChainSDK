import base64
import hashlib

from PikcioChain import ClientAPI
from config import get_config
from log import Logger

config = get_config()


def run_test():
    logg = Logger()

    try:
        with open('/home/fabien/Images/blockchain1.png', 'rb') as img_file:
            base64.b64encode(img_file.read())
    except (IOError, TypeError):
        pass

    try:
        with open('/home/fabien/Images/matryoshka.png', 'rb') as img_file:
            base64.b64encode(img_file.read())
    except (IOError, TypeError):
        pass

    username = "pikcio_node_username"
    password_hash = hashlib.sha1("pikcio_node_password").digest().enode('hex')
    client_api = ClientAPI(username=username, password=password_hash)

    access = client_api.get_access_token()
    logg.debug("\n===Access :\n {0} \n===\n".format(access))

    ###########################################################################

    ############################################################
    #                                                          #
    #               UPDATE TEST 31/08/18                       #
    #                                                          #
    ############################################################

    ##################################
    # Everything related to the user #
    ##################################

    # OK :
    '''
    json_update_password = {
        "current_password": "qwerty",
        "password": "ytrewq",
        "retype_password": "ytrewq"
    }
    result = client_api.update_password(json_update_password)
    '''
    '''
    json_get_reset_token_forgotten_password = {
        "question_id": 1,
        "answer": "answer1"
    }
    result = client_api.get_reset_token_forgotten_password(
        json_get_reset_token_forgotten_password
    )
    '''
    '''
    json_reset_password = {
        "reset_token": "4525019d46b3c424d77917c9b2e1da781b9cec2e",
        "new_password": "azertyuiop",
        "confirm_password": "aztyuiop"
    }
    result = client_api.reset_password(json_reset_password)
    '''
    result = client_api.get_user_avatar()
    '''
    json_set_user_avatar = {
        "avatar":
            {
                "data": file_data,
                "value": "sangoku_api.png"
            }
    }
    result = client_api.set_user_avatar(json_set_user_avatar)
    '''
    # result = client_api.get_user_profile()
    '''
    json_update_user_profile = {
        "profile":
            {
                "children": {'value': 'azert', 'shared': False},
                "birth_date": {'value': '2', 'shared': True},
                "country": {'value': 'France', 'shared': False},
                "my new item": {'value': 'LE CRES', 'shared': False}
            }
    }
    result = client_api.update_user_profile(json_update_user_profile)
    '''
    # result = client_api.get_background()
    # result = client_api.get_tci()
    '''
    json_delete_custom_profile_item = {"item": "re test"}
    result = client_api.delete_custom_profile_item(
        json_delete_custom_profile_item
    )
    '''
    '''
    json_upload_data = {
        "data": "Jana kramer",
        "metadata": "say_my_name",
        "context": "Professional",
        "source": "API"
    }
    result = client_api.upload_data(json_upload_data)
    '''
    # TO BE TESTED :
    # not included in the current version :
    '''
    json_register = {
        "username": "",
        "firstname": "",
        "lastname": "",
        "email": ""
    }
    client_api.register()
    '''
    '''
    json_login = {
        "username": "johncena",
        "password": "toor"
    }
    client_api.login(json_login)
    '''
    # client_api.logout()
    # result = client_api.set_background('data_45')
    # result = client_api.import_profile()
    # result = client_api.export_profile()

    ###########################################################################

    ##################################
    # Everything related to contacts #
    ##################################

    # OK :

    # result = client_api.find_user(
    #     query='41f91225e521b2bb03f7680f26a8b366cb134c3e'
    # )
    '''
    json_add_contact = {
        "matr_id": "414d544d385356486b50346a434668744e73596754393574573872444"
                   "34d7a463375",
        "username": "jimmy"
    }
    result = client_api.add_contact(json_add_contact)
    '''
    # result = client_api.get_contacts()
    # result = client_api.get_contact_profile(
    #     matr_id='414d544d385356486b50346a57457387244434d7a463375'
    # )
    '''
    json_add_contact = {
        "matr_id": "414d544d385356486b50346a57457387244434d7a463375",
        "keep_files": True
    }
    result = client_api.remove_contact(json_add_contact)
    '''
    # result = client_api.accept_contact_request(
    #     matr_id="414d544d385356486b50346a57457387244434d7a463375"
    # )
    # result = client_api.reject_contact_request(
    #     matr_id="414d544d385356486b50346a57457387244434d7a463375"
    # )
    '''
    json_block_contact = {
        "matr_id": "414d544d385356486b50346a57457387244434d7a463375",
        "keep_files": False
    }
    result = client_api.block_contact(json_block_contact)
    '''
    # result = client_api.unblock_contact(
    #     matr_id="414d544d385356486b50346a57457387244434d7a463375"
    # )
    '''
    json_block_contact = {
        "matr_id": "414d544d385356486b50346a434668744e73596754393574573872444"
                   "34d7a463375",
        "action": "remove"
    }
    result = client_api.manage_replicant(json_block_contact)
    '''
    # TO BE TESTED :

    # not included in the current version :
    # client_api.import_contacts()
    # client_api.invite_someone()
    # result = client_api.get_notifications_online()

    ###########################################################################

    #########################################
    # Everything related to Pikcio messages #
    #########################################

    # OK :
    '''
    json_get_pikcio_messages = {
        "category": "received",
        "limit": 0,
        "date": "2017-04-01 12:12:12",
        "filter": "after"
    }
    result = client_api.get_pikcio_messages(json_get_pikcio_messages)

    # result = client_api.get_pikcio_message(
    #     msg_id='211197ad9109c3cf0f5793651e38f7dae5b5d28a'
    # )
    # result = client_api.delete_pikcio_message(
    #     msg_id='211197ad9109c3cf0f5793651e38f7dae5b5d28a'
    # )
    '''
    '''
    json_send_pikcio_message = {
        "content": "This is a text content of a Pikcio message",
        "subject": "TEST from API",
        "lifetime": '30',
        "certification": False,
        "external_receivers":
            [
                {"email": "dev@matchupbox", "name": "Support Matchupbox"}
            ],
        "receivers": [
            "414d544d385356486b50346a434668744e7359675439357457387244434d7a46"
            "3375"
        ]
    }
    result = client_api.send_pikcio_message(json_send_pikcio_message)
    '''
    # result = client_api.set_pikcio_message_to_read(
    #     msg_id='bfd927a239f2d8e61a9133e1fbe2b016d2de619b'
    # )
    # result = client_api.pikcio_message_request_certification(
    #     msg_id='bfd927a239f2d8e61a9133e1fbe2b016d2de619b'
    # )

    ###########################################################################

    #######################################
    # Everything related to chat messages #
    #######################################

    # OK :
    '''
    json_get_conversation = {
        "chat": {
            "matr_id": "414d544d385356486b50346a434668744e7359675439357457387"
                       "244434d7a463375",
            "date": "2018-01-01",
            "filter": "after",
            "limit": 1
        }
    }
    result = client_api.get_chat_conversation(json_get_conversation)
    '''
    '''
    json_send_chat_message = {
        "receivers":
            [
                {
                    'matr_id': '415133767636324c6d594c476246375138623943527a32'
                               '326972453566533933616b'
                },
                {
                    'matr_id': '414d544d385356486b50346a434668744e735967543935'
                               '7457387244434d7a463375'
                }
            ],
        "message": "Test from API NEW VERSION",
        "certify": False
    }
    result = client_api.send_chat_message(json_send_chat_message)
    '''
    # result = client_api.delete_chat_message(
    #     msg_id='0d1d588ad8393d7796066a67420641efb8776f71'
    # )
    # result = client_api.get_chat_message_status(
    #     msg_id='450f1a5002cbc8071dbd8e47e86f4bfed7509df5'
    # )
    # result = client_api.set_chat_message_to_read(
    #     msg_id='efa996a5a6216c696d112e1aa82578df05798fdd'
    # )

    # KO :

    # result = client_api.delete_chat_conversation(
    #     matr_id="414d544d385356486b50346a57457387244434d7a463375"
    # )

    ###########################################################################

    #######################################
    # Everything related to file messages #
    #######################################

    # OK:
    '''
    json_get_file_messages = {
        "file":
            {
                "matr_id": '414d544d385356486b50346a434668744e7359675439357457'
                           '387244434d7a463375',
                "date": '2016-04-18 09:06:16',
                "filter": "after",
                "limit": 2
            }
    }
    result = client_api.get_file_messages(json_get_file_messages)
    '''
    '''
    json_send_file_message = {
        "receivers":
            [
                {
                    'matr_id': '415133767636324c6d594c476246375138623943527a32'
                               '326972453566533933616b'
                },
                {
                    'matr_id': '414d544d385356486b50346a434668744e735967543935'
                               '7457387244434d7a463375'
                }
            ],
        "file_name": 'testingAPI.png',
        "file_content": file_data,
        "certify": True
    }

    result = client_api.send_file_message(json_send_file_message)
    '''
    # result = client_api.set_file_message_to_read(
    #     msg_id='459e1debe9310630e001ccd8acbaa2048f64c355'
    # )
    # result = client_api.delete_file_message(
    #     msg_id='459e1debe9310630e001ccd8acbaa2048f64c355'
    # )

    # MISSING PikcioChain.py :

    # client_api.get_file_message_meta_data()
    # client_api.get_file_message_matr_msg_id()

    ###########################################################################

    #######################################
    # Everything related to wall messages #
    #######################################

    # OK :
    '''
    json_get_wall_messages = {
        'wall':
            {
                "limit": 2,
                "date": "2017-01-28 14:14:14",
                "filter": "after"
            }
    }
    result = client_api.get_wall_messages(json_get_wall_messages)
    '''
    '''
    json_send_wall_file_message = {
        "file":
            {
                "data": file_data,
                "name": "test_wall from API.jpg"
            }
    }
    result = client_api.send_wall_message(json_send_wall_file_message)
    '''
    '''
    json_send_wall_text_message = {
        "message":
            {
                "data": "test from api"
            }
    }
    result = client_api.send_wall_message(json_send_wall_text_message)
    '''
    # result = client_api.delete_wall_message(
    #     message_id='a5d6e553c251c26680f8d887e815e0a59af5866f'
    # )
    # result = client_api.get_wall_message_comments(
    #     message_id='09152ea2963136d5ea5be98a79e8908f4dbf8dda'
    # )

    # to be tested :

    # not included in the current version
    # todo : all features concerning public wall (send, retrieve, ...)

    ###########################################################################

    #########################################
    # Everything related to file management #
    #########################################

    # OK :
    '''
    json_upload_file = {
        "files":
            [
                {
                    "file_name": "",
                    "file_content": file_data,
                    "tags": "api blockchain, test",
                    "contexts": ""
                },
                {
                    "file_name": "matryoshka.png",
                    "file_content": file_data2,
                    "tags": "",
                    "contexts": ""
                }
            ],
        "folder_name": "APIFolder"
    }
    result = client_api.upload_file(json_upload_file)
    '''
    '''
    json_delete_file = {
        "file_id": 1591,
        "check": False
    }
    result = client_api.delete_file(json_delete_file)
    '''
    '''
    json_get_files_info = {
        "folder_name": "APIFolder",
        "limit": 2
    }
    result = client_api.get_files_info(json_get_files_info)
    '''
    # result = client_api.get_file_info('8')
    # result = client_api.get_folders()
    # result = client_api.encrypt_file('6')
    # result = client_api.decrypt_file('8')
    # result = client_api.certify_file('8')
    # result = client_api.request_file_history('8')

    # KO :

    # result = client_api.delete_folder("APIFolder")
    # result = client_api.move_file(data_43)

    ###########################################################################

    ##################################
    # Everything related to Settings #
    ##################################

    # OK :

    # result = client_api.report_bug("test API")

    # to be tested :

    # not included in the current version :
    # result = client_api.edit_network()
    # result = client_api.edit_message_lifetime()
    # result = client_api.create_api()
    # result = client_api.delete_api()
    # result = client_api.get_api_info()
    # result = client_api.get_api_config_file()
    # result = client_api.get_api_qr_code()
    # result = client_api.toggle_popups()

    ###########################################################################

    ################################
    # Everything related to Groups #
    ################################

    # ok :

    # to be tested :

    # not included in the current version :
    # result = client_api.create_group(data_16)
    # result = client_api.delete_group(name="TestAPI")
    # result = client_api.list_group()
    # result = client_api.get_group_info(data_18)
    # result = client_api.add_contact_to_group(data_17)
    # result = client_api.remove_contact_from_group(data_17)
    # result = client_api.send_group_file_message(data_19)
    # result = client_api.send_group_chat_message(data_20)
    # result = client_api.delete_group_message(
    #     msg_id="73ba804f503b8c4f7c9ccf35fb369ec860871496"
    # )
    # result = client_api.get_group_messages(name="TestAPI")

    ###########################################################################

    ################################
    # Everything related to Agenda #
    ################################

    # ok :

    # to be tested :

    # not included in the current version :
    # client_api.get_agenda_events(data_24)
    # client_api.get_event("d368b18421fb30a45d8b262f526d7aa31d57526a")
    # client_api.create_event(data_22)
    # client_api.update_event(data_23)
    # client_api.delete_event(event_id=)
    # client_api.reject_event(event_id=)
    # client_api.accept_event(event_id=)

    ###########################################################################

    ###############################
    # Everything related to Email #
    ###############################

    # ok :

    # to be tested :

    # not included in the current version :
    # client_api.edit_emails_frequency(data=)
    # client_api.link_emails(data=)

    ###########################################################################

    ################################
    # Everything related to Wallet #
    ################################

    # ok :
    '''
    json_make_payment = {
        "matr_id": "40b3551fe8cd576e710d613f79c199360533269f",
        "amount": "1.125"
    }
    result = client_api.make_payment(json_make_payment)
    '''
    # result = client_api.update_wallet()
    # result = client_api.get_transactions()

    # to be tested :

    # not included in the current version :

    ###########################################################################

    #########################################
    # Everything related to Generic Message #
    #########################################

    # ok :
    '''
    custom_content = {
        'brand': 'BMW',
        'model': 'M6'
    }
    json_send_generic_message = {
        'type': 'Ouioui',
        'scope': 'film',
        'action': 'send',
        'content': custom_content,
        'receivers': ['1a3dc918c938a22ab4b3d8ab7d9fae55cdb2b8cb'],
        'certify': False,
        'attachments': ['6']
    }

    custom_content_msf_create_case = {
        'type': 'MSF',
        'scope': 'medical_case',
        'action': 'create',
        'receivers': ['b71b9522f2050ad93f064e66738bbabc33225cd5'],
        'certify': False,
        'content': {
            'type': 'Patient-related clinical query (to a specific patient)',
            'subject': 'Cancer',
            'language': 'EN',
            'localization': 'Dire dawa, Ethiopia',
            'patient_name': 'Lilian',
            'patient_lastname': 'Laslandes',
            'patient_age': '45',
            'gender': 'male',
            'priority': 'critical',
            'referrer_id': '2',
            'complaint': 'Lorem Ipsum is simply dummy text of the printing and'
                         ' typesetting industry.',
            'history': 'and a search for lorem ipsum will uncover many web '
                       'sites still in their infancy.',
            'past': 'The standard chunk of Lorem Ipsum used since the 1500s'
        },
        'attachments': []
    }
    # result = client_api.send_generic_message(json_send_generic_message)
    '''
    '''
    json_get_generic_messages1 = {
        'type': 'MSF',
        'scope': 'medical_case',
        'action': '',
        'is_read': True
    }
    json_get_generic_messages2 = {
        'type': 'Ouioui',
        'scope': 'film',
        'action': '',
        'limit': 2,
        'date': '',
        'filter_date': '',
        'is_read': True
    }
    result = client_api.get_generic_messages(json_get_generic_messages1)
    '''

    # result = client_api.delete_generic_messages(
    #     message_id='f798701d1249944e8cc8214b5b5e353fd50511ff'
    # )

    # result = client_api.get_generic_message_status(
    #     message_id='b8b5e24dcf446ca6faeda4a944f41a08a117740c'
    # )

    # to be tested :

    # not included in the current version :

    ###########################################################################

    if isinstance(result, str):
        logg.debug("\n1===\n{0} \n===\n".format(result))
    else:
        logg.debug("\n2===\n{0} \n===\n".format(result.content))
