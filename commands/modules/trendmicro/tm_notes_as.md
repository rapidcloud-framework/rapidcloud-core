### Application Security

    # TODO
    '''
    Node.js

    npm install --save trend_app_protect

    require('trend_app_protect');

    //import support added in version 4.5.0 and above for projects that require/support es6 modules
    import 'trend_app_protect';

    TREND_AP_KEY and TREND_AP_SECRET environment variables
    -or-
    trend_app_protect.json and be in the application root folder, and needs to contain at least the following:

    {
    "key": "my-key",
    "secret": "my-secret"
    }
    '''


    # TODO
    '''
    Python Lambda Functions

    pip install 

    1. Env Variables:

    TREND_AP_KEY: < key from Application Security Dashboard >
    TREND_AP_SECRET: < secret from Application Security Dashboard >
    TREND_AP_READY_TIMEOUT: 30
    TREND_AP_TRANSACTION_FINISH_TIMEOUT: 10
    TREND_AP_MIN_REPORT_SIZE: 1
    TREND_AP_INITIAL_DELAY_MS: 1
    TREND_AP_MAX_DELAY_MS: 100
    TREND_AP_HTTP_TIMEOUT: 5
    TREND_AP_PREFORK_MODE: False
    TREND_AP_CACHE_DIR: /tmp/trend_cache
    TREND_AP_LOG_FILE: STDERR    
    
    2. Add a layer to function
        arn:aws:lambda:<aws region>:800880067056:layer:CloudOne-ApplicationSecurity-<language>:<layer version>


    3. Code skeleton

    import trend_app_protect.start
    from trend_app_protect.api.aws_lambda import protect_handler

    @protect_handler
    def handler(event, context):

        # Your application code here

        return {
            'statusCode': 200,
            'body': 'Hello from Lambda',
        }
    '''


    # TODO
    '''
    WSGI based apps
    
    1. import trend_app_protect.start
    2. Set the TREND_AP_KEY and TREND_AP_SECRET environment variables
    '''


    - NO CODE CHANGES REQUIRED
        - The self-contained Application Security agent runs inside the process of your application without requiring any code changes in the application itself.
    - web applicatins ackend bincluding containerized and serverless
        - legacy applications, containers, and AWS Lambda and Fargate
    - notifies via Slack, PagerDuty, or NewRelic
    - supported languages: 
        Java (8 and newer)
        Python (2.7, 3.4 and newer)
        NodeJS (10 and newer)
        PHP (7.0 and newer)
        .NET (.NET Framework 4.5.2 and newer, .NET Core 2.0 and newer)
        Ruby  (2.0.0 and newer) coming soon
    - Application definitions
        Up to 300 serverless functions
        Up to 30 containers
        Up to 5 servers/VMs
        Up to one region 
    - 

