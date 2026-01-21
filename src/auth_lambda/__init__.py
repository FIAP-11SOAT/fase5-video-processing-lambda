"""
Auth Lambda - Authentication and Authorization service
Entry point for AWS Lambda
"""
from .presentation.router import lambda_handler, main_handler

__all__ = ['lambda_handler', 'main_handler']
