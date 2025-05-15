def handler(request, response):
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
        },
        'body': {'status': 'ok', 'message': 'Vision RAG API is online'}
    }
