"""
Alert Lambda Handler - CloudWatch/SNS Integration
Receives CloudWatch alerts via SNS and processes them
"""
import json
from typing import Dict, Any
from common.logging_config import get_logger

# Configure structured logging
logger = get_logger(__name__)


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        logger.info(
            "received_event",
            request_id=context.request_id if context else None,
            records_count=len(event.get('Records', []))
        )
        
        for record in event.get('Records', []):
            if record.get('EventSource') == 'aws:sns':
                process_sns_message(record)
        
        logger.info("alert_processed_successfully")
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Alert processed successfully'})
        }
        
    except Exception as e:
        logger.error("error_processing_alert", error=str(e), exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def process_sns_message(record: Dict[str, Any]) -> None:
    """
    Process individual SNS message
    
    Args:
        record: SNS record from the event
    """
    sns_data = record.get('Sns', {})
    message = sns_data.get('Message', '')
    subject = sns_data.get('Subject', 'No Subject')
    
    logger.info("processing_sns_message", subject=subject)
    
    try:
        # Try to parse message as JSON (CloudWatch alarms send JSON)
        alarm_data = json.loads(message)
        process_cloudwatch_alarm(alarm_data)
    except json.JSONDecodeError:
        # If not JSON, treat as plain text
        logger.info("plain_text_message", message=message)
        process_text_message(message)

def process_cloudwatch_alarm(alarm_data: Dict[str, Any]) -> None:
    """
    Process CloudWatch alarm data
    
    Args:
        alarm_data: Parsed CloudWatch alarm information
    """
    alarm_name = alarm_data.get('AlarmName', 'Unknown')
    new_state = alarm_data.get('NewStateValue', 'Unknown')
    reason = alarm_data.get('NewStateReason', 'No reason provided')
    timestamp = alarm_data.get('StateChangeTime', 'Unknown')
    
    logger.info(
        "cloudwatch_alarm_details",
        alarm_name=alarm_name,
        new_state=new_state,
        reason=reason,
        timestamp=timestamp
    )
    
    # TODO: Implement alert processing logic
    # Examples:
    # - Send email/Slack notification
    # - Store in database for analysis
    # - Trigger auto-remediation
    # - Create incident ticket
    
    if new_state == 'ALARM':
        logger.warning("alarm_state_detected", alarm_name=alarm_name)
        # Handle alarm state
    elif new_state == 'OK':
        logger.info("alarm_returned_to_ok", alarm_name=alarm_name)
        # Handle recovery
    else:
        logger.info("alarm_in_state", alarm_name=alarm_name, state=new_state)

def process_text_message(message: str) -> None:
    """
    Process plain text message
    
    Args:
        message: Plain text message content
    """
    logger.info("processing_text_message", message=message)
    # TODO: Implement text message processing
