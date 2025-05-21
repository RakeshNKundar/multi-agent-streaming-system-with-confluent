import json
from scheduler_agent import get_calendar_service_from_aws_secret_manager, schedule_meeting, produce_event_to_kafka, ensure_list_of_strings, sns_publisher

def lambda_handler(event, context):

    for events in event:
        schedule_event = events['payload']['value']

        meeting_info = {}
        meeting_info['title'] = schedule_event['title']
        meeting_info['description'] = schedule_event['description']
        meeting_info['location'] = schedule_event['location']
        meeting_info['start'] = schedule_event['start']
        meeting_info['end'] = schedule_event['end']
        meeting_info['attendees'] = ensure_list_of_strings(schedule_event['attendees'])

        # calendar_service = get_calendar_service_from_aws_secret_manager()

        event_link, error_message = sns_publisher(meeting_info)

        is_meeting_successful = error_message is None

        meeting_info['message_id'] = schedule_event['message_id']
        meeting_info['user_email'] = schedule_event['user_email']
        meeting_info['session_id'] = schedule_event['session_id']
        meeting_info['employee_id'] = schedule_event['employee_id']
        meeting_info['message'] = schedule_event['message']
        meeting_info['timestamp'] = schedule_event['timestamp']

        produce_event_to_kafka(meeting_info, event_link, is_meeting_successful, error_message)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Lambda executed successfully!')
    }
